# ETO NEED PARA GUMANA ANG ATING PROGRAM
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from datafunctions import load_foods, add_log, total_today
import os

# helper functions
# Calculate protein content based on food type and amount consumed
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


# Application title label
title_label = tk.Label(top_frame, text="GainTrack", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_TITLE)
title_label.pack(pady=(30, 5))

# Current date display label
date_label = tk.Label(top_frame, text=date.today().strftime("%B %d, %Y"), bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 16))
date_label.pack()

# Protein intake display showing current total vs goal
protein_display = tk.Label(top_frame, text="0g / 0g", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 42, "bold"))
protein_display.pack(pady=(10, 0))


# Main frame
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True, pady=20)


# Progress bar to visualize protein goal completion percentage
progress = ttk.Progressbar(main_frame, length=600, maximum=100, style="Orange.Horizontal.TProgressbar")
progress.pack(pady=20)


# Profile section ng main GUI
profile_frame = tk.Frame(main_frame, bg="white")
profile_frame.pack(pady=10)


# Profile section title
tk.Label(profile_frame, text="Set Your Profile", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Weight input field with validation (max 3 digits)
tk.Label(profile_frame, text="Weight (kg):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
validate_weight = root.register(validate_weight_input)
weight_entry = tk.Entry(profile_frame, width=20, validate="key", validatecommand=(validate_weight, "%P"))
weight_entry.grid(row=1, column=1, padx=10, pady=5)

# Age input field with validation (max 2 digits)
tk.Label(profile_frame, text="Age:", bg="white", font=FONT_LABEL).grid(row=2, column=0, padx=10, pady=5, sticky="e")
validate_age = root.register(validate_age_input)
age_entry = tk.Entry(profile_frame, width=20, validate="key", validatecommand=(validate_age, "%P"))
age_entry.grid(row=2, column=1, padx=10, pady=5)

# Goal selection dropdown (BULKING, CUTTING, or MAINTENANCE)
tk.Label(profile_frame, text="Goal:", bg="white", font=FONT_LABEL).grid(row=3, column=0, padx=10, pady=5, sticky="e")
goal_var = tk.StringVar(value="")
goal_menu = ttk.Combobox(profile_frame, textvariable=goal_var, values=["BULKING", "CUTTING", "MAINTENANCE"], width=18, state="readonly")
goal_menu.grid(row=3, column=1, padx=10, pady=5)


# Save user profile and calculate protein goal based on weight and fitness goal
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

    # Calculate protein goal: BULKING (2.0g/kg), CUTTING (1.8g/kg), MAINTENANCE (1.6g/kg)
    if goal == "BULKING":
        target = weight * 2.0
    elif goal == "CUTTING":
        target = weight * 1.8
    else:
        target = weight * 1.6

    # Set global protein goal and update display
    protein_goal = round(target, 2)
    update_progress()
    messagebox.showinfo("Profile Saved", f"Daily Protein Goal: {protein_goal}g")


# Save Profile button to calculate and set daily protein goal
tk.Button(profile_frame, text="Save Profile", command=save_profile, bg=BG_COLOR, fg="white",
          font=FONT_BUTTON, width=18, height=1).grid(row=4, column=0, columnspan=2, pady=10)


# Dito foods (FOOD INPUTS)
input_frame = tk.Frame(main_frame, bg="white")
input_frame.pack(pady=20)


# Food selection dropdown populated from foods.csv
tk.Label(input_frame, text="Select Food:", bg="white", font=FONT_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
food_var = tk.StringVar()
food_menu = ttk.Combobox(input_frame, textvariable=food_var, values=list(load_foods().keys()), width=25, state="readonly")
food_menu.grid(row=0, column=1, padx=10, pady=5)

# Amount input field for food quantity in grams
tk.Label(input_frame, text="Amount (grams):", bg="white", font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
amount_entry = tk.Entry(input_frame, width=27)
amount_entry.grid(row=1, column=1, padx=10, pady=5)


# This is buttons
# Update progress bar and protein display based on today's total intake
def update_progress():
    today_total = total_today()
    if protein_goal > 0:
        # Calculate percentage and cap at 100%
        percentage = min((today_total / protein_goal) * 100, 100)
        progress["value"] = percentage
        protein_display.config(text=f"{today_total}g / {protein_goal}g")
        # Disable add button if goal is reached
        if today_total >= protein_goal:
            add_btn.config(state="disabled")
        else:
            add_btn.config(state="normal")
    else:
        # No goal set, just show current total
        protein_display.config(text=f"{today_total}g / 0g")
        add_btn.config(state="normal")



# Log food intake, calculate protein, save to CSV, and update display
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
   
    # Calculate protein content and save to logs.csv
    protein = calculate_protein(food, amount)
    add_log(food, amount, protein)
    update_progress()
    messagebox.showinfo("Logged", f"{protein}g of protein added from {food}!")
    # Check if daily goal is reached
    today_total = total_today()
    if protein_goal > 0 and today_total >= protein_goal:
        messagebox.showinfo("Goal Reached!", f"You've reached your daily protein goal of {protein_goal}g!")
        add_btn.config(state="disabled")


# Clear all input fields and reset protein goal (does not delete history)
def clear_program():
    global protein_goal
    # Clear all input fields
    food_var.set("")
    amount_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    goal_var.set("")

    # Reset data and display
    protein_goal = 0
    protein_display.config(text="0g / 0g")
    progress["value"] = 0
    add_btn.config(state="normal")

    messagebox.showinfo("Reset", "Program has been reset!")

# Display history window showing all logged protein intake from logs.csv
def show_history():
    if not os.path.exists("logs.csv"):
        messagebox.showinfo("History", "No history available yet.")
        return

    # Create new window for history display
    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("400x400")

    tk.Label(history_window, text="Protein Intake History",
             font=("Arial", 16, "bold")).pack(pady=10)

    # Content frame with text box and scrollbar for viewing all logs
    content_frame = tk.Frame(history_window)
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    text_box = tk.Text(content_frame, width=50, height=15)
    text_box.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(content_frame, command=text_box.yview)
    scrollbar.pack(side="right", fill="y")
    text_box.config(yscrollcommand=scrollbar.set)

    # Read and display all entries from logs.csv
    with open("logs.csv", "r") as file:
        for line in file:
            text_box.insert(tk.END, line)

    text_box.config(state="disabled")

    # Separate frame for the reset button so it's always visible
    btn_frame = tk.Frame(history_window)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Reset History",
          command=reset_history, bg=BG_COLOR, fg="black",
          font=FONT_BUTTON, width=15).pack()


# Clear all history data from logs.csv file (permanently deletes all logged entries)
def reset_history():
    if not os.path.exists("logs.csv"):
        messagebox.showinfo("Reset History", "No history to reset.")
        return

    # Ask for confirmation before deleting all history
    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete ALL history?")
    if not confirm:
        return

    # Clear the entire logs.csv file
    with open("logs.csv", "w") as file:
        file.write("")

    messagebox.showinfo("Reset History", "History has been cleared!")


# Add protein & clear button section
add_btn_frame = tk.Frame(main_frame, bg="white")
add_btn_frame.pack(pady=20)

# History button to view all logged protein intake
history_btn = tk.Button(add_btn_frame, text="History", command=show_history,
                        bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=10, height=2)
history_btn.grid(row=0, column=0, padx=10)

# Add Protein button to log food intake
add_btn = tk.Button(add_btn_frame, text="+ Add Protein", command=log_food,
                    bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=18, height=2)
add_btn.grid(row=0, column=1, padx=10)

# Clear button to reset all input fields and protein goal
clear_btn = tk.Button(add_btn_frame, text="Clear", command=clear_program,
                      bg=BG_COLOR, fg="white", font=FONT_BUTTON, width=10, height=2)
clear_btn.grid(row=0, column=2, padx=10)



# Initialize progress display on startup
update_progress()
# Start the GUI event loop
root.mainloop()
