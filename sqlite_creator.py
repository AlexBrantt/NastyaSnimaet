import sqlite3

# Если в текущей директории нет файла db.sqlite - 
# он будет создан; одновременно будет создано и соединение с базой данных.
# Если файл существует, метод connect просто подключится к базе.
con = sqlite3.connect('db.sqlite')

# Создаём специальный объект cursor для работы с БД.
# Вся дальнейшая работа будет вестись через методы этого объекта.
cur = con.cursor()

# Готовим SQL-запросы.
# Для читаемости запрос обрамлён в тройные кавычки и разбит построчно.
query_review = '''
CREATE TABLE IF NOT EXISTS review (id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER REFERENCES user (id), date TEXT NOT NULL, review_text TEXT NOT NULL);
'''
query_user = '''
CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, username TEXT, first_name TEXT, last_name TEXT, date_joined TEXT NOT NULL, last_interaction TEXT, status TEXT DEFAULT user);
'''

query_work_schedule = '''
CREATE TABLE IF NOT EXISTS work_schedule (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, customer TEXT);
'''

query_project = '''
CREATE TABLE IF NOT EXISTS project (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price INTEGER, customer TEXT, status TEXT DEFAULT заказ, date TEXT, time TEXT);
'''


query1= '''
CREATE TABLE IF NOT EXISTS coupon (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL, value TEXT);
'''
# ОЧИСТКА БД
query_full_clear_db = '''
    DELETE FROM review;
    DELETE FROM orders;
    DELETE FROM user;
    DELETE FROM project;
    DELETE FROM coupon;
    DELETE FROM sqlite_sequence WHERE name = 'review';
    DELETE FROM sqlite_sequence WHERE name = 'orders';
    DELETE FROM sqlite_sequence WHERE name = 'user';
    DELETE FROM sqlite_sequence WHERE name = 'project';
    DELETE FROM sqlite_sequence WHERE name = 'coupon';
'''

query = '''
INSERT INTO settings (key, value) VALUES ('autocoupon_value', '20%');
'''
# Применяем запросы.
# cur.execute()
#con.commit()
# весь скрипт применить...
cur.executescript(query_full_clear_db)
# Закрываем соединение с БД.
con.close()