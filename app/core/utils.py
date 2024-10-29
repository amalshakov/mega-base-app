from transliterate import translit
import re

from app.core.log import get_logger
from .regex import validate_email

logger = get_logger()

def sort_users_by_uploads(users: list[dict[str, int]]):
    """
    Сортирует список пользователей по количеству загруженных файлов.

    Пользователи сортируются в порядке убывания количества загруженных файлов.
    Если количество загруженных файлов одинаково, пользователи сортируются по имени пользователя в алфавитном порядке.
    """
    n = len(users)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (
                users[j]["number_upload_files"] < users[j + 1]["number_upload_files"] or
                (
                    users[j]["number_upload_files"] == users[j + 1]["number_upload_files"] and
                    users[j]["username"] > users[j + 1]["username"]
                )
            ):
                users[j], users[j + 1] = users[j + 1], users[j]
    return users


def sort_users_by_uploads2(users: list[dict[str, int]]):
    return sorted(users, key=lambda x: x["number_upload_files"], reverse=True)


def get_email_from_full_name(full_name: str):
    """
    Генерит адрес электронной почты на основе ФИО.

    full_name должно содержать три слова: фамилию, имя и отчество. ("Фамилия Имя Отчество")
    Если формат имени корректен, адрес электронной почты формируется в формате "name.surname@megafon.ru".
    В противном случае возвращается False и выводится сообщение об ошибке.
    """
    if len(full_name.strip().split()) == 3 and full_name.replace(" ", "").isalpha() and not re.search(r'[a-zA-Z]', full_name):
        logger.info(f"В графу ФИО пользователь ввел: '{full_name}'. Принято.")
        latin_full_name = translit(full_name, "ru", reversed=True)
        surname, name, patronymic = latin_full_name.replace("'", "").strip().lower().split()
    else:
        print("Ошибка! Введите ФИО в формате: Фамилия Имя Отчество. Например: Иванов Иван Иванович")
        logger.info(f"В графу ФИО пользователь ввел: '{full_name}'. Отклонено.")
        return False
    current_email = f"{name}.{surname}@megafon.ru"
    return validate_email(current_email, surname, name, patronymic)
