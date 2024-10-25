import re

valid_email = [
    "zina.sidorova@megafon.ru",
    "denis.dyatlov@megafon.ru"
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
) -> str:
    pattern = r"^[a-z]+\.[a-z]+@megafon\.ru$"

    if re.match(pattern, email):
        if email in valid_email:
            email = f"{name}.{patronymic[:2]}.{surname}@megafon.ru"
            if email in valid_email:
                print(f"Ваш email '{email}' УЖЕ занят. Обратитесь к администратору!")
                return email
        valid_email.append(email)
        print(f"Ваш email '{email}' валиден. Добавлен в массив valid_email.")
        return email
    else:
        invalid_email.append(email)
        print(f"Ваш email '{email}' не валиден! Добавлен в массив invalid_email.")
        return email
