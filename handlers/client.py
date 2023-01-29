from aiogram import types, Dispatcher


async def start_command_client(message: types.Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}!')
    await message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_client, commands=['start'])