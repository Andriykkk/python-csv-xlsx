import csv
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from utils import calculate_age


def analise_csv(csv_file):
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            male_count = 0
            female_count = 0
            age_categories = {"younger_18": 0, "18-45": 0, "45-70": 0, "older_70": 0}
            gender_age_count = defaultdict(lambda: defaultdict(int))

            for row in reader:
                age = calculate_age(
                    datetime.strptime(row["Дата народження"], "%Y-%m-%d")
                )
                if row["Стать"] == "male":
                    male_count += 1
                    gender_age_count["Ч"][age] += 1
                elif row["Стать"] == "female":
                    female_count += 1
                    gender_age_count["Ж"][age] += 1

                if age <= 18:
                    age_categories["younger_18"] += 1
                elif age <= 45:
                    age_categories["18-45"] += 1
                elif age <= 70:
                    age_categories["45-70"] += 1
                else:
                    age_categories["older_70"] += 1

            print(f"Кількість чоловіків: {male_count}")
            print(f"Кількість жінок: {female_count}")
            print("Кількість співробітників за віковими категоріями:", age_categories)

            plot_gender_distribution(male_count, female_count)
            plot_age_distribution(age_categories)
            plot_gender_age_distribution(gender_age_count)

    except FileNotFoundError:
        print(f"Файл {csv_file} не знайдено.")
    except csv.Error as e:
        print(f"Помилка читання файлу {csv_file}: {e}")


def plot_gender_distribution(male_count, female_count):
    plt.figure(figsize=(8, 4))
    plt.bar(["Чоловіки", "Жінки"], [male_count, female_count], color=["blue", "pink"])
    plt.title("Розподіл співробітників за статтю")
    plt.ylabel("Кількість")
    plt.show()


def plot_age_distribution(age_categories):
    plt.figure(figsize=(8, 4))
    plt.bar(age_categories.keys(), age_categories.values(), color="green")
    plt.title("Кількість співробітників за віковими категоріями")
    plt.ylabel("Кількість")
    plt.show()


def plot_gender_age_distribution(gender_age_count):
    categories = ["younger_18", "18-45", "45-70", "older_70"]
    male_counts = []
    female_counts = []
    for category in categories:
        male_count = 0
        for age, count in gender_age_count["Ч"].items():
            if isinstance(age, int):  # Check if age is a number
                if category == "younger_18" and age < 18:
                    male_count += count
                elif category == "18-45" and 18 <= age <= 45:
                    male_count += count
                elif category == "45-70" and 45 < age <= 70:
                    male_count += count
                elif category == "older_70" and age > 70:
                    male_count += count
        male_counts.append(male_count)

        female_count = 0
        for age, count in gender_age_count["Ж"].items():
            if isinstance(age, int):  # Check if age is a number
                if category == "younger_18" and age < 18:
                    female_count += count
                elif category == "18-45" and 18 <= age <= 45:
                    female_count += count
                elif category == "45-70" and 45 < age <= 70:
                    female_count += count
                elif category == "older_70" and age > 70:
                    female_count += count
        female_counts.append(female_count)

    width = 0.35
    x = range(len(categories))

    plt.figure(figsize=(10, 5))
    plt.bar(x, male_counts, width=width, label="Чоловіки", color="blue")
    plt.bar(
        [i + width for i in x], female_counts, width=width, label="Жінки", color="pink"
    )

    plt.title("Розподіл статі по вікових категоріях")
    plt.xticks([i + width / 2 for i in x], categories)
    plt.ylabel("Кількість")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    csv_filename = "employees.csv"
    analise_csv(csv_filename)
    print("Ok")
