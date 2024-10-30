import tkinter as tk
from tkinter import ttk
import re
import enchant
import requests

def load_common_passwords():
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return set(response.text.splitlines())
    else:
        print("Failed to load common passwords list")
        return set()

common_passwords = load_common_passwords()

def check_password_strength(*args):
    password = password_var.get()
    
    # Clear feedback and reset strength meter when password is empty
    if not password:
        feedback_text.set("")
        strength_var.set(0)
        strength_meter.config(style="Red.Horizontal.TProgressbar")
        return

    strength = 0
    feedback = []
    max_strength = 6

    # Check if password is in common passwords list
    if password.lower() in common_passwords:
        feedback.append("Password is too common")
        strength = 0
    elif 'password' in password.lower():
        feedback.append("Password contains the word 'password'")
        strength = 0
    else:
        # Check length
        if len(password) < 8:
            feedback.append("Password is too short")
        else:
            if len(password) >= 15:
                strength += 2
            else:
                strength += 1

        # Check for uppercase
        if re.search(r"[A-Z]", password):
            strength += 1
        else:
            feedback.append("Add uppercase letters")

        # Check for lowercase
        if re.search(r"[a-z]", password):
            strength += 1
        else:
            feedback.append("Add lowercase letters")

        # Check for digits
        if re.search(r"\d", password):
            strength += 1
        else:
            feedback.append("Add numbers")

        # Check for special characters
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1
        else:
            feedback.append("Add special characters")

        # Check for dictionary words
        d = enchant.Dict("en_US")
        if d.check(password.lower()):
            feedback.append("Contains a dictionary word")
            strength -= 1

        # Check for 3 or more consecutive identical characters
        if re.search(r"(.)\1{2,}", password):
            feedback.append("Contains repeated characters")
            strength -= 1

    # Ensure strength is within bounds
    strength = max(0, min(strength, max_strength))

    # Calculate percentage for progress bar
    strength_percentage = (strength / max_strength) * 100

    # Update strength meter
    strength_var.set(strength_percentage)

    # Update strength meter color
    if strength_percentage <= 20:
        strength_meter.config(style="Red.Horizontal.TProgressbar")
    elif strength_percentage <= 40:
        strength_meter.config(style="Orange.Horizontal.TProgressbar")
    elif strength_percentage <= 60:
        strength_meter.config(style="Yellow.Horizontal.TProgressbar")
    elif strength_percentage <= 80:
        strength_meter.config(style="LightGreen.Horizontal.TProgressbar")
    else:
        strength_meter.config(style="DarkGreen.Horizontal.TProgressbar")

    # Update feedback
    feedback_text.set("\n".join(feedback) if feedback else "Strong password")

def toggle_password_visibility():
    password_entry.config(show="" if show_password_var.get() else "*")

# Create main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x300")

# Create styles for progress bar
style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=20)
style.configure("Red.Horizontal.TProgressbar", background="red")
style.configure("Orange.Horizontal.TProgressbar", background="orange")
style.configure("Yellow.Horizontal.TProgressbar", background="yellow")
style.configure("LightGreen.Horizontal.TProgressbar", background="light green")
style.configure("DarkGreen.Horizontal.TProgressbar", background="dark green")

# Create variables
password_var = tk.StringVar()
password_var.trace_add("write", check_password_strength)
show_password_var = tk.BooleanVar()
strength_var = tk.DoubleVar()
feedback_text = tk.StringVar()

# Create and place widgets
ttk.Label(root, text="Password Strength Checker", font=("Arial", 16)).pack(pady=10)

password_entry = ttk.Entry(root, textvariable=password_var, show="*", width=30)
password_entry.pack(pady=5)

ttk.Checkbutton(root, text="Show password", variable=show_password_var, command=toggle_password_visibility).pack()

strength_meter = ttk.Progressbar(root, length=300, variable=strength_var, mode="determinate", style="Red.Horizontal.TProgressbar")
strength_meter.pack(pady=10)

feedback_label = ttk.Label(root, textvariable=feedback_text, wraplength=350, justify="center")
feedback_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()