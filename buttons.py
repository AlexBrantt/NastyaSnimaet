"""Модель хранящая кнопки."""

from telebot import types

from db_module import get_projects

from messages import project_statuses, price_list

buttons_name = {
    'price': 'Прайс ❤️',
    'works': 'Работы 🎥',
    'check_date': 'Проверить дату 📆',
    'user_project': 'Мои проекты 📗',
    'stage': 'Стадия монтажа 🔍',
    'coupone': 'Купоны 🎁',
    'order': 'Записаться 📝',
    'review': 'Оставить отзыв 💌',
    'cancel': 'Отмена',
    'send_order': 'Молча отправить✅',
    'admin': 'Админка 📱',
    'projects_menu': 'Проекты 📗',
    'add_proj': 'Добавить проект 📥',
    'get_orders': 'Заявки 📝',
    'get_reviews': 'Отзывы 🥰',
    'get_projects_billing': 'Выручка 💵',
    'edit_price': 'Редактор прайса 🔖',
    'menu_coupon': 'Купоны ✨',
    'give_coupon': 'Выдать купон 🎁',
    'delete_coupon': 'Забрать купон 😈',
    'admin_users_menu': 'Пользователи 👥',
    'admin_user_info': 'Карточка пользователя 👤',
    'ban_user': 'Забанить 🚷',
    'unban_user': 'Разбанить ✳️',
    'delete': 'Удалить ❌',
    'delete_order': 'Удаление заявки ❌',
    'delete_review': 'Удаление отзыва ❌',
    'cancel_admin': 'Hазад',
    'edit_proj_name': 'Изменить название 📝',
    'edit_proj_price': 'Изменить цену 💵',
    'edit_proj_customer': 'Изменить заказчика 👤',
    'edit_proj_status': 'Изменить статус 📌',
    'edit_proj_date': 'Изменить дату 📆',
    'edit_proj_time': 'Изменить время ⏰',
    'cancel_edit_proj': 'Назад',
    'delete_proj': 'Удалить проект 🛑',
    'confirm_delete_proj': 'Точно удалить ❌',
    'settings': 'Настройки ⚙️',
    'autocoupon_periodicity': 'Интервал автокупона 🤖',
    'autocoupon_value': 'Скидка автокупона 🛍',
    'send_all': 'Рассылка ✉️',
    'send_all_confirm': 'Подтверждаю рассылку ✅'
}


# Главное меню для пользователя
main_menu_user = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_user.add(types.KeyboardButton(buttons_name['price']),
                   types.KeyboardButton(buttons_name['works']),
                   types.KeyboardButton(buttons_name['check_date']),
                   types.KeyboardButton(buttons_name['user_project']),
                   types.KeyboardButton(buttons_name['order']),
                   types.KeyboardButton(buttons_name['review']),
                   )

# Главное меню с кнопкой админки
main_menu_admin = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_admin.add(types.KeyboardButton(buttons_name['price']),
                    types.KeyboardButton(buttons_name['works']),
                    types.KeyboardButton(buttons_name['check_date']),
                    types.KeyboardButton(buttons_name['user_project']),
                    types.KeyboardButton(buttons_name['order']),
                    types.KeyboardButton(buttons_name['review']),
                    types.KeyboardButton(buttons_name['admin']),
                    )

# Меню отмены ведущее в гл меню
cancel_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_menu.add(types.KeyboardButton(buttons_name['cancel']))

# Меню разделов прайса
price_menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
price_menu.add(types.KeyboardButton(buttons_name['cancel']))
buttons_price = [types.KeyboardButton(price) for price in price_list]
price_menu.add(*buttons_price)

# Меню проектов пользователя
user_project_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
user_project_menu.add(types.KeyboardButton(buttons_name['stage']),
                      types.KeyboardButton(buttons_name['coupone']),
                      types.KeyboardButton(buttons_name['cancel']),
                      )

# Пользовательское меню заказа
order_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
order_menu.add(types.KeyboardButton(buttons_name['send_order']),
               types.KeyboardButton(buttons_name['cancel']))

# Админ меню
admin_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
admin_menu.add(types.KeyboardButton(buttons_name['projects_menu']),
               types.KeyboardButton(buttons_name['add_proj']),
               types.KeyboardButton(buttons_name['get_projects_billing']),
               types.KeyboardButton(buttons_name['menu_coupon']),
               types.KeyboardButton(buttons_name['get_orders']),
               types.KeyboardButton(buttons_name['get_reviews']),
               types.KeyboardButton(buttons_name['admin_users_menu']),
               types.KeyboardButton(buttons_name['settings']),
               types.KeyboardButton(buttons_name['send_all']),
               types.KeyboardButton(buttons_name['cancel']))

# Кнопка отмены в админке
cancel_menu_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_menu_admin.add(types.KeyboardButton(buttons_name['cancel_admin']))

# Меню пользователей в админке
menu_users_admin = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menu_users_admin.add(
    types.KeyboardButton(buttons_name['admin_user_info']),
    types.KeyboardButton(buttons_name['ban_user']),
    types.KeyboardButton(buttons_name['unban_user']),
    types.KeyboardButton(buttons_name['cancel_admin'])
    )

# Меню купонов в админке
menu_coupon = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
menu_coupon.add(
    types.KeyboardButton(buttons_name['give_coupon']),
    types.KeyboardButton(buttons_name['delete_coupon']),
    types.KeyboardButton(buttons_name['cancel_admin'])
    )

# Меню удаления заявок
order_menu_delete = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
order_menu_delete.add(types.KeyboardButton(buttons_name['delete_order']),
               types.KeyboardButton(buttons_name['cancel_admin']))

# Меню выбора удаления заявок или отзывов от пользователя
review_menu_delete = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
review_menu_delete.add(types.KeyboardButton(buttons_name['delete_review']),
                types.KeyboardButton(buttons_name['cancel_admin']))


# Меню список проектов
def get_project_menu():
    """Функция, пересобирает меню каждый раз, возвращает актуальный список."""
    projects_menu = types.ReplyKeyboardMarkup(row_width=1,
                                              resize_keyboard=True)
    projects = get_projects()
    cancel = types.KeyboardButton(buttons_name['cancel_admin'])
    buttons_projects = [types.KeyboardButton(project[1]) for project in projects]
    all_buttons = [cancel] + buttons_projects
    projects_menu.add(*all_buttons)
    return projects_menu


# Меню редактирования проекта
project_edit = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
project_edit.add(types.KeyboardButton(buttons_name['cancel_edit_proj']))
project_edit.add(types.KeyboardButton(buttons_name['edit_proj_status']),
                 types.KeyboardButton(buttons_name['edit_proj_name']),
                 types.KeyboardButton(buttons_name['edit_proj_customer']),
                 types.KeyboardButton(buttons_name['edit_proj_price']),
                 types.KeyboardButton(buttons_name['edit_proj_date']),
                 types.KeyboardButton(buttons_name['edit_proj_time']),
                 types.KeyboardButton(buttons_name['delete_proj']),
                 )

# Меню подтверждения удаления
delete_confirm_menu = types.ReplyKeyboardMarkup(row_width=1,
                                                resize_keyboard=True)
delete_confirm_menu.add(
    types.KeyboardButton(buttons_name['cancel_edit_proj']),
    types.KeyboardButton(buttons_name['confirm_delete_proj']))

# Меню выбора статуса в редактировании проекта
status_select_menu = types.ReplyKeyboardMarkup(row_width=3,
                                               resize_keyboard=True)
cancel = types.KeyboardButton(buttons_name['cancel_edit_proj'])
buttons_status = [types.KeyboardButton(status) for status in project_statuses]
status_select_menu.add(cancel)
status_select_menu.add(*buttons_status)

# Меню выхода с редактирования проекта
cancel_edit_proj = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_edit_proj.add(types.KeyboardButton(buttons_name['cancel_edit_proj']))


settings_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
settings_menu.add(
    types.KeyboardButton(buttons_name['autocoupon_periodicity']),
    types.KeyboardButton(buttons_name['autocoupon_value']),
    types.KeyboardButton(buttons_name['edit_price']),
    types.KeyboardButton(buttons_name['cancel_admin']),
    )

send_all_confirm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
send_all_confirm.add(
    types.KeyboardButton(buttons_name['send_all_confirm']),
    types.KeyboardButton(buttons_name['cancel_admin']),
)