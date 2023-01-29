from aiogram import executor

from create_bot import dp

async def on_startup(_):
    print("The bot has been started successfully!")

from handlers import client, admin, others

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == "__main__":
    executor.start_polling(dp,
                           on_startup=on_startup,
                           skip_updates=True)
