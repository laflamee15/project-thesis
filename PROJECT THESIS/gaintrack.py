import customtkinter as ctk
import tkinter as tk
from datetime import date
from datafunctions import (
    load_foods,
    add_log,
    total_today,
    reset_session_logs,
    load_last_user,
    save_user_record,
    save_session_profile,
    load_session_profile,
    LOG_FILE, reset_session_logs,
    STATE_FILE
)
from userfunctions import (
    calculate_protein,
    validate_age_input,
    validate_weight_input,
    calculate_protein_goal
)
import os
from tkinter import messagebox

# --- Initialize CTk ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("GainTrack - Protein Intake Tracker")
root.state("zoomed")

# --- Colors & Fonts ---
BG_COLOR = "#1E1E2F"
FRAME_BG = "#2E2E3E"
ENTRY_BG = "#3A3A4A"
ACCENT_COLOR = "#FF4C29"
TEXT_COLOR = "#FFFFFF"
FONT_TITLE = ("Arial", 28, "bold")
FONT_LABEL = ("Arial", 25)
FONT_BUTTON = ("Arial", 14, "bold")

food_data = load_foods()
protein_goal = 0  # Default state habang wala pang nasi-save na profile

# ----------------- Functions -----------------

def save_profile():
    global protein_goal
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    try:
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid weight.")
        return

    age_value = age_entry.get().strip()
    goal = goal_var.get()
    if not goal:
        messagebox.showerror("Error", "Select a goal.")
        return

    protein_goal = calculate_protein_goal(weight, goal)
    update_progress()
    profile_title_label.configure(text=f"Hello, {name}! Welcome to GainTrack!")

    profile_data = {
        "Name": name,
        "Weight": weight,
        "Age": age_value,
        "Goal": goal,
        "ProteinGoal": protein_goal
    }

    save_user_record(name, weight, age_value, goal, protein_goal)
    save_session_profile(profile_data)
    messagebox.showinfo("Profile Saved", f"Daily Protein Goal: {protein_goal}g")

def load_saved_profile():
    global protein_goal
    session_profile = load_session_profile()
    profile_source = session_profile if session_profile else load_last_user()
    if not profile_source:
        return

    try:
        protein_goal = float(profile_source.get("ProteinGoal", 0))
    except (TypeError, ValueError):
        protein_goal = 0

    name = profile_source.get("Name", "")
    weight = profile_source.get("Weight", "")
    age = profile_source.get("Age", "")
    goal = profile_source.get("Goal", "")

    name_entry.delete(0, tk.END)
    name_entry.insert(0, name)

    weight_entry.delete(0, tk.END)
    weight_entry.insert(0, weight)

    age_entry.delete(0, tk.END)
    age_entry.insert(0, age)

    if goal in goal_menu._values:  # customtkinter Combobox uses _values
        goal_var.set(goal)

    if name:
        profile_title_label.configure(text=f"Hello, {name}! Welcome to GainTrack!")

def update_progress():
    today_total = total_today()
    
    # Always define fraction
    fraction = min(today_total / protein_goal, 1.0) if protein_goal > 0 else 0

    # Update progress bar and text
    progress.set(fraction)
    protein_display.configure(
        text=f"{today_total}g / {protein_goal}g" if protein_goal > 0 else f"{today_total}g / 0g"
    )

    # Disable add button if goal reached
    add_btn.configure(state="disabled" if protein_goal > 0 and today_total >= protein_goal else "normal")

    # Update progress bar color
    progress.configure(progress_color=ACCENT_COLOR if today_total > 0 else progress._fg_color)

    
def log_food():
    food = food_var.get()
    if not food:
        messagebox.showwarning("Missing", "Please select a food item.")
        return

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for amount.")
        return

    protein = calculate_protein(food_data, food, amount)
    add_log(food, amount, protein)
    update_progress()
    messagebox.showinfo("Logged", f"{protein}g of protein added from {food}!")
    if protein_goal > 0 and total_today() >= protein_goal:
        messagebox.showinfo("Goal Reached!", f"You've reached your daily protein goal of {protein_goal}g!")
        add_btn.configure(state="disabled")

def clear_program():
    """Resets the dashboard and clears session/profile files."""
    global protein_goal

    # Clear GUI inputs
    food_var.set("")
    amount_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    goal_var.set("")
    profile_title_label.configure(text=PROFILE_HEADING)

    # Reset session logs and protein goal
    reset_session_logs()
    protein_goal = 0
    update_progress()
    add_btn.configure(state="normal")

    # Remove saved session/profile
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

    messagebox.showinfo("Reset", "Program has been reset!")


def show_history():
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("History", "No history available yet.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("400x400")

    tk.Label(history_window, text="Protein Intake History", font=("Arial", 16, "bold")).pack(pady=10)
    content_frame = tk.Frame(history_window)
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    text_box = tk.Text(content_frame, width=50, height=15)
    text_box.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(content_frame, command=text_box.yview)
    scrollbar.pack(side="right", fill="y")
    text_box.config(yscrollcommand=scrollbar.set)

    with open(LOG_FILE, "r") as file:
        for line in file:
            text_box.insert(tk.END, line)
    text_box.config(state="disabled")

    btn_frame = tk.Frame(history_window)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Reset History", command=reset_history, bg=BG_COLOR, fg="white",
              font=FONT_BUTTON, width=15).pack()

def reset_history():
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Reset History", "No history to reset.")
        return

    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete ALL history?")
    if not confirm:
        return

    with open(LOG_FILE, "w") as file:
        file.write("")
    messagebox.showinfo("Reset History", "History has been cleared!")

#GUI Layout

# Top Frame
top_frame = ctk.CTkFrame(root, corner_radius=0, fg_color=BG_COLOR)
top_frame.pack(fill="x")

title_label = ctk.CTkLabel(top_frame, text="GainTrack", font=FONT_TITLE, fg_color=None, text_color=TEXT_COLOR)
title_label.pack(pady=(30, 5))

date_label = ctk.CTkLabel(top_frame, text=date.today().strftime("%B %d, %Y"), font=("Arial", 16), fg_color=None, text_color=TEXT_COLOR)
date_label.pack()

protein_display = ctk.CTkLabel(top_frame, text="0g / 0g", font=("Arial", 42, "bold"), fg_color=None, text_color=TEXT_COLOR)
protein_display.pack(pady=(10, 20))

# Main Frame
main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color=FRAME_BG)
main_frame.pack(fill="both", expand=True, pady=10, padx=20)

# Progress Bar
progress = ctk.CTkProgressBar(
    main_frame, 
    width=800,
    height=50, 
    progress_color=ACCENT_COLOR,
    )
progress.pack(pady=20)

# Profile Frame
# --- Profile Frame (centered content, taller frame) ---
PROFILE_HEADING = "Set Your Profile"

profile_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=50,
    fg_color=ENTRY_BG,
    width=550,
    height=350  # taller vertically
)
profile_frame.pack(pady=30, padx=10)  # keep spacing above/below, no fill="both" to avoid stretching

# Inner frame to center content
profile_content = ctk.CTkFrame(profile_frame, fg_color="transparent")
profile_content.place(relx=0.5, rely=0.5, anchor="center")  # center content vertically & horizontally

# Profile heading
profile_title_label = ctk.CTkLabel(
    profile_content, 
    text=PROFILE_HEADING, 
    font=("Segoe UI", 25, "bold"), 
    fg_color=None, 
    text_color=TEXT_COLOR
)
profile_title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Name
ctk.CTkLabel(profile_content, text="Name:", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="e")
name_entry = ctk.CTkEntry(profile_content, width=280, height=35, corner_radius=10)
name_entry.grid(row=1, column=1, padx=10, pady=10)

# Weight
ctk.CTkLabel(profile_content, text="Weight (kg):", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=10, sticky="e")
weight_entry = ctk.CTkEntry(profile_content, width=280, height=35, corner_radius=10, validate="key", validatecommand=(root.register(validate_weight_input), "%P"))
weight_entry.grid(row=2, column=1, padx=10, pady=10)

# Age
ctk.CTkLabel(profile_content, text="Age:", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=3, column=0, padx=10, pady=10, sticky="e")
age_entry = ctk.CTkEntry(profile_content, width=280, height=35, corner_radius=10, validate="key", validatecommand=(root.register(validate_age_input), "%P"))
age_entry.grid(row=3, column=1, padx=10, pady=10)

# Goal
ctk.CTkLabel(profile_content, text="Goal:", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=4, column=0, padx=10, pady=10, sticky="e")
goal_var = tk.StringVar()
goal_menu = ctk.CTkComboBox(profile_content, width=280, height=35, values=["BULKING", "CUTTING", "MAINTENANCE"], variable=goal_var, corner_radius=10, state="readonly")
goal_menu.grid(row=4, column=1, padx=10, pady=10)

# Save Profile Button
ctk.CTkButton(
    profile_content, 
    text="Save Profile", 
    font=FONT_LABEL, 
    command=save_profile, 
    fg_color=ACCENT_COLOR,
    hover_color="#FF6A42", 
    corner_radius=15, 
    width=200, 
    height=30

).grid(row=5, column=0, columnspan=2, pady=20)

#Food Input Frame (keep same, just center content)
input_frame = ctk.CTkFrame(
    main_frame, 
    corner_radius=20, 
    fg_color=ENTRY_BG, 
    width=450, 
    height=150
    )

input_frame.pack(pady=0, padx=10)
input_frame.pack_propagate(False)  # prevent shrinking

input_content = ctk.CTkFrame(input_frame, fg_color="transparent")
input_content.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(input_content, text="Select Food:", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10, sticky="e")
food_var = tk.StringVar()
food_menu = ctk.CTkComboBox(input_content, values=list(food_data.keys()), variable=food_var, corner_radius=10, state="readonly", width=200)
food_menu.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(input_content, text="Amount (grams):", font=FONT_LABEL, fg_color=None, text_color=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="e")
amount_entry = ctk.CTkEntry(input_content, width=200, corner_radius=10)
amount_entry.grid(row=1, column=1, padx=10, pady=10)

# --- Buttons Frame (centered buttons) ---
add_btn_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color=FRAME_BG, width=700, height=100)
add_btn_frame.pack(pady=20)
add_btn_frame.pack_propagate(False)

buttons_content = ctk.CTkFrame(add_btn_frame, fg_color="transparent", width=600, height=50)
buttons_content.place(relx=0.5, rely=0.5, anchor="center")
buttons_content.pack_propagate(False)

history_btn = ctk.CTkButton(
    buttons_content, 
    text="History", 
    command=show_history, 
    fg_color=ACCENT_COLOR, 
    hover_color="#FF6A42", 
    corner_radius=15, 
    width=200,
    height=30,
    font=FONT_LABEL
    )

history_btn.grid(row=0, column=0, padx=20)

add_btn = ctk.CTkButton(
    buttons_content, 
    text="+ Add Protein", 
    command=log_food, 
    fg_color=ACCENT_COLOR, 
    hover_color="#FF6A42", 
    corner_radius=15, 
    width=200,
    height=30,
    font=FONT_LABEL
    )

add_btn.grid(row=0, column=1, padx=20)

clear_btn = ctk.CTkButton(
    buttons_content, 
    text="Clear", 
    command=clear_program, 
    fg_color=ACCENT_COLOR, 
    hover_color="#FF6A42", 
    corner_radius=15, 
    width=200,
    height=30,
    font=FONT_LABEL
    )
clear_btn.grid(row=0, column=2, padx=20)


# ----------------- Start -----------------
load_saved_profile()
update_progress()
root.mainloop()
