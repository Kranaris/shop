from aiogram import types, Dispatcher

from config import ADMINS

async def start_command_admin(message: types.Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет Босс!')
        await message.delete()
    else:
        await message.reply(f'Ты не Администратор')
        await message.delete()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_command_admin, commands=['админ'])