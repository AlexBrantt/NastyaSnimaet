"""Главный модуль бота."""

import datetime
import shlex
import time
import urllib3
import requests
import os
import logging
from logging.handlers import RotatingFileHandler
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
                       user_set_select, update_last_interaction,
                       get_projects_billing, give_coupon,
                       get_user_coupone, get_all_cupone,
                       delete_coupon, get_user_by_username,
                       user_set_status_by_username, auto_give_cupone,
                       settings_get, settings_update,
                       get_users_id,
                       )

from buttons import (get_project_menu, buttons_name,
                     main_menu_admin, main_menu_user,
                     cancel_menu, order_menu,
                     admin_menu, cancel_menu_admin,
                     project_edit, cancel_edit_proj,
                     delete_confirm_menu, status_select_menu,
                     price_menu, user_project_menu,
                     menu_coupon, order_menu,
                     review_menu, menu_users_admin,
                     settings_menu)

from validators import date_validator, coupone_add_validator

from messages import messages_dict, price_list

from utils import read_text_file, write_text_file

load_dotenv()

TOKEN = os.getenv('TOKEN')
NASTYA_ID = os.getenv('NASTYA_ID')
ALEX = os.getenv('ALEX_ID')
DEBUG_ADMIN = 'root'

default_timezone = pytz.timezone('Europe/Kaliningrad')
datetime.datetime.now(default_timezone)

bot = telebot.TeleBot(TOKEN)

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
# Создаем обработчик для записи в файл
file_handler = RotatingFileHandler("app.log", maxBytes=10*1024*1024,
                                   backupCount=5, encoding='utf-8')
"""
maxBytes- максимальный размер файла (в байтах), при котором произойдет ротация
backupCount- количество файлов логов, которые будут сохранены после ротации
"""
file_handler.setFormatter(formatter)
# Настраиваем логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


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


def send_all():
    logging.info('[Рассылка]: Рассылка запущена')
    users_id = get_users_id()
    for index, id in enumerate(users_id):
        chat_id = id[0]
        bot.send_message(chat_id, 'Тест')
        logging.info(f'[Рассылка]: {index}-е сообщение доставлено')
        if index % 5 == 0:
            logging.info('[Рассылка]: Пауза')
            time.sleep(1)
    logging.info('[Рассылка]: Рассылка завершена')

# send_all()
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
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    last_interaction = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    update_last_interaction(user_id, last_interaction)
    action = user_get_action(user_id)
    logging.info(f'{username}: {text}')

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
                         reply_markup=price_menu)

    # Отправить прайс с кнопки
    elif text in price_list and action == 'menu':
        price = read_text_file(price_list[text])
        bot.send_message(chat_id, price)

    # Команда Посмотреть работы
    elif text == buttons_name['works']:
        bot.send_message(chat_id, messages_dict['works'],
                         reply_markup=main_menu)

    # Команда посмотреть свободна ли дата
    elif text == buttons_name['check_date']:
        bot.send_message(chat_id, messages_dict['check_date'],
                         reply_markup=cancel_menu)
        user_set_action(user_id, 'check_date')

    elif text == buttons_name['user_project']:
        bot.send_message(chat_id, 'Меню проектов',
                         reply_markup=user_project_menu)

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

    elif text == buttons_name['coupone']:
        coupons = get_user_coupone(username)
        if coupons:
            msg = '\n\n'.join([f'Купон для команды {coupon[1]}\nНа {coupon[2]}' for coupon in coupons])
        else:
            msg = 'Купоны не найдены.'
        bot.send_message(chat_id, msg)

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
                         reply_markup=cancel_menu_admin)
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
        bot.send_message(chat_id, msg, reply_markup=order_menu)

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
        bot.send_message(chat_id, msg, reply_markup=review_menu)
     
    elif text == buttons_name['get_projects_billing']:
        if not check_admin(user_id):
            return
        billing = get_projects_billing()
        msg = f'Выручка: {billing}'
        bot.send_message(chat_id, msg)

    elif text == buttons_name['edit_price']:
        if not check_admin(user_id):
            return
        msg = 'Выберите редактируемый прайс'
        bot.send_message(chat_id, msg, reply_markup=price_menu)
        user_set_action(user_id, 'select_edit_price')

    elif text == buttons_name['menu_coupon']:
        if not check_admin(user_id):
            return
        coupons = get_all_cupone()
        if coupons:
            msg = '\n\n'.join(
                [f'КУПОН №{coupon[0]}\nКоманда: {coupon[1]}\nНа {coupon[2]}' for coupon in coupons]
                )
        else:
            msg = 'Купоны не найдены.'
        bot.send_message(chat_id, msg, reply_markup=menu_coupon)

    elif text == buttons_name['give_coupon']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['give_coupon'],
                         reply_markup=cancel_menu_admin)
        user_set_action(user_id, 'give_coupon')

    elif text == buttons_name['delete_coupon']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, messages_dict['delete_coupon'],
                         reply_markup=cancel_menu_admin)
        user_set_action(user_id, 'delete_coupon')

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

    elif text == buttons_name['admin_users_menu']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Управление пользователями',
                         reply_markup=menu_users_admin)
    
    elif text == buttons_name['admin_user_info']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Введите логин пользователя',
                         reply_markup=menu_users_admin)
        user_set_action(user_id, 'admin_user_info')

    elif text == buttons_name['ban_user']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, '[БАН⚠️]: Введите логин пользователя',
                         reply_markup=menu_users_admin)
        user_set_action(user_id, 'ban_user')

    elif text == buttons_name['unban_user']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, '[Разбан]: Введите логин пользователя',
                         reply_markup=menu_users_admin)
        user_set_action(user_id, 'unban_user')

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
                         reply_markup=status_select_menu)
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

    elif text == buttons_name['settings']:
        if not check_admin(user_id):
            return
        bot.send_message(chat_id, 'Настройки',
                         reply_markup=settings_menu)
        
    elif text == buttons_name['autocoupon_periodicity']:
        if not check_admin(user_id):
            return
        interval = settings_get('autocoupon_periodicity')
        msg = f"""Интервал автокупона, каждый {interval[0]}-й проект
Для изменения введите новое значение
        """
        bot.send_message(chat_id, msg, reply_markup=settings_menu)
        user_set_action(user_id, 'autocoupon_periodicity')
       
    elif text == buttons_name['autocoupon_value']:
        if not check_admin(user_id):
            return
        value = settings_get('autocoupon_value')
        msg = f"""Скидка автокупона: {value[0]}
Для изменения ведите новое значение"""
        bot.send_message(chat_id, msg, reply_markup=settings_menu)
        user_set_action(user_id, 'autocoupon_value')


    # Обработка текста вне кнопок
    else:
        proj_select = user_get_select(user_id)

        # Обработка ввода для добавления проекта
        if action == 'admin_add_project':
            if not check_admin(user_id):
                return
            try:
                parts = shlex.split(text)
                project_name = parts[0].strip("'")
                team = parts[1].strip("'") if len(parts) > 1 else None
                customer = parts[2] if len(parts) > 2 else None
                price = int(parts[3]) if len(parts) > 3 else None
                date = parts[4] if len(parts) > 4 else None
                time_range = parts[5] if len(parts) > 5 else None

                valid_date = date_validator(date)
                if valid_date:
                    data = (
                            project_name,
                            price,
                            customer.replace('@', '') if customer is not None else None,
                            valid_date,
                            time_range,
                            team,
                        )
                    project_create(data)
                    user_set_action(user_id, 'menu')
                    bot.send_message(chat_id, messages_dict['proj_added'],
                                     reply_markup=admin_menu)
                    if auto_give_cupone(team):
                        msg = f'Автоматически был выдан купон команде -  {team}'
                        bot.send_message(chat_id, msg)
                else:
                    bot.send_message(chat_id, messages_dict['check_date_error'])
            except IndexError:
                err_msg = "Ошибка: недостаточно аргументов в введенной строке."
                bot.send_message(chat_id, err_msg)
                logging.info(f'{user_id}: {err_msg}')
            except ValueError:
                bot.send_message(chat_id, messages_dict['proj_error'])
                logging.info(f"{user_id}: {messages_dict['proj_error']}")

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
                team = project[7]
                msg = f"""Информация о проекте ID {id}
Название: {name}
Статус: {status}
Заказчик: {customer}
Команда: {team}
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

        elif action == 'edit_price':
            if not check_admin(user_id):
                return
            select = user_get_select(user_id)
            file_path = price_list[select]
            write_text_file(file_path, text)
            bot.send_message(chat_id, 'Изменено)', reply_markup=admin_menu)
            user_set_action(user_id, 'menu')

        elif action == 'select_edit_price':
            if not check_admin(user_id):
                return
            if text in price_list:
                user_set_select(user_id, text)
                user_set_action(user_id, 'edit_price')
                msg = 'Введите новый прайс'
                bot.send_message(chat_id, msg, reply_markup=cancel_menu_admin)
            else:
                msg = 'Введите коректный раздел прайса!'
                bot.send_message(chat_id, msg, reply_markup=project_edit)

        elif action == 'give_coupon':
            if not check_admin(user_id):
                return
            try:
                coupone_add_validator(text)
                parts = shlex.split(text)
                team = parts[0].strip("'")
                value = parts[1]if len(parts) > 1 else None
                data = (team, value)
                give_coupon(data)
                msg = f'Купон на {value} успешно выдан команде {team}'
                bot.send_message(chat_id, msg, reply_markup=menu_coupon)
                user_set_action(user_id, 'menu')

            except ValueError:
                bot.send_message(chat_id, messages_dict['proj_error'],)
                logging.info(f"{user_id}: {err_msg}")

        elif action == 'delete_coupon':
            if not check_admin(user_id):
                return
            if text.isdigit():
                id = int(text)
                if delete_coupon(id):
                    user_set_action(user_id, 'menu')
                    bot.send_message(chat_id, f'Купон №{id} успешно удален',
                                     reply_markup=menu_coupon)
                else:
                    bot.send_message(chat_id, 'Купона с таким номер нет🥴')
            else:
                err_msg = 'Пожалуйста, введите корректный номер купона.'
                bot.send_message(chat_id, err_msg)

        elif action == 'admin_user_info':
            if not check_admin(user_id):
                return
            username = text.replace('@', '')
            user = get_user_by_username(username)
            if user:
                get_user_id = user[1]
                username = f'@{username}'
                firts_name = user[3] if user[3] else ''
                last_name = user[4] if user[4] else ''
                date_join = user[5]
                last_interaction = user[6]
                status = user[7]
                msg = f"""Пользователь {username}👤
Имя: {firts_name} {last_name}
Статус: {status}
Последняя активность: {last_interaction}
Дата регистрации: {date_join}
ID: {get_user_id}
"""
                bot.send_message(chat_id, msg)
                user_set_action(user_id, 'menu')
            else:
                msg = 'Пользователь не найден'
                bot.send_message(chat_id, msg)
        
        elif action == 'ban_user':
            if not check_admin(user_id):
                return
            username = text.replace('@', '')
            if user_set_status_by_username(username, 'banned'):
                msg = f'Пользователь @{username} успешно забанен'
                bot.send_message(chat_id, msg)
                user_set_action(user_id, 'menu')
            else:
                msg = 'Пользователь не найден'
                bot.send_message(chat_id, msg)
        
        elif action == 'unban_user':
            if not check_admin(user_id):
                return
            username = text.replace('@', '')
            if user_set_status_by_username(username, 'user'):
                msg = f'Пользователь @{username} успешно разбанен'
                bot.send_message(chat_id, msg)
                user_set_action(user_id, 'menu')
            else:
                msg = 'Пользователь не найден'
                bot.send_message(chat_id, msg)

        elif action == 'autocoupon_periodicity':
            if not check_admin(user_id):
                return
            if text.isdigit():
                settings_update('autocoupon_periodicity', text)
                user_set_action(user_id, 'menu')
                msg = f'Обновлено! Купон будет выдаваться каждый {text}-й проект'
                bot.send_message(chat_id, msg)
            else:
                bot.send_message(chat_id, 'Введите число!')

        elif action == 'autocoupon_value':
            if not check_admin(user_id):
                return
            settings_update('autocoupon_value', text)
            user_set_action(user_id, 'menu')
            msg = f'Обновлено! Новая скидка - {text}'
            bot.send_message(chat_id, msg)


try:
    bot.polling(none_stop=True, interval=0, timeout=20)
except (urllib3.exceptions.ConnectionError,
        urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.ConnectTimeoutError) as e:
    err_msg = "Произошла ошибка соединения или превышено время ожидания:"
    logging.error(err_msg, e)
    time.sleep(3)
except requests.exceptions.ReadTimeout as e:
    err_msg = "Произошла ошибка при чтении ответа:"
    logging.error(err_msg, e)
    time.sleep(3)
except requests.exceptions.ConnectionError as e:
    err_msg = "Произошла ошибка соединения:"
    logging.error(err_msg, e)
    time.sleep(3)
except urllib3.exceptions.HTTPError as e:
    err_msg = "Произошла ошибка HTTP:"
    logging.error(err_msg, e)
    time.sleep(3)

"""except Exception as e:
    print(f"Error: {e}")
    time.sleep(15)  # Задержка перед повторной попыткой"""
