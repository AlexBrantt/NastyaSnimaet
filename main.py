"""Главный модуль бота."""

import datetime
import shlex
import time
import urllib3
import requests
import os
from dotenv import load_dotenv

import pytz
import telebot

from db_module import (user_create, user_exist,
                       user_get_action, user_set_action,
                       project_create, user_get_status,
                       user_set_status, check_date,
                       get_status_my_proj, review_add,
                       order_add, get_orders, get_reviews,
                       delete_order, delete_review,
                       get_project_by_name, edit_project,
                       delete_project, user_get_select,
                       user_set_select, update_last_interaction,)

from buttons import (buttons_name, main_menu_admin,
                     main_menu_user, delete_menu,
                     cancel_menu, order_menu,
                     admin_menu, cancel_menu_admin,
                     get_project_menu, project_edit,
                     cancel_edit_proj, delete_confirm_menu,)

from validators import date_validator

from messages import messages_dict

load_dotenv()

TOKEN = os.getenv('TOKEN')
NASTYA_ID = os.getenv('NASTYA_ID')
ALEX = os.getenv('ALEX_ID')
DEBUG_ADMIN = 'root'

default_timezone = pytz.timezone('Europe/Kaliningrad')
datetime.datetime.now(default_timezone)

bot = telebot.TeleBot(TOKEN)


def get_current_datetime():
    """Получить текущую дату время."""
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def check_admin(user_id):
    """Проверка на админку."""
    if user_get_status(user_id) == 'admin':
        return True
    return False


def time_to_minutes(time_str):
    """Функция для преобразования строки времени в числовое значение для удобства сортировки."""
    start_time = time_str.split('-')[0]
    hours, minutes = map(int, start_time.split(':'))
    return hours * 60 + minutes


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
    bot.send_message(message.chat.id, messages_dict['start'],
                     reply_markup=main_menu_user)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    """Основной обработчик текста."""
    text = message.text
    print(text)
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    last_interaction = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    update_last_interaction(user_id, last_interaction)

    # Проверка на админку и установка нужного меню
    if check_admin(user_id):
        main_menu = main_menu_admin
    else:
        main_menu = main_menu_user

    if text == DEBUG_ADMIN:
        if check_admin(user_id):
            user_set_status(user_id, 'user')
            bot.send_message(chat_id, 'С вас сняты права админа',
                             reply_markup=main_menu_user)
        else:
            user_set_status(user_id, 'admin')
            bot.send_message(chat_id, 'Вы стали админом',
                             reply_markup=main_menu_admin)
        return

    # Команда Прайс
    if text == buttons_name['price']:
        bot.send_message(chat_id, messages_dict['price'],
                         reply_markup=main_menu)

    # Команда Посмотреть работы
    elif text == buttons_name['works']:
        bot.send_message(chat_id, messages_dict['works'],
                         reply_markup=main_menu)

    # Команда посмотреть свободна ли дата
    elif text == buttons_name['check_date']:
        bot.send_message(chat_id, messages_dict['check_date'],
                         reply_markup=cancel_menu)
        user_set_action(user_id, 'check_date')

    # Команда проверки статуса проектов пользователя
    elif text == buttons_name['stage']:
        projects = get_status_my_proj(username)
        statuses = ''
        if projects:
            for project in projects:
                statuses += f'Проект: {project[0]}\nCтатус: {project[1]}\n\n'
            msg = f'{messages_dict["stage_if"]}\n\n{statuses}'
            bot.send_message(chat_id, msg, reply_markup=main_menu)
        else:
            bot.send_message(chat_id, messages_dict['stage_else'],
                             reply_markup=main_menu)

    elif text == buttons_name['order']:
        bot.send_message(chat_id, messages_dict['order'],
                         reply_markup=order_menu)
        user_set_action(user_id, 'send_order')

    elif text == buttons_name['review']:
        bot.send_message(chat_id, messages_dict['review'],
                         reply_markup=cancel_menu)
        user_set_action(user_id, 'send_review')

    # Команда возврата отмены действия и возврата в гл. меню
    elif text == buttons_name['cancel']:
        bot.send_message(chat_id, messages_dict['cancel'],
                         reply_markup=main_menu)
        user_set_action(user_id, 'menu')

    # Команда перехода в админ меню
    elif text == buttons_name['admin']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['admin'],
                         reply_markup=admin_menu)

    # Команда добавить проект
    elif text == buttons_name['add_proj']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['add_proj'],
                         reply_markup=cancel_menu)
        user_set_action(user_id, 'admin_add_project')

    # Команда получения всех активных заявок
    elif text == buttons_name['get_orders']:
        if not check_admin(user_id):
            return
        orders = get_orders()
        order_list = ''
        for order in orders:
            order_list += f'Отправитель: @{order[0]}\nТекст: {order[1]}\n\n'
        if not orders:
            order_list = messages_dict['empty']
        msg = f'{messages_dict["orders_head"]}\n\n{order_list}'
        bot.send_message(chat_id, msg)

    # Команда получения отзывов
    elif text == buttons_name['get_reviews']:
        if not check_admin(user_id):
            return
        reviews = get_reviews()
        rev_list = ''
        for review in reviews:
            rev_list += f'@{review[0]}\n💌: {review[1]}\n\n'
        if not reviews:
            rev_list = messages_dict['empty']
        msg = f'{messages_dict["reviews_head"]}\n\n{rev_list}'
        bot.send_message(chat_id, msg)

    elif text == buttons_name['delete_menu']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['delete_menu'],
                         reply_markup=delete_menu)

    elif text == buttons_name['cancel_admin']:
        if not check_admin(user_id):
            return
        user_set_action(user_id, 'menu')
        bot.send_message(chat_id, messages_dict['cancel_admin'],
                         reply_markup=admin_menu)

    elif text == buttons_name['delete_order']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['delete_order'],
                         reply_markup=cancel_menu_admin)
        user_set_action(user_id, 'delete_order')

    elif text == buttons_name['delete_review']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['delete_review'],
                         reply_markup=cancel_menu_admin)
        user_set_action(user_id, 'delete_review')

    elif text == buttons_name['projects_menu']:
        if not check_admin(user_id):
            return
        projects_menu = get_project_menu()
        bot.send_message(chat_id, 'Меню проектов',
                         reply_markup=projects_menu)
        user_set_action(user_id, 'project_edit')

    # Обработка изменения проекта
    elif text == buttons_name['edit_proj_name']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите новое название',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_name')

    elif text == buttons_name['edit_proj_price']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите цену',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_price')

    elif text == buttons_name['edit_proj_customer']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите логин заказчика',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_customer')

    elif text == buttons_name['edit_proj_status']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите новый статус',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_status')

    elif text == buttons_name['edit_proj_date']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите дату',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_date')

    elif text == buttons_name['edit_proj_time']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите время',
                         reply_markup=cancel_edit_proj)
        user_set_action(user_id, 'edit_proj_time')

    elif text == buttons_name['delete_proj']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Подтвердите удаление',
                         reply_markup=delete_confirm_menu)
        user_set_action(user_id, 'delete_proj')

    elif text == buttons_name['cancel_edit_proj']:
        if not check_admin(user_id):
            return
        proj_menu = get_project_menu()
        bot.send_message(chat_id, 'Отменено',
                         reply_markup=proj_menu)
        user_set_action(user_id, 'project_edit')
        
    elif text == buttons_name['confirm_delete_proj']:
        if not check_admin(user_id):
            return
        delete_project(user_get_select(user_id))
        proj_menu = get_project_menu()
        bot.send_message(chat_id, 'Проект успешно удален',
                         reply_markup=proj_menu)
        user_set_action(user_id, 'project_edit')

    # Обработка текста вне кнопок
    else:
        action = user_get_action(user_id)
        proj_select = user_get_select(user_id)

        # Обработка ввода для добавления проекта
        if action == 'admin_add_project':
            if not check_admin(user_id):
                return
            try:
                parts = shlex.split(text)
                project_name = parts[0].strip("'")
                customer = parts[1] if len(parts) > 1 else None
                price = int(parts[2]) if len(parts) > 2 else None
                date = parts[3] if len(parts) > 3 else None
                time_range = parts[4] if len(parts) > 4 else None

                valid_date = date_validator(date)
                if valid_date:
                    data = (
                            project_name,
                            price,
                            customer.replace('@', '') if customer is not None else None,
                            valid_date,
                            time_range
                        )
                    project_create(data)
                    user_set_action(user_id, 'menu')
                    bot.send_message(chat_id, messages_dict['proj_added'],
                                     reply_markup=main_menu)
                else:
                    bot.send_message(chat_id, messages_dict['check_date_error'])
            except IndexError:
                err_msg = "Ошибка: недостаточно аргументов в введенной строке."
                bot.send_message(chat_id, err_msg,
                                 reply_markup=main_menu)
            except ValueError:
                bot.send_message(chat_id, messages_dict['proj_error'],
                                 reply_markup=main_menu)

        # Обработка ввода проверки даты
        elif action == 'check_date':
            if date_validator(text):
                dates = check_date(text)
                if dates:
                    sorted_times = sorted([time[0] for time in dates],
                                          key=time_to_minutes)
                    times = '\n'.join(sorted_times)
                    msg = f'{messages_dict["check_date_times"]}\n{times}'
                    bot.send_message(chat_id, msg, reply_markup=main_menu)
                else:
                    bot.send_message(chat_id, messages_dict['check_date_free'],
                                     reply_markup=main_menu)
                user_set_action(user_id, 'menu')
            else:
                msg = messages_dict['check_date_error']
                bot.send_message(chat_id, msg)

        # Обработка ввода отправки заявки
        elif action == 'send_order':
            msg_user = messages_dict['send_order']
            if text == buttons_name['send_order']:
                msg_nastya = f'{messages_dict["give_order"]} @{username}'
            else:
                msg_nastya = f'{messages_dict["give_order"]} @{username}\n\n{text}'
            bot.send_message(NASTYA_ID, msg_nastya)
            bot.send_message(chat_id, msg_user, reply_markup=main_menu)
            order_add((username, get_current_datetime(), text))
            user_set_action(user_id, 'menu')

        # Обработка ввода отправки отзыва
        elif action == 'send_review':
            msg_user = messages_dict['send_review']
            msg_nastya = f'{messages_dict["give_review"]}\n\n{text}'
            send_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            data = (username, send_date, text)
            bot.send_message(chat_id, msg_user, reply_markup=main_menu)
            bot.send_message(NASTYA_ID, msg_nastya)
            review_add(data)
            user_set_action(user_id, 'menu')

        elif action == 'delete_order':
            if not check_admin(user_id):
                return
            customer = text.replace('@', '')
            if delete_order(customer):
                msg = f'Заяки пользователя {text} удалены'
                bot.send_message(chat_id, msg, reply_markup=admin_menu)
            else:
                msg = '[Ошибка]: Заявок от пользователя не найдено'
                bot.send_message(chat_id, msg)

        elif action == 'delete_review':
            if not check_admin(user_id):
                return
            customer = text.replace('@', '')
            if delete_review(customer):
                msg = f'Отзывы пользователя {text} удалены'
                bot.send_message(chat_id, msg, reply_markup=admin_menu)
            else:
                msg = '[Ошибка]: Отзывов от пользователя не найдено'
                bot.send_message(chat_id, msg)

        elif action == 'project_edit':
            if not check_admin(user_id):
                return
            project = get_project_by_name(text)
            if project:
                id = project[0]
                name = project[1]
                price = project[2]
                customer = project[3]
                status = project[4]
                date = project[5]
                time = project[6]
                msg = f"""Информация о проекте ID {id}
Название: {name}
Статус: {status}
Заказчик: {customer}
Дата: {date} {time}
Цена: {price}
"""
                user_set_select(user_id, int(id))
                bot.send_message(chat_id, msg, reply_markup=project_edit)
            else:
                msg = 'Проект с таким именем не найден'
                bot.send_message(chat_id, msg)

        # редактирование проекта
        elif action == 'edit_proj_name':
            if not check_admin(user_id):
                return
            try:
                edit_project('name', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)

        elif action == 'edit_proj_status':
            if not check_admin(user_id):
                return
            try:
                edit_project('status', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
        
        elif action == 'edit_proj_price':
            if not check_admin(user_id):
                return
            try:
                edit_project('price', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)

        elif action == 'edit_proj_customer':
            if not check_admin(user_id):
                return
            try:
                edit_project('customer', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)

        elif action == 'edit_proj_date':
            if not check_admin(user_id):
                return
            try:
                edit_project('date', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)

        elif action == 'edit_proj_time':
            if not check_admin(user_id):
                return
            try:
                edit_project('time', proj_select, text)
                msg = 'Проект успешно отредактирован👌🏻'
                bot.send_message(chat_id, msg, reply_markup=project_edit)
                user_set_action(user_id, 'project_edit')
            except Exception as e:
                msg = f'Возникла ошибка, зовем алекса 💀\n{e}'
                bot.send_message(chat_id, msg, reply_markup=project_edit)


try:
    bot.polling(none_stop=True, interval=0, timeout=20)
except (urllib3.exceptions.ConnectionError,
        urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.ConnectTimeoutError) as e:
    print("Произошла ошибка соединения или превышено время ожидания:", e)
    time.sleep(3)
except requests.exceptions.ReadTimeout as e:
    print("Произошла ошибка при чтении ответа:", e)
    time.sleep(3)
except urllib3.exceptions.HTTPError as e:
    print("Произошла ошибка HTTP:", e)
    time.sleep(3)

"""except Exception as e:
    print(f"Error: {e}")
    time.sleep(15)  # Задержка перед повторной попыткой"""
