from aiogram import Bot, Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import dotenv


dotenv.load_dotenv()

storage = MemoryStorage()
bot = Bot(os.getenv('API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
