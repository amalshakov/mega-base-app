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


def validate_email(email: str):
    pattern = r"^[a-z]+\.[a-z]+@megafon\.ru$"

    if re.match(pattern, email):
        if email not in valid_email:
            valid_email.append(email)
            print("Ваш email валиден. Добавлен в массив valid_email.")
            print(valid_email)
        else:
            print("Ваш email валиден. Но уже существует.")
    else:
        invalid_email.append(email)
        print("Ваш email не валиден! Добавлен в массив invalid_email.")
        print(invalid_email)
