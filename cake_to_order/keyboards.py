from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)


custom_your_cake_button = KeyboardButton(text='Собрать свой авторский торт')
choose_from_catalog_button = KeyboardButton(text='Выбрать из каталога')

skip_button = InlineKeyboardButton(text='Пропустить', callback_data='no_data')
without_inscription_button = InlineKeyboardButton(text='Без надписи ', callback_data='no_data')
time_button_1 = InlineKeyboardButton(text='11:00 - 15:00', callback_data='11:00 - 15:00')
time_button_2 = InlineKeyboardButton(text='15:00 - 19:00', callback_data='15:00 - 19:00')
go_home_button = KeyboardButton(text='Вернуться в начало')
about_us_button = KeyboardButton(text='О нас')
order_ready_cake_button = InlineKeyboardButton(text='Заказать', callback_data='Заказать')
back_to_cake_choosing_button = InlineKeyboardButton(text='Назад к выбору', callback_data='Назад к выбору')
go_home_inline_button = InlineKeyboardButton(text='Вернуться в начало', callback_data='Вернуться в начало')
confirm_order_button = InlineKeyboardButton(text='Подтвердить заказ', callback_data='Подтвердить заказ')
improve_cake_button = InlineKeyboardButton(text='"Прокачать" торт', callback_data='"Прокачать" торт')
forward_button = InlineKeyboardButton(text='>>', callback_data='>>')
backward_button = InlineKeyboardButton(text='<<', callback_data='<<')
page_button = InlineKeyboardButton(text='/', callback_data='page_number')


main_page_keyboard = ReplyKeyboardMarkup(keyboard=[[custom_your_cake_button], [choose_from_catalog_button], [about_us_button]], resize_keyboard=True, one_time_keyboard=True)
without_inscription_keyboard = InlineKeyboardMarkup(inline_keyboard=[[without_inscription_button], [go_home_inline_button]])
skip_keyboard = InlineKeyboardMarkup(inline_keyboard=[[skip_button], [go_home_inline_button]])
time_selecting_keyboard = InlineKeyboardMarkup(inline_keyboard=[[time_button_1, time_button_2], [go_home_inline_button]])
go_home_keyboard = ReplyKeyboardMarkup(keyboard=[[go_home_button]], resize_keyboard=True)
cake_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[order_ready_cake_button], [back_to_cake_choosing_button], [go_home_inline_button]])
cake_improve_keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_order_button], [improve_cake_button], [go_home_inline_button]])
