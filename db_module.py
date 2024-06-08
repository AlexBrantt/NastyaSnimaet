"""Модуль бд."""

import sqlite3
import logging
from messages import project_statuses


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
        logging.error("Ошибка при вставке данных пользователя:", e)
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


def user_set_select(user_id, select):
    """Устанавлиет текущее действие пользователю."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE user SET select_item = ? WHERE user_id = ?", (select, user_id))
    con.commit()
    con.close()


def user_get_select(user_id):
    """Получает текущее действие пользователя."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT select_item FROM user WHERE user_id = ?", (user_id,))
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
    # logging.info(f'Установлен статус: {status}')


def update_last_interaction(user_id, last_iteraion):
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE user SET last_interaction = ? WHERE user_id = ?", (last_iteraion, user_id))
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
    cur.execute("SELECT name,status FROM project WHERE customer = ?", (username,))
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
            date, time, team)
            VALUES (?, ?, ?, ?, ?, ?);''',
            data
        )
        con.commit()
        print("Данные проекта успешно вставлены в базу данных.")
    except sqlite3.Error as e:
        logging.error("Ошибка при вставке данных проекта:", e)
    finally:
        con.close()


def get_projects():
    """Получает проекты."""
    con = db_connect()
    cur = con.cursor()
    last_status = project_statuses[-1]
    query = "SELECT * FROM project WHERE status != ?"
    cur.execute(query, (last_status,))
    result = cur.fetchall()
    con.close()
    return result


def get_projects_billing():
    """Получает доход с активных проектов."""
    con = db_connect()
    cur = con.cursor()
    last_status = project_statuses[-1]
    query = "SELECT price FROM project WHERE status != ?"
    cur.execute(query, (last_status,))
    result = cur.fetchall()
    con.close()
    billing = 0
    for price in result:
        billing += price[0]
    return billing


def get_project_by_name(name):
    """Получает проекты."""
    con = db_connect()
    cur = con.cursor()
    query = "SELECT * FROM project WHERE name = ?"
    cur.execute(query, (name,))
    result = cur.fetchone()
    con.close()
    return result


# меняем значение в столбце column по id на new_arg
def edit_project(column, id, new_arg):
    """Получает проекты."""
    print(column, id, new_arg)
    con = db_connect()
    cur = con.cursor()
    query = f"UPDATE project SET {column} = ? WHERE id = ?"
    cur.execute(query, (new_arg, id))
    con.commit()
    con.close()


def delete_project(id):
    """Удаляет проект."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("DELETE FROM project WHERE id = ?", (id,))
    con.commit()
    con.close()


def review_add(data):
    """Добавляение отзыва в бд."""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO review (username, date, text)
            VALUES (?, ?, ?);''',
            data
        )
        con.commit()
        print("Отзыв успешно вставлен в базу данных.")
    except sqlite3.Error as e:
        logging.error("Ошибка при отправке отзыва:", e)
    finally:
        con.close()


def get_reviews():
    """Получает отзывы."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT username, text FROM review")
    result = cur.fetchall()
    con.close()
    return result


def order_add(data):
    """Добавляение заказа в бд."""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO orders (username, date, text)
            VALUES (?, ?, ?);''',
            data
        )
        con.commit()
        print("Данные заказа успешно вставлены в базу данных.")
    except sqlite3.Error as e:
        logging.error("Ошибка при вставке данных заказа:", e)
    finally:
        con.close()


def get_orders():
    """Получает отзывы."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT username, text FROM orders")
    result = cur.fetchall()
    con.close()
    return result


def delete_review(username):
    """Удаляет отзывы пользователя."""
    username = username.replace('@', '')
    get = check_user_reviews(username)

    if get:
        con = db_connect()
        cur = con.cursor()
        cur.execute("DELETE FROM review WHERE username = ?", (username,))
        con.commit()
        con.close()
        return True
    return False


def delete_order(username):
    """Удаляет заявки пользователя."""
    username = username.replace('@', '')
    get = check_user_orders(username)

    if get:
        con = db_connect()
        cur = con.cursor()
        cur.execute("DELETE FROM orders WHERE username = ?", (username,))
        con.commit()
        con.close()
        return True
    return False


def check_user_orders(username):
    """Получает отзывы."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT id FROM orders WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result


def check_user_reviews(username):
    """Получает отзывы."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT id FROM review WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result


def give_coupon(data):
    """Выдает купон"""
    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(
            '''INSERT INTO coupon (owner, value)
            VALUES (?, ?);''',
            data
        )
        con.commit()
        logging.info("Купон внесен в базу.")
    except sqlite3.Error as e:
        logging.error("Ошибка при вставке данных пользователя:", e)
    finally:
        con.close()


def get_user_coupone(username):
    """Получает все купоны для пользователя, если значение team содержится в owner."""
    con = db_connect()
    cur = con.cursor()
    # Получаем все team из таблицы project по имени пользователя
    cur.execute("SELECT DISTINCT team FROM project WHERE customer = ?", (username,))
    team_results = cur.fetchall()

    if not team_results:
        con.close()
        return None
    
    all_coupons = []
    seen_coupons = set()
    # Проходим по всем найденным team и ищем купоны для каждой из них
    for team_result in team_results:
        team = team_result[0]
        if team is None:
            continue

        # Получаем все записи из таблицы coupon, если team содержится в owner
        cur.execute("SELECT * FROM coupon WHERE owner LIKE ?", ('%' + team + '%',))
        coupons = cur.fetchall()

        for coupon in coupons:
            if coupon not in seen_coupons:
                seen_coupons.add(coupon)
                all_coupons.append(coupon)
    con.close()

    return all_coupons if all_coupons else None

# ОТЛАДКА
def clear_users_db():
    """Очистить таблицу пользователей в бд."""
    con = db_connect()
    cur = con.cursor()
    cur.execute("DELETE FROM user")
    con.commit()
    con.close()
