from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

client_cb = CallbackData('product', 'id', 'action')
def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/Продукты")],
    ], resize_keyboard=True, one_time_keyboard=True)

    return kb

def get_buy_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Купить", callback_data=client_cb.new(product_id, 'buy'))],
    ])

    return ikb