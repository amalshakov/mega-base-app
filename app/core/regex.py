import re

from core.log import get_logger

logger = get_logger()

valid_email = [
    "zina.sidorova@megafon.ru",
    "denis.dyatlov@megafon.ru",
    "denis.petrov@megafon.ru",
    "oleg.ivanov@megafon.ru",
    "oleg.pe.ivanov@megafon.ru",
]

invalid_email = [
    "petr4.fedorov@megafon.ru",
    "Alex.petrov@megafon.ru",
    "даша.борисова@megafon.ru",
]


def validate_email(
        email: str,
        surname: str,
        name: str,
        patronymic: str,
):
    pattern = r"^[a-z]+\.[a-z]+@megafon\.ru$"

    if re.match(pattern, email):
        if email in valid_email:
            new_email = f"{name}.{patronymic[:2]}.{surname}@megafon.ru"
            if new_email in valid_email:
                print(f"Ваши email'ы '{email}' и '{new_email}' УЖЕ заняты! Обратитесь к администратору!")
                logger.info(f"Не получилось сформировать email для ФИО: '{surname} {name} {patronymic}'. Данные email'ы уже заняты: '{email}' и '{new_email}'")
                return False
            valid_email.append(new_email)
            print(f"Данный email '{email}' уже занят!")
            print(f"Ваш email будет такой '{new_email}', валиден. Добавлен в массив valid_email.")
            logger.info(f"Сформирован email '{new_email}' для ФИО: '{surname} {name} {patronymic}'. Email '{email}' занят!")
            return new_email
        valid_email.append(email)
        print(f"Ваш email '{email}' валиден. Добавлен в массив valid_email.")
        logger.info(f"Сформирован email '{email}' для ФИО: '{surname} {name} {patronymic}'.")
        return email
    else:
        invalid_email.append(email)
        print(f"Ваш email '{email}' не валиден! Добавлен в массив invalid_email.")
        logger.info(f"Сформированый email '{email}' для ФИО: '{surname} {name} {patronymic}' не валиден.")
        return False
