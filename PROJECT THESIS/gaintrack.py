# ETO NEED PARA GUMANA ANG ATING PROGRAM
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from datafunctions import load_foods, add_log, total_today
import os

# helper functions
def calculate_protein(food, amount):
    if food in food_data:
        protein = food_data[food] * (amount / 100)
        return round(protein, 2)    
    else:
        return 0

# age to 2digit
def validate_age_input(new_value):
    if new_value == "":  
        return True
    if new_value.isdigit() and len(new_value) <= 2:
        return True
    return False

# weight to 3digit
def validate_weight_input(new_value):
    if new_value == "":  
        return True
    if new_value.isdigit() and len(new_value) <= 3:
        return True
    return False

# MAIN GUI
root = tk.Tk()
root.title("GainTrack - Protein Intake Tracker")
root.state("zoomed")


# colors and fonts
BG_COLOR = "#FF7B54"
TEXT_COLOR = "white"
FONT_TITLE = ("Arial", 28, "bold")
FONT_LABEL = ("Arial", 14)
FONT_BUTTON = ("Arial", 14, "bold")


# load data
food_data = load_foods()
protein_goal = 0


# progress bar (style ng progress bar ya)
style = ttk.Style()
style.theme_use('default')
style.configure("Orange.Horizontal.TProgressbar", troughcolor="#FFE8D6", background=BG_COLOR, thickness=30, bordercolor="#FFE8D6")


# Top section ng main GUI
top_frame = tk.Frame(root, bg=BG_COLOR, height=200)
top_frame.pack(fill="x")


title_label = tk.Label(top_frame, text="GainTrack", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_TITLE)
title_label.pack(pady=(30, 5))


date_label = tk.Label(top_frame, text=date.today().strftime("%B %d, %Y"), bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 16))
date_label.pack()


protein_display = tk.Label(top_frame, text="0g / 0g", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 42, "bold"))
protein_display.pack(pady=(10, 0))


# Main frame
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True, pady=20)


progress = ttk.Progressbar(main_frame, length=600, maximum=100, style="Orange.Horizontal.TProgressbar")
progress.pack(pady=20)


# Profile section ng main GUI
profile_frame = tk.Frame(main_frame, bg="white")
profile_frame.pack(pady=10)


tk.Label(profile_frame, text="Set Your Profile", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 10))


tk.Label(profile_frame, text="Weight (kg):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
validate_weight = root.register(validate_weight_input)
weight_entry = tk.Entry(profile_frame, width=20, validate="key", validatecommand=(validate_weight, "%P"))
weight_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(profile_frame, text="Age:", bg="white", font=FONT_LABEL).grid(row=2, column=0, padx=10, pady=5, sticky="e")
validate_age = root.register(validate_age_input)
age_entry = tk.Entry(profile_frame, width=20, validate="key", validatecommand=(validate_age, "%P"))
age_entry.grid(row=2, column=1, padx=10, pady=5)



tk.Label(profile_frame, text="Goal:", bg="white", font=FONT_LABEL).grid(row=3, column=0, padx=10, pady=5, sticky="e")
goal_var = tk.StringVar(value="")
goal_menu = ttk.Combobox(profile_frame, textvariable=goal_var, values=["BULKING", "CUTTING", "MAINTENANCE"], width=18, state="readonly")
goal_menu.grid(row=3, column=1, padx=10, pady=5)


def save_profile():
    global protein_goal
    try:
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid weight.")
        return
   
    goal = goal_var.get()
    if not goal:
        messagebox.showerror("Error", "Select a goal.")
        return

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


# Dito foods (FOOD INPUTS)
input_frame = tk.Frame(main_frame, bg="white")
input_frame.pack(pady=20)


tk.Label(input_frame, text="Select Food:", bg="white", font=FONT_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
food_var = tk.StringVar()
food_menu = ttk.Combobox(input_frame, textvariable=food_var, values=list(load_foods().keys()), width=25, state="readonly")
food_menu.grid(row=0, column=1, padx=10, pady=5)


tk.Label(input_frame, text="Amount (grams):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
amount_entry = tk.Entry(input_frame, width=27)
amount_entry.grid(row=1, column=1, padx=10, pady=5)


# This is buttons
def update_progress():
    today_total = total_today()
    if protein_goal > 0:
        percentage = min((today_total / protein_goal) * 100, 100)
        progress["value"] = percentage
        protein_display.config(text=f"{today_total}g / {protein_goal}g")
        if today_total >= protein_goal:
            add_btn.config(state="disabled")
        else:
            add_btn.config(state="normal")


    else:
        protein_display.config(text=f"{today_total}g / 0g")
        add_btn.config(state="normal")



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
    today_total = total_today()
    if protein_goal > 0 and today_total >= protein_goal:
        messagebox.showinfo("🎉 Goal Reached!", f"You've reached your daily protein goal of {protein_goal}g!")
        add_btn.config(state="disabled")

def clear_program():
    global protein_goal
    food_var.set("")
    amount_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    goal_var.set("")

    # reset data
    protein_goal = 0
    protein_display.config(text="0g / 0g")
    progress["value"] = 0
    add_btn.config(state="normal")

    messagebox.showinfo("Reset", "Program has been reset!")


#add protein & clear button
add_btn_frame = tk.Frame(main_frame, bg="white")
add_btn_frame.pack(pady=20)

add_btn = tk.Button(add_btn_frame, text="+ Add Protein", command=log_food,
                    bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=18, height=2)
add_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(add_btn_frame, text="⟳ Clear", command=clear_program,
                      bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=10, height=2)
clear_btn.grid(row=0, column=1, padx=10)



update_progress()
root.mainloop()
