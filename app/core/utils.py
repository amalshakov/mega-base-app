from transliterate import translit

from core.log import get_logger
from .regex import validate_email

logger = get_logger()

def sort_users_by_uploads(users: list[dict[str, int]]):
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
    if len(full_name.strip().split()) == 3 and full_name.replace(" ", "").isalpha():
        logger.info(f"В графу ФИО пользователь ввел: '{full_name}'. Принято.")
        latin_full_name = translit(full_name, "ru", reversed=True)
        surname, name, patronymic = latin_full_name.replace("'", "").strip().lower().split()
    else:
        print("Ошибка! Введите ФИО в формате: Фамилия Имя Отчество. Например: Иванов Иван Иванович")
        logger.info(f"В графу ФИО пользователь ввел: '{full_name}'. Отклонено.")
        return False
    current_email = f"{name}.{surname}@megafon.ru"
    return validate_email(current_email, surname, name, patronymic)
