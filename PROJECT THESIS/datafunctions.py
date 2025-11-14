# Import necessary modules for CSV handling, file operations, date, and GUI messages
import csv
import os
from datetime import date
from tkinter import messagebox

# Get the directory path of the current file for relative file access
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load food data from foods.csv and return as dictionary (food name: protein per 100g)
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


# Add a new log entry to logs.csv with food, amount, and protein data
# Automatically writes CSV header if file is empty or doesn't exist
def add_log(food, amount, protein):
    needs_header = True
    try:
        with open("logs.csv", "r", newline='') as f:
            # Try to read as CSV to check if header exists
            reader = csv.DictReader(f)
            # If file has content and can read header, we don't need to write it
            if reader.fieldnames == ['Date', 'Food', 'Amount', 'Protein']:
                needs_header = False
    except (FileNotFoundError, csv.Error):
        # File doesn't exist or is corrupted/empty, need to write header
        needs_header = True

    # Append new log entry to logs.csv (creates file if it doesn't exist)
    with open("logs.csv", "a", newline='') as f:
        fieldnames = ['Date', 'Food', 'Amount', 'Protein']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if needs_header:
            writer.writeheader()
        writer.writerow({'Date': str(date.today()), 'Food': food, 'Amount': amount, 'Protein': protein})


# Calculate and return total protein intake for today from logs.csv
def total_today():
    total = 0
    try:
        with open("logs.csv", newline='') as f:
            reader = csv.DictReader(f)
            # Sum all protein values for entries matching today's date
            for row in reader:
                if row.get('Date') == str(date.today()):
                    total += float(row['Protein'])
    except FileNotFoundError:
        return 0
    return round(total, 2)





