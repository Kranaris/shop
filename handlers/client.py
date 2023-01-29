from aiogram import types, Dispatcher

from keyboards import get_start_kb

async def start_command_client(message: types.Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}!',
                         reply_markup=get_start_kb())
    await message.delete()

async def product_command(message: types.Message) -> None:
    await message.answer(f'Продукты:')
    await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])
    dp.register_message_handler(product_command, commands=['Продукты'])
