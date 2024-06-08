import logging
from db_module import get_project_by_id
from messages import messages_dict


def project_info(id):
    project = get_project_by_id(id)
    if project:
        id = project[0]
        name = project[1]
        price = project[2] if project[2] else messages_dict['empty_value']
        customer = project[3] if project[3] else messages_dict['empty_value']
        status = project[4] if project[4] else messages_dict['empty_value']
        date = project[5] if project[5] else messages_dict['empty_value']
        time = project[6] if project[6] else messages_dict['empty_value']
        team = project[7] if project[7] else messages_dict['empty_value']
        info = f"""Информация о проекте ID {id}
Название: {name}
Статус: {status}
Заказчик: {customer}
Команда: {team}
Дата: {date} {time}
Цена: {price}
"""
        return info

def read_text_file(file_path):
    """Возвращает содержимое текстового файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        err_msg = f"Файл {file_path} не найден."
        logging.error(err_msg)
        return None
    except Exception as e:
        err_msg = f"Произошла ошибка при чтении файла: {e}"
        logging.error(err_msg)
        return None


def write_text_file(file_path, content):
    """Перезаписывает содержимое текстового файла"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Содержимое успешно записано в файл {file_path}.")
    except Exception as e:
        err_msg = f"Произошла ошибка при записи в файл: {e}"
        logging.error(err_msg)
