from cake_to_order.settings import TG_BOT_TOKEN
from keyboards import (main_page_keyboard, skip_button, skip_keyboard,
                       without_inscription_keyboard, time_selecting_keyboard,
                       go_home_keyboard, cake_menu_keyboard,
                       go_home_inline_button, cake_improve_keyboard,
                       forward_button, backward_button, page_button)
from texts import TEXTS

import os
from datetime import date, timedelta
from aiogram import Bot, Router
from aiogram.types import (Message, InlineKeyboardButton, CallbackQuery,
                           FSInputFile, InputMediaPhoto)
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cake_to_order.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
import django
from django.conf import settings

if not settings.configured:
    django.setup()

from main_app.models import (Client, Cake, Topping, Berry, Decor, CakeLevel,
                             CakeForm, OrderCake)


bot = Bot(TG_BOT_TOKEN, parse_mode='html')
router = Router()


class FSM(StatesGroup):
    shape_choosing_state = State()
    topping_choosing_state = State()
    berries_choosing_state = State()
    decor_choosing_state = State()
    add_inscription_state = State()
    add_comment_state = State()
    input_address_state = State()
    input_date_state = State()
    input_time_state = State()
    show_order_state = State()
    show_selected_cake_state = State()
    cake_menu_state = State()
    input_name_state = State()
    input_phone_state = State()


cake_pic = FSInputFile('pictures/Tort.png')
cake_levels = FSInputFile('pictures/Levels.png')
cake_shape = FSInputFile('pictures/figure.png')
toppings_photo = FSInputFile('pictures/topping.png')
berries_photo = FSInputFile('pictures/berries.png')
decor_photo = FSInputFile('pictures/decor.png')
inscription_photo = FSInputFile('pictures/Text.png')
add_decor_photo = FSInputFile('pictures/add_decor.jpg')

keys_to_check = ('cake_id', 'level_id', 'shape_id', 'topping_id', 'berry_id', 'decor_id')

levels = {1: '1 уровень (+400 р.)',
          2: '2 уровня (+750 р.)',
          3: '3 уровня (+1 100 р.', }
shapes = {1: '🟡 Круг (+400 р.)',
          2: '🟨 Квадрат (+600 р.)',
          3: '🟨🟨 Прямоугольник (+1 000 р.)', }


@router.message(CommandStart())
@router.message(Text(text='Вернуться в начало'))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    await bot.send_photo(chat_id=message.chat.id, photo=cake_pic,
                         caption=TEXTS['greeting'],
                         reply_markup=main_page_keyboard)


@router.callback_query(lambda callback: callback.data == 'Вернуться в начало')
async def process_main_menu_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    update = Message(message_id=callback.message.message_id, date=callback.message.date, chat=callback.message.chat)
    await process_start_command(update, state)


@router.callback_query(lambda callback: callback.data == 'Назад к выбору')
async def process_back_to_cake_choosing_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    update = Message(message_id=callback.message.message_id, date=callback.message.date, chat=callback.message.chat)
    await process_select_ready_button(update, state)


@router.message(Text(text='О нас'))
async def process_about_us_button(message: Message, state: FSMContext):
    await message.answer(text='Компания Cake WOW. Торты на заказ.\nНаш адрес: ул. Гагарина д.52\nТелефон: +7999 999 99 99',
                         reply_markup=main_page_keyboard)


@router.message(Text(text='Собрать свой авторский торт'))
async def process_custom_your_cake_button(message: Message, state: FSMContext):
    levels = CakeLevel.get_cake_level()
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=levels[level], callback_data=level) for level in levels]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=message.chat.id, photo=cake_levels,
                         caption='Сколько уровней будет?',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.shape_choosing_state)


@router.callback_query(StateFilter(FSM.shape_choosing_state))
async def process_level_choosing(callback: CallbackQuery, state: FSMContext):
    await state.update_data(level_id=callback.data)
    shapes = CakeForm.get_cake_form()
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=shapes[shape], callback_data=shape) for shape in shapes]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=callback.from_user.id, photo=cake_shape,
                         caption='Какой формы будет Ваш торт?',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.topping_choosing_state)


@router.callback_query(StateFilter(FSM.topping_choosing_state))
async def process_shape_choosing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == '"Прокачать" торт':
        await state.update_data(shape_id='no_data')
    else:
        await state.update_data(shape_id=callback.data)
    toppings = Topping.get_topping()
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=toppings[topping], callback_data=topping) for topping in toppings]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(skip_button)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=callback.from_user.id, photo=toppings_photo,
                         caption='Выбрать топинг',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.berries_choosing_state)


@router.callback_query(StateFilter(FSM.berries_choosing_state))
async def process_toping_choosing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(topping_id=callback.data)
    berries = Berry.get_berry()
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=berries[berry], callback_data=berry) for berry in berries]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(skip_button)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=callback.from_user.id, photo=berries_photo,
                         caption='Добавить ягод',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.decor_choosing_state)


@router.callback_query(StateFilter(FSM.decor_choosing_state))
async def process_berry_choosing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(berry_id=callback.data)
    decors = Decor.get_decor()
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=decors[decor], callback_data=decor) for decor in decors]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(skip_button)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=callback.from_user.id, photo=decor_photo,
                         caption='Выбрать декор',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.add_inscription_state)


@router.callback_query(StateFilter(FSM.add_inscription_state))
async def process_decor_choosing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(decor_id=callback.data)
    await bot.send_photo(chat_id=callback.from_user.id, photo=inscription_photo,
                         caption='Мы можем разместить на торте любую надпись\nОтправьте сообщение с надписью',
                         reply_markup=without_inscription_keyboard)
    await state.set_state(FSM.add_comment_state)


@router.callback_query(StateFilter(FSM.add_comment_state))
async def process_without_inscription_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(inscription='no_data')
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Добавьте комментарий к заказу',
                           reply_markup=skip_keyboard)
    await state.set_state(FSM.input_name_state)


@router.message(StateFilter(FSM.add_comment_state))
async def process_inscription_input(message: Message, state: FSMContext):
    await state.update_data(inscription=message.text)
    await message.answer(text='Добавьте комментарий к заказу',
                         reply_markup=skip_keyboard)
    # TODO: проверить клиента по базе
    await state.set_state(FSM.input_name_state)


@router.callback_query(StateFilter(FSM.input_name_state))
async def process_without_comment_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(comment=callback.data)
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Введите ваше имя:\nВводя ваши личные данные вы '
                           'даете согласие на обработку ваших персональных данных')
    await state.set_state(FSM.input_phone_state)


@router.message(StateFilter(FSM.input_name_state))
async def process_comment_input(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer(text='Введите ваше имя:\nВводя ваши личные данные вы '
                         'даете согласие на обработку ваших персональных данных')
    await state.set_state(FSM.input_phone_state)


@router.message(StateFilter(FSM.input_phone_state))
async def process_name_input(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Введите ваш телефон:')
    await state.set_state(FSM.input_address_state)


@router.message(StateFilter(FSM.input_address_state))
async def process_phone_input(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text='Введите адрес доставки:')
    await state.set_state(FSM.input_date_state)


@router.message(StateFilter(FSM.input_date_state))
async def process_address_input(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    day = date.today()
    dates = []
    for _ in range(8):
        day += timedelta(days=1)
        dates.append(day)
    dates = [f'{date.day}.{str(date.month).zfill(2)}' for date in dates]

    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=date, callback_data=date) for date in dates]
    kb_builder.row(*buttons, width=4)
    kb_builder.row(go_home_inline_button)
    await message.answer(text='Выберите дату доставки',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.input_time_state)


@router.callback_query(StateFilter(FSM.input_time_state))
async def process_date_input(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Выберите время',
                           reply_markup=time_selecting_keyboard)
    await state.set_state(FSM.show_order_state)


@router.callback_query(StateFilter(FSM.show_order_state))
async def process_time_input(callback: CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    await state.update_data(telegram_id=callback.from_user.id)
    cake_order = await state.get_data()
    await state.clear()
    for key in keys_to_check:
        if key not in cake_order:
            cake_order[key] = 'no_data'
    order = OrderCake.save_order(cake_order)
    await bot.send_message(chat_id=callback.from_user.id,
                           text=order,
                           reply_markup=go_home_keyboard)
    await state.set_state(default_state)


@router.message(Text(text='Выбрать из каталога'))
async def process_select_ready_button(message: Message, state: FSMContext):
    ready_cakes = Cake.get_cakes()
    page = 0
    photo = BufferedInputFile(file=ready_cakes[page]['img'], filename='photo.jpg')
    await state.update_data(page=page)
    page_button.text = f'{page + 1}/{len(ready_cakes)}'
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=cake, callback_data=cake) for cake in ready_cakes[page]['id']]
    kb_builder.row(*buttons, width=3)
    kb_builder.row(backward_button, page_button, forward_button, width=3)
    kb_builder.row(go_home_inline_button)
    await bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption='Выберите ваш любимый торт',
                         reply_markup=kb_builder.as_markup())
    await state.set_state(FSM.show_selected_cake_state)


@router.callback_query(lambda callback: callback.data.startswith('>>'))
async def process_forward_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    page = data['page']
    ready_cakes = Cake.get_cakes()
    if page < len(ready_cakes) - 1:
        page += 1
    else:
        return
    await state.update_data(page=page)
    photo = BufferedInputFile(file=ready_cakes[page]['img'], filename='photo.jpg')
    page_button.text = f'{page + 1}/{len(ready_cakes)}'
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=cake, callback_data=cake) for cake in ready_cakes[page]['id']]
    kb_builder.row(*buttons, width=3)
    kb_builder.row(backward_button, page_button, forward_button, width=3)
    kb_builder.row(go_home_inline_button)
    await bot.edit_message_media(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(media=photo),
                                 )
    await bot.edit_message_caption(chat_id=callback.from_user.id,
                                   message_id=callback.message.message_id,
                                   caption='Выберите ваш любимый торт',
                                   reply_markup=kb_builder.as_markup())


@router.callback_query(lambda callback: callback.data.startswith('<<'))
async def process_backward_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    ready_cakes = Cake.get_cakes()
    page = data['page']
    if page > 0:
        page -= 1
    else:
        return
    await state.update_data(page=page)
    photo = BufferedInputFile(file=ready_cakes[page]['img'], filename='photo.jpg')
    page_button.text = f'{page + 1}/{len(ready_cakes)}'
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=cake, callback_data=cake) for cake in ready_cakes[page]['id']]
    kb_builder.row(*buttons, width=3)
    kb_builder.row(backward_button, page_button, forward_button, width=3)
    kb_builder.row(go_home_inline_button)
    await bot.edit_message_media(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(media=photo),
                                 )
    await bot.edit_message_caption(chat_id=callback.from_user.id,
                                   message_id=callback.message.message_id,
                                   caption='Выберите ваш любимый торт',
                                   reply_markup=kb_builder.as_markup())


@router.callback_query(StateFilter(FSM.show_selected_cake_state),
                       ~Text(text='page_number'))
async def show_selected_cake(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(cake_id=callback.data)
    cake = Cake.get_cake(callback.data)
    image_bytes = cake['img'].read()
    photo = BufferedInputFile(file=image_bytes, filename='photo.jpg')
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                         caption=cake['text'],
                         reply_markup=cake_menu_keyboard)
    await state.set_state(FSM.cake_menu_state)


@router.callback_query(StateFilter(FSM.cake_menu_state),
                       lambda callback: callback.data == 'Заказать')
async def process_order_ready_cake_button(callback: CallbackQuery):
    await callback.answer()
    await bot.send_photo(chat_id=callback.from_user.id, photo=add_decor_photo,
                         caption='Вы можете добавить топинг, ягоды, декор и надпись к выбранному торту',
                         reply_markup=cake_improve_keyboard)


@router.callback_query(StateFilter(FSM.cake_menu_state),
                       lambda callback: callback.data == '"Прокачать" торт')
async def process_improve_cake_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_shape_choosing(callback, state)


@router.callback_query(StateFilter(FSM.cake_menu_state),
                       lambda callback: callback.data == 'Подтвердить заказ')
async def process_confirm_order_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_without_inscription_button(callback, state)
