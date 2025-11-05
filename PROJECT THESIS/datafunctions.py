import csv
import os
from datetime import date
from tkinter import messagebox

# only for the path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_foods():
    foods = {}
    try:
        path = os.path.join(BASE_DIR, "foods.csv")
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                foods[row['Food']] = float(row['Protein_per_100g'])
    except FileNotFoundError:
        messagebox.showerror("Error", "foods.csv not found!")
    return foods


def add_log(food, amount, protein):
    file_exists = False
    try:
        with open("logs.csv", "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass


    with open("logs.csv", "a", newline='') as f:
        fieldnames = ['Date', 'Food', 'Amount', 'Protein']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Date': str(date.today()), 'Food': food, 'Amount': amount, 'Protein': protein})


def total_today():
    total = 0
    try:
        with open("logs.csv", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Date') == str(date.today()):
                    total += float(row['Protein'])
    except FileNotFoundError:
        return 0
    return round(total, 2)





