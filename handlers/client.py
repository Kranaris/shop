from aiogram import types, Dispatcher

from create_bot import bot

import sqllite

from keyboards.client_kb import *

from config import ADMINS


async def show_all_products_client(message: types.Message, products: list) -> None:
    for product in products:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=product[1],
                             caption=f"{product[0]} из {len(products)}\n"
                                     f"Название: <b>{product[2]}</b>\n"
                                     f"Описание: <em>{product[3]}</em>\n"
                                     f"Цена: <em>{product[4]} RUB</em>",
                             parse_mode='html',
                             reply_markup=get_buy_ikb(product[0])
                             )


async def start_command_client(message: types.Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}!',
                         reply_markup=get_start_kb())
    await message.delete()


async def product_command_client(message: types.Message) -> None:
    products = await sqllite.get_all_products_bd()

    if not products:
        await message.answer("Пока нет продуктов!")
        await message.delete()

    await show_all_products_client(message, products)


async def cb_buy_product(callback: types.CallbackQuery) -> None:
    product_data = callback.data.split(':')
    await bot.send_message(ADMINS[0], text=f"Новый Зааказ!\n"
                                           f"Клиент: @{callback.from_user.username}\n"
                                           f"Product_id: {product_data[1]}"
                           )
    await callback.message.reply("Заявка на покупку отправлена Администратору!\n"
                                 "Пожалуйста ожидайте ответ.")
    await callback.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])
    dp.register_message_handler(product_command_client, commands=['Продукты'])
    dp.register_callback_query_handler(cb_buy_product, client_cb.filter(action="buy"))
