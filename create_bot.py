import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv

dotenv.load_dotenv()
ADMINS = [int(_) for _ in os.getenv("ADMINS").split(",")]

storage = MemoryStorage()
bot = Bot(os.getenv('API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
