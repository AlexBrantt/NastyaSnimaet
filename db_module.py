"""Модуль бд."""

import sqlite3


def db_connect():
    """Подключение к бд."""
    return sqlite3.connect('db.sqlite')


def user_create(data):
    """Добавляение пользователя в бд."""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO user (user_id, username, first_name,
            last_name, date_joined, last_interaction)
            VALUES (?, ?, ?, ?, ?, ?);''',
            data
        )
        con.commit()
        print("Данные пользователя успешно вставлены в базу данных.")
    except sqlite3.Error as e:
        print("Ошибка при вставке данных пользователя:", e)
    finally:
        con.close()


def user_exist(user_id):
    """Проверяет есть ли запись о пользователе в бд."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT 1 FROM user WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    con.close()
    return result is not None


def user_set_action(user_id, action):
    """Устанавлиет текущее действие пользователю."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE user SET action = ? WHERE user_id = ?", (action, user_id))
    con.commit()
    con.close()


def user_get_action(user_id):
    """Получает текущее действие пользователя."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT action FROM user WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    con.close()
    return result[0]


def user_get_status(user_id):
    """Получает текущее действие пользователя."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT status FROM user WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    con.close()
    return result[0]


def user_set_status(user_id, status):
    """Устанавлиет текущее действие пользователю."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE user SET status = ? WHERE user_id = ?", (status, user_id))
    con.commit()
    con.close()


def check_date(date):
    """Получает текущее действие пользователя."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT time FROM project WHERE date = ?", (date,))
    result = cur.fetchall()
    con.close()
    return result


def get_status_my_proj(username):
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT name,status FROM project WHERE customer = ?", (f'@{username}',))
    result = cur.fetchall()
    con.close()
    return result


def project_create(data):
    """Добавляение проекта в бд."""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO project (name, price, customer,
            date, time)
            VALUES (?, ?, ?, ?, ?);''',
            data
        )
        con.commit()
        print("Данные проекта успешно вставлены в базу данных.")
    except sqlite3.Error as e:
        print("Ошибка при вставке данных проекта:", e)
    finally:
        con.close()


def review_add(data):
    """Добавляение проекта в бд."""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO review (username, date, text)
            VALUES (?, ?, ?);''',
            data
        )
        con.commit()
        print("Данные проекта успешно вставлены в базу данных.")
    except sqlite3.Error as e:
        print("Ошибка при вставке данных проекта:", e)
    finally:
        con.close()



# ОТЛАДКА
def clear_users_db():
    """Очистить таблицу пользователей в бд."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("DELETE FROM user")
    con.commit()
    con.close()
