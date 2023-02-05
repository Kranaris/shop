from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

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


def get_product_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Изменить", callback_data=products_cb.new(product_id, 'edit'))],
        [InlineKeyboardButton("Удалить", callback_data=products_cb.new(product_id, 'delete'))],

    ])

    return ikb


def get_edit_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Изменить_фото", callback_data=products_cb.new(product_id, 'photo'))],
        [InlineKeyboardButton("Изменить_название", callback_data=products_cb.new(product_id, 'title'))],
        [InlineKeyboardButton("Изменить_описание", callback_data=products_cb.new(product_id, 'description'))],
        [InlineKeyboardButton("Изменить_цену", callback_data=products_cb.new(product_id, 'price'))],
        [InlineKeyboardButton("Назад", callback_data=products_cb.new(product_id, 'back'))],

    ])

    return ikb


def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/отмена'))
