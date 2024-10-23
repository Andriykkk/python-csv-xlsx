import csv
from faker import Faker
import random

fake = Faker(locale="uk_UA")

male_patr = [
    "Анатолійович",
    "Борисович",
    "Васильович",
    "Геннадійович",
    "Дмитрович",
    "Євгенович",
    "Зіновійович",
    "Ігоревич",
    "Леонідович",
    "Миколайович",
    "Олександрович",
    "Петрович",
    "Русланович",
    "Сергійович",
    "Тарасович",
    "Ульянович",
    "Федорович",
    "Ярославович",
    "Артемович",
    "Володимирович",
]

female_patr = [
    "Анатоліївна",
    "Борисівна",
    "Василівна",
    "Геннадіївна",
    "Дмитрівна",
    "Євгенівна",
    "Зіновіївна",
    "Ігорівна",
    "Леонідівна",
    "Миколаївна",
    "Олександрівна",
    "Петрівна",
    "Русланівна",
    "Сергіївна",
    "Тарасівна",
    "Ульянівна",
    "Федорівна",
    "Ярославівна",
    "Артемівна",
    "Володимирівна",
]


def generate_employees(num):
    employees = []

    for i in range(num):
        gender = random.choices(["male", "female"], weights=[60, 40])[0]
        if gender == "male":
            first_name = fake.first_name_male()
            patronymic = random.choice(male_patr)
        else:
            first_name = fake.first_name_female()
            patronymic = random.choice(female_patr)

        employee = {
            "Прізвище": fake.last_name(),
            "Ім’я": first_name,
            "По батькові": patronymic,
            "Стать": gender,
            "Дата народження": fake.date_of_birth(minimum_age=15, maximum_age=85),
            "Посада": fake.job(),
            "Місто проживання": fake.city(),
            "Адреса проживання": fake.address().replace("\n", ", "),
            "Телефон": fake.phone_number(),
            "Email": fake.email(),
        }
        employees.append(employee)

    return employees


def write_to_csv(employees):
    with open("employees.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = employees[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for employee in employees:
            writer.writerow(employee)


if __name__ == "__main__":
    employees = generate_employees(2000)
    write_to_csv(employees)
    print(f"{len(employees)} employees generated.")
