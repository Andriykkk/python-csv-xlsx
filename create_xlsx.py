import csv
from datetime import datetime
from openpyxl import Workbook
from utils import calculate_age


def create_xlsx(csv_file, xlsx_file):
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            employees = [row for row in reader]

            wb = Workbook()
            ws_all = wb.active
            ws_all.title = "all"

            headers = ["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"]
            ws_all.append(headers)

            index = 0
            for employee in employees:
                birthday = datetime.strptime(employee["Дата народження"], "%Y-%m-%d")
                age = calculate_age(birthday)

                ws_all.append(
                    [
                        index,
                        employee["Прізвище"],
                        employee["Ім’я"],
                        employee["По батькові"],
                        employee["Дата народження"],
                        age,
                    ]
                )
                index += 1

            categories = {"younger_18": [], "18-45": [], "45-70": [], "older_70": []}

            for employee in employees:
                birth_date = datetime.strptime(employee["Дата народження"], "%Y-%m-%d")
                age = calculate_age(birth_date)
                employee["Вік"] = age
                if age < 18:
                    categories["younger_18"].append(employee)
                elif 18 <= age <= 45:
                    categories["18-45"].append(employee)
                elif 45 < age <= 70:
                    categories["45-70"].append(employee)
                else:
                    categories["older_70"].append(employee)

            for category in categories:
                ws = wb.create_sheet(category)
                ws.append(headers)
                index = 0
                for employee in categories[category]:
                    ws.append(
                        [
                            index,
                            employee["Прізвище"],
                            employee["Ім’я"],
                            employee["По батькові"],
                            employee["Дата народження"],
                            employee["Вік"],
                        ]
                    )
                    index += 1
            wb.save(xlsx_file)
    except FileNotFoundError:
        print("Проблеми при відкритті файлу CSV.")
    except Exception as e:
        print(f"Неможливо створити XLSX файл: {e}")


if __name__ == "__main__":
    create_xlsx("employees.csv", "employees.xlsx")
