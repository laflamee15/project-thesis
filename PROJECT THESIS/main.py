import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import date

# ------------------ Helper Functions ------------------
def load_foods():
    foods = {}
    try:
        with open("foods.csv", newline='') as f:
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

def calculate_protein(food, amount):
    if food in food_data:
        protein = food_data[food] * (amount / 100)
        return round(protein, 2)
    else:
        return 0

# ------------------ Main GUI ------------------
root = tk.Tk()
root.title("GainTrack - Protein Intake Tracker")
root.state("zoomed")

# Colors & Fonts
BG_COLOR = "#FF7B54"
TEXT_COLOR = "white"
FONT_TITLE = ("Arial", 28, "bold")
FONT_LABEL = ("Arial", 14)
FONT_BUTTON = ("Arial", 14, "bold")

# Load data
food_data = load_foods()
protein_goal = 0

# Style Progress Bar
style = ttk.Style()
style.theme_use('default')
style.configure("Orange.Horizontal.TProgressbar", troughcolor="#FFE8D6", background=BG_COLOR, thickness=30, bordercolor="#FFE8D6")

# ------------------ Top Section ------------------
top_frame = tk.Frame(root, bg=BG_COLOR, height=200)
top_frame.pack(fill="x")

title_label = tk.Label(top_frame, text="GainTrack", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_TITLE)
title_label.pack(pady=(30, 5))

date_label = tk.Label(top_frame, text=date.today().strftime("%B %d, %Y"), bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 16))
date_label.pack()

protein_display = tk.Label(top_frame, text="0g / 0g", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 42, "bold"))
protein_display.pack(pady=(10, 0))

# ------------------ Main Frame ------------------
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True, pady=20)

progress = ttk.Progressbar(main_frame, length=600, maximum=100, style="Orange.Horizontal.TProgressbar")
progress.pack(pady=20)

# ------------------ Profile Section (in main GUI) ------------------
profile_frame = tk.Frame(main_frame, bg="white")
profile_frame.pack(pady=10)

tk.Label(profile_frame, text="Set Your Profile", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 10))

tk.Label(profile_frame, text="Weight (kg):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
weight_entry = tk.Entry(profile_frame, width=20)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(profile_frame, text="Age:", bg="white", font=FONT_LABEL).grid(row=2, column=0, padx=10, pady=5, sticky="e")
age_entry = tk.Entry(profile_frame, width=20)
age_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(profile_frame, text="Goal:", bg="white", font=FONT_LABEL).grid(row=3, column=0, padx=10, pady=5, sticky="e")
goal_var = tk.StringVar(value="")
goal_menu = ttk.Combobox(profile_frame, textvariable=goal_var, values=["BULKING", "CUTTING", "MAINTENANCE"], width=18)
goal_menu.grid(row=3, column=1, padx=10, pady=5)

def save_profile():
    global protein_goal
    try:
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid weight.")
        return
    
    goal = goal_var.get()
    if goal == "BULKING":
        target = weight * 2.0
    elif goal == "CUTTING":
        target = weight * 2.0
    else:
        target = weight * 1.6

    protein_goal = round(target, 2)
    update_progress()
    messagebox.showinfo("Profile Saved", f"Daily Protein Goal: {protein_goal}g")

tk.Button(profile_frame, text="Save Profile", command=save_profile, bg=BG_COLOR, fg="white",
          font=FONT_BUTTON, width=18, height=1).grid(row=4, column=0, columnspan=2, pady=10)

# ------------------ Food Input ------------------
input_frame = tk.Frame(main_frame, bg="white")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Select Food:", bg="white", font=FONT_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
food_var = tk.StringVar()
food_menu = ttk.Combobox(input_frame, textvariable=food_var, values=list(load_foods().keys()), width=25)
food_menu.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Amount (grams):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
amount_entry = tk.Entry(input_frame, width=27)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

# ------------------ Buttons ------------------
def update_progress():
    today_total = total_today()
    if protein_goal > 0:
        percentage = min((today_total / protein_goal) * 100, 100)
        progress["value"] = percentage
        protein_display.config(text=f"{today_total}g / {protein_goal}g")
    else:
        protein_display.config(text=f"{today_total}g / 0g")

def log_food():
    food = food_var.get()
    if not food:
        messagebox.showwarning("Missing", "Please select a food item.")
        return
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for amount.")
        return
    
    protein = calculate_protein(food, amount)
    add_log(food, amount, protein)
    update_progress()
    messagebox.showinfo("Logged", f"{protein}g of protein added from {food}!")

add_btn_frame = tk.Frame(main_frame, bg="white")
add_btn_frame.pack(pady=20)

add_btn = tk.Button(add_btn_frame, text="+ Add Protein", command=log_food,
                    bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=20, height=2)
add_btn.pack()

update_progress()
root.mainloop()
