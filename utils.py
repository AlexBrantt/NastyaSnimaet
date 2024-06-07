import logging


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
