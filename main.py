"""Главный модуль бота."""

import datetime
import shlex

import pytz
import telebot
from telebot import types

from db_module import (user_create, user_exist,
                       user_get_action, user_set_action,
                       project_create, user_get_status,
                       user_set_status, check_date,
                       get_status_my_proj, review_add)

TOKEN = ''
NASTYA_ID = 466699718

default_timezone = pytz.timezone('Europe/Kaliningrad')
datetime.datetime.now(default_timezone)


buttons_name = {
    'price': 'Прайс ❤️',
    'works': 'Работы 🎥',
    'check_date': 'Проверить дату 📆',
    'stage': 'Стадия монтажа 🔍',
    'order': 'Записаться 📝',
    'review': 'Оставить отзыв 💌',
    'cancel': 'Отмена',
    'send_order': 'Молча отправить✅',
    'admin': 'Админка 📱',
    'add_proj': 'Добавить проект 📗'
}

main_menu_user = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_user.add(types.KeyboardButton(buttons_name['price']),
                   types.KeyboardButton(buttons_name['works']),
                   types.KeyboardButton(buttons_name['check_date']),
                   types.KeyboardButton(buttons_name['stage']),
                   types.KeyboardButton(buttons_name['order']),
                   types.KeyboardButton(buttons_name['review']),
                   )

main_menu_admin = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_admin.add(types.KeyboardButton(buttons_name['price']),
                    types.KeyboardButton(buttons_name['works']),
                    types.KeyboardButton(buttons_name['check_date']),
                    types.KeyboardButton(buttons_name['stage']),
                    types.KeyboardButton(buttons_name['order']),
                    types.KeyboardButton(buttons_name['review']),
                    types.KeyboardButton(buttons_name['admin']),
                    )

cancel_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_menu.add(types.KeyboardButton(buttons_name['cancel']))

order_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
order_menu.add(types.KeyboardButton(buttons_name['send_order']))
order_menu.add(types.KeyboardButton(buttons_name['cancel']))

admin_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
admin_menu.add(types.KeyboardButton(buttons_name['add_proj']))
admin_menu.add(types.KeyboardButton(buttons_name['cancel']))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def user_register(message):
    """Добавляение пользователя в бд."""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    date_joined = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    last_interaction = date_joined
    user_data = (user_id, username, first_name,
                 last_name, date_joined, last_interaction)
    if not user_exist(user_id):
        user_create(user_data)
    bot.send_message(message.chat.id, 'Добро пожаловать!',
                     reply_markup=main_menu_user)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    """Основной обработчик текста."""
    text = message.text
    print(text)
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка на админку и установка нужного меню
    if user_get_status(user_id) == 'admin':
        main_menu = main_menu_admin
    else:
        main_menu = main_menu_user
    
    # Команда Прайс
    if text == buttons_name['price']:
        bot.send_message(chat_id, 'Прайс Настеньки еще не написан!',
                         reply_markup=main_menu)
        
    # Команда Посмотреть работы
    elif text == buttons_name['works']:
        bot.send_message(chat_id, 'Тут пока пусто',
                         reply_markup=main_menu)
        
    # Команда посмотреть свободна ли дата
    elif text == buttons_name['check_date']:
        msg = '''Введите интересующую вас дату в формате д.м.г
Пример: 01.06.2024'''
        bot.send_message(chat_id, msg, reply_markup=cancel_menu)
        user_set_action(user_id, 'check_date')

    # Команда проверки статуса проектов пользователя
    elif text == buttons_name['stage']:
        projects = get_status_my_proj(username)
        statuses = ''
        if projects:
            for project in projects:
                statuses += f'Проект: {project[0]}\nCтатус: {project[1]}\n\n'
            msg = f'Сводка о ваших проектах:\n\n{statuses}'
            bot.send_message(chat_id, msg, reply_markup=main_menu)
        else:
            msg = 'За вашим аккаунтом не закреплено действующих проектов'
            bot.send_message(chat_id, msg, reply_markup=main_menu)

    elif text == buttons_name['order']:
        msg = """Ваша заявка будет отправлена лично Настеньке
Вы можете отправить сообщение заявки или нажать кнопку подтвердить"""
        bot.send_message(chat_id, msg, reply_markup=order_menu)
        user_set_action(user_id, 'send_order')

    elif text == buttons_name['review']:
        bot.send_message(chat_id, 'Напишите ваш отзыв', reply_markup=cancel_menu)
        user_set_action(user_id, 'send_review')

    # Команда возврата отмены действия и возврата в гл. меню
    elif text == buttons_name['cancel']:
        bot.send_message(chat_id, 'Главное меню', reply_markup=main_menu)
        user_set_action(user_id, 'menu')

    # Команда добавить проект
    elif text == buttons_name['add_proj']:
        msg = """Введите промпт
Шаблон: 'название проекта' заказчик цена дата время
Пример: 'BLACKPINK - TOMBOY' @sorotto 3500 01.06.2024 15:00-17:00 """
        bot.send_message(chat_id, msg, reply_markup=cancel_menu)
        user_set_action(user_id, 'add_project')

    # Команда перехода в админ меню
    elif text == buttons_name['admin']:
        bot.send_message(chat_id, 'Вы вошли в админку', reply_markup=admin_menu)

    # Обработка текста вне кнопок
    else:
        action = user_get_action(user_id)

        # Обработка ввода для добавления проекта
        if action == 'add_project':
            try:
                parts = shlex.split(text)
                project_name = parts[0].strip("'")
                customer = parts[1]
                price = int(parts[2])
                date = parts[3]
                time_range = parts[4]
                data = (project_name, price, customer, date, time_range)
                project_create(data)
                user_set_action(user_id, 'menu')
                bot.send_message(chat_id, 'Проект успешно добавлен!', reply_markup=main_menu)
            except ValueError:
                msg = """[Ошибка]: Некорректный формат!
Убедитесь в правильности запроса.
Ковычек, обрамляющих название, должно быть ровно две!"""
                bot.send_message(chat_id, msg, reply_markup=main_menu)
        elif action == 'check_date':
            try:
                dates = check_date(text)
                if dates:
                    times = ''
                    for date in dates:
                        times += f'{date[0]} \n'
                    msg = f'Занятые часы в этот день:\n{times}'
                    bot.send_message(chat_id, msg, reply_markup=main_menu)
                else:
                    msg = 'Этот день свободен, я вся ваша👌🏻'
                    bot.send_message(chat_id, msg, reply_markup=main_menu)
                user_set_action(user_id, 'menu')
            except ValueError:
                msg = '[Ошибка]: Проверьте корретность введенной даты'
                bot.send_message(chat_id, msg, reply_markup=main_menu)

        elif action == 'send_order':
            msg_user = 'Ваша заявка отправлена! С вами свяжутся :)'
            if text == buttons_name['send_order']:
                msg_nastya = f'Опачки, заявочка от @{username}'
            else:
                msg_nastya = f'Опачки, заявочка от @{username}\n\n{text}'
            bot.send_message(NASTYA_ID, msg_nastya)
            bot.send_message(chat_id, msg_user, reply_markup=main_menu)

        elif action == 'send_review':
            msg_user = 'Ваш отзыв отправлен❤️'
            msg_nastya = f'Опачки, у тебя новый отзыв:\n\n{text}'
            send_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            data = (username, send_date, text)
            review_add(data)
            bot.send_message(chat_id, msg_user, reply_markup=main_menu)
            bot.send_message(NASTYA_ID, msg_nastya)


bot.polling(none_stop=True)
