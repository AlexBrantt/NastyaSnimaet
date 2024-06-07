"""Модель хранящая кнопки."""

from telebot import types

from db_module import get_projects

from messages import project_statuses

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
    'projects_menu': 'Мои проекты 📗',
    'add_proj': 'Добавить проект 📥',
    'get_orders': 'Заявки 📝',
    'get_reviews': 'Отзывы 🥰',
    'delete': 'Удалить ❌',
    'delete_menu': 'Меню удаления 🗑',
    'delete_order': 'Удаление заявки ❌',
    'delete_review': 'Удаление отзыва ❌',
    'cancel_admin': 'Hазад',
    'edit_proj_name': 'Изменить название',
    'edit_proj_price': 'Изменить цену',
    'edit_proj_customer': 'Изменить заказчика',
    'edit_proj_status': 'Изменить статус',
    'edit_proj_date': 'Изменить дату',
    'edit_proj_time': 'Изменить время',
    'cancel_edit_proj': 'Назад',
    'delete_proj': 'Удалить проект 🛑',
    'confirm_delete_proj': 'Точно удалить ❌',
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

order_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
order_menu.add(types.KeyboardButton(buttons_name['send_order']),
               types.KeyboardButton(buttons_name['cancel']))

admin_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
admin_menu.add(types.KeyboardButton(buttons_name['projects_menu']),
               types.KeyboardButton(buttons_name['add_proj']),
               types.KeyboardButton(buttons_name['get_orders']),
               types.KeyboardButton(buttons_name['get_reviews']),
               types.KeyboardButton(buttons_name['delete_menu']),
               types.KeyboardButton(buttons_name['cancel']))

cancel_menu_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_menu_admin.add(types.KeyboardButton(buttons_name['cancel_admin']))

delete_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
delete_menu.add(types.KeyboardButton(buttons_name['delete_order']),
                types.KeyboardButton(buttons_name['delete_review']),
                types.KeyboardButton(buttons_name['cancel_admin']))

delete_confirm_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
delete_confirm_menu.add(types.KeyboardButton(buttons_name['cancel_edit_proj']),
                        types.KeyboardButton(buttons_name['confirm_delete_proj']))

status_select_menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
cancel = types.KeyboardButton(buttons_name['cancel_edit_proj'])
buttons_status = [types.KeyboardButton(status) for status in project_statuses]
status_select_menu.add(cancel)
status_select_menu.add(*buttons_status)


def get_project_menu():
    projects_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    projects = get_projects()
    cancel = types.KeyboardButton(buttons_name['cancel_admin'])
    buttons_projects = [types.KeyboardButton(project[1]) for project in projects]
    all_buttons = [cancel] + buttons_projects
    projects_menu.add(*all_buttons)
    return projects_menu


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

cancel_edit_proj = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_edit_proj.add(types.KeyboardButton(buttons_name['cancel_edit_proj']))
