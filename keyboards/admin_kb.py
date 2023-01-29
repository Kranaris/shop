from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import StatesGroup, State

products_cb = CallbackData('product', 'id', 'action')


def get_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/управление")]
    ], resize_keyboard=True)
    return kb


def product_manager() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/показать_все_продукты")],
        [KeyboardButton("/добавить_новый_продукт")]
    ], resize_keyboard=True)
    return kb


def get_edit_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Изменить_продукт", callback_data=products_cb.new(product_id, 'edit'))],
        [InlineKeyboardButton("Удалить_продукт", callback_data=products_cb.new(product_id, 'delete'))],
    ])

    return ikb


def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/отмена'))
