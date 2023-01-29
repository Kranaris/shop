from aiogram import types, Dispatcher

from aiogram.dispatcher.storage import FSMContext

from create_bot import bot

from keyboards.admin_kb import *

import sqllite

from config import ADMINS


class Product_statesGroup(StatesGroup):
    photo = State()
    title = State()
    description = State()
    edit_title = State()


async def show_all_products(message: types.Message, products: list) -> None:
    if message.from_user.id in ADMINS:
        for product in products:
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=product[1],
                                 caption=f"Product_id: {product[0]}\n"
                                         f"Title: <b>{product[2]}</b>\n"
                                         f"Description: <em>{product[3]}</em>",
                                 parse_mode='html',
                                 reply_markup=get_edit_ikb(product[0]))


async def start_command_admin(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет Босс!',
                             reply_markup=get_admin_kb())
        await message.delete()
    else:
        await message.reply(f'Ты не Администратор')
        await message.delete()


async def product_command(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Управление продуктами:',
                             reply_markup=product_manager())
        await message.delete()
    else:
        await message.reply(f'Ты не Администратор')
        await message.delete()


async def add_new_product(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.delete()
        await message.answer("Загрузи фото",
                             reply_markup=get_cancel())

        await Product_statesGroup.photo.set()


async def check_photo(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.reply("Это не фото!")


async def load_photo(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id

        await message.reply("Напиши название:")
        await Product_statesGroup.next()


async def handle_title(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['title'] = message.text

        await message.reply("Напиши описание:")
        await Product_statesGroup.next()


async def handle_finish(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['description'] = message.text
        await sqllite.create_new_product(state)
        await message.reply("Продукт добавлен!",
                            reply_markup=get_admin_kb())
        await state.finish()


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        if state is None:
            return
        await message.reply('Добавление отменено!',
                            reply_markup=get_admin_kb())

        await state.finish()


async def get_all_products(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        products = await sqllite.get_all_products_bd()

        if not products:
            await message.answer("Пока нет продуктов!")
            await message.delete()

        await show_all_products(message, products)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_command_admin, commands=['админ', 'admin'])
    dp.register_message_handler(product_command, commands=['управление'])
    dp.register_message_handler(cancel_command, commands=['отмена'])
    dp.register_message_handler(get_all_products, commands=['показать_все_продукты'])
    dp.register_message_handler(add_new_product, commands=['добавить_новый_продукт'])
    dp.register_message_handler(check_photo, lambda message: not message.photo, state=Product_statesGroup.photo)
    dp.register_message_handler(load_photo, content_types=['photo'], state=Product_statesGroup.photo)
    dp.register_message_handler(handle_title, state=Product_statesGroup.title)
    dp.register_message_handler(handle_finish, state=Product_statesGroup.description)