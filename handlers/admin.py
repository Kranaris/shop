from aiogram import types, Dispatcher

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher.storage import FSMContext

from create_bot import bot

from keyboards.admin_kb import *

import sqllite

from config import ADMINS


class Product_statesGroup(StatesGroup):
    photo = State()
    title = State()
    description = State()
    price = State()
    edit_photo = State()
    edit_some = State()


async def show_all_products(message: types.Message, products: list) -> None:
    if message.from_user.id in ADMINS:
        for product in products:
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=product[1],
                                 caption=f"Product_id: {product[0]}\n"
                                         f"Название: <b>{product[2]}</b>\n"
                                         f"Описание: <em>{product[3]}</em>\n"
                                         f"Цена: <em>{product[4]} RUB</em>",
                                 parse_mode='html',
                                 reply_markup=get_product_ikb(product[0]))


async def start_command_admin(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет Босс!',
                             reply_markup=get_admin_kb())
        await message.delete()
    else:
        await bot.send_message(chat_id=ADMINS[0],
                               text=f'Пользователь\n'
                                    f'Username: @{message.from_user.username}\n'
                                    f'id: {message.from_user.id}\n'
                                    f'попытался воспользоваться правами администратора')


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        if state is None:
            return
        await message.reply('Действие отменено!',
                            reply_markup=get_admin_kb())

        await state.finish()


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


async def check_price(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.reply("Напиши цену целым числом!")


async def handle_price(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['description'] = message.text

        await message.reply("Напиши цену:")
        await Product_statesGroup.next()


async def handle_finish(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['price'] = message.text
        await sqllite.create_new_product(state)
        await message.reply("Продукт добавлен!",
                            reply_markup=get_admin_kb())
        await state.finish()


async def cb_delete_product(callback: types.CallbackQuery, callback_data: dict) -> None:
    await sqllite.delete_product(callback_data['id'])

    await callback.message.reply("Продукт был удален!")
    await callback.answer()


async def cb_edit_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['caption'] = callback.message.caption
    await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   caption="Что изменить?",
                                   reply_markup=get_edit_ikb(callback_data['id'])
                                   )


async def cb_back(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                       message_id=callback.message.message_id,
                                       caption=data['caption'],
                                       reply_markup=get_product_ikb(callback_data['id'])
                                       )


async def edit_some(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = callback_data['id']
        data['action'] = callback_data["action"]
        data['photo_before'] = callback.message.message_id
        if callback_data["action"] == 'photo':
            await callback.message.answer("Загрузи новое фото:",
                                          reply_markup=get_cancel())
            await Product_statesGroup.edit_photo.set()
        else:
            await callback.message.answer("Напиши новое:",
                                          reply_markup=get_cancel())
            await Product_statesGroup.edit_some.set()
            data['message'] = callback.message.message_id
    await callback.answer()


async def load_new_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        await sqllite.edit_photo(data['product_id'], message.photo[0].file_id)
    product = await sqllite.get_one_product_bd(data['product_id'])
    await message.delete()
    await bot.send_photo(chat_id=message.chat.id,
                         photo=product[1],
                         caption=f"Product_id: {product[0]}\n"
                                 f"Название: <b>{product[2]}</b>\n"
                                 f"Описание: <em>{product[3]}</em>\n"
                                 f"Цена: <em>{product[4]} RUB</em>",
                         parse_mode='html',
                         reply_markup=get_product_ikb(product[0]))
    await message.answer(text="Продолжим!",
                         reply_markup=get_admin_kb())
    await state.finish()


async def load_new_some(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if data['action'] == 'price' and not message.text.isdigit():
            await message.reply("Цена должна быть целым числом!")
        else:
            await sqllite.edit_some(data['product_id'], data['action'], message.text)
            await message.reply("Изменено!",
                                reply_markup=get_admin_kb())
            product = await sqllite.get_one_product_bd(data['product_id'])
            await bot.edit_message_caption(chat_id=message.chat.id,
                                           message_id=data['message'],
                                           caption=f"Product_id: {product[0]}\n"
                                                   f"Название: <b>{product[2]}</b>\n"
                                                   f"Описание: <em>{product[3]}</em>\n"
                                                   f"Цена: <em>{product[4]} RUB</em>",
                                           parse_mode='html',
                                           reply_markup=get_product_ikb(product[0])
                                           )
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
    dp.register_message_handler(cancel_command, commands=['отмена'], state="*")
    dp.register_message_handler(product_command, commands=['управление'])
    dp.register_message_handler(get_all_products, commands=['показать_все_продукты'])
    dp.register_message_handler(add_new_product, commands=['добавить_новый_продукт'])
    dp.register_message_handler(check_photo, lambda message: not message.photo,
                                state=[Product_statesGroup.photo, Product_statesGroup.edit_photo])
    dp.register_message_handler(load_photo, content_types=['photo'], state=Product_statesGroup.photo)
    dp.register_message_handler(handle_title, state=Product_statesGroup.title)
    dp.register_message_handler(check_price, lambda message: not message.text.isdigit(),
                                state=Product_statesGroup.price)
    dp.register_message_handler(handle_price, state=Product_statesGroup.description)
    dp.register_message_handler(handle_finish, state=Product_statesGroup.price)
    dp.register_callback_query_handler(cb_delete_product, products_cb.filter(action='delete'))
    dp.register_callback_query_handler(cb_edit_product, products_cb.filter(action='edit'))
    dp.register_callback_query_handler(cb_back, products_cb.filter(action='back'))
    dp.register_callback_query_handler(edit_some, products_cb.filter(action=['title', 'description', 'price', 'photo']))
    dp.register_message_handler(load_new_photo, content_types=['photo'], state=Product_statesGroup.edit_photo)
    dp.register_message_handler(load_new_some, state=Product_statesGroup.edit_some)
