import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate a password
def generate_password(length, exclude_chars):
    if length > 30:
        messagebox.showerror("Error", "Password length cannot exceed 30 characters!")
        return ""

    all_characters = string.ascii_letters + string.digits + string.punctuation
    available_characters = ''.join([char for char in all_characters if char not in exclude_chars])

    if not available_characters:
        messagebox.showerror("Error", "No valid characters available for password generation!")
        return ""

    password = ''.join(random.choice(available_characters) for _ in range(length))
    return password

# Function to save password
def save_to_file(password, title):
    if not title.strip():
        messagebox.showerror("Error", "Title is required!")
        return

    # Check if the title already exists in the file when creating a new password
    if check_duplicate_title(title):
        messagebox.showerror("Error", "Title already exists in the file!")
        return

    try:
        with open("Credentials.txt", "a") as file:
            file.write(f"Title: {title}\nPassword: {password}\n\n---\n")
        messagebox.showinfo("Success", "Password saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save password: {e}")

# Function to retrieve a password
def retrieve_password(title, pin):
    if not title.strip():
        messagebox.showerror("Error", "Title is required!")
        return
    if pin != "1234":
        messagebox.showerror("Error", "Incorrect PIN!")
        return

    try:
        with open("Credentials.txt", "r") as file:
            data = file.readlines()

        found, stored_password = False, None

        for i in range(len(data)):
            if f"Title: {title}" in data[i]:
                found = True
                stored_password = data[i + 1].replace("Password: ", "").strip()
                break

        if found and stored_password:
            retrieve_password_label.config(text=f"Retrieved Password: {stored_password}")
        else:
            messagebox.showerror("Error", "No matching password found!")

    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found!")

# Function to update a password
def update_password(title, pin, new_password):
    if not title.strip():
        messagebox.showerror("Error", "Title is required!")
        return
    if pin != "1234":
        messagebox.showerror("Error", "Incorrect PIN!")
        return
    if not new_password.strip():
        messagebox.showerror("Error", "New password cannot be empty!")
        return

    if not check_duplicate_title(title):  # Check if title exists for update
        messagebox.showerror("Error", "No matching password found to update!")
        return

    try:
        with open("Credentials.txt", "r") as file:
            data = file.readlines()

        found = False
        for i in range(len(data)):
            if f"Title: {title}" in data[i]:
                found = True
                data[i + 1] = f"Password: {new_password}\n"
                break

        if found:
            with open("Credentials.txt", "w") as file:
                file.writelines(data)
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", "No matching password found!")

    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found!")

# Function to check for duplicate title
def check_duplicate_title(title):
    try:
        with open("Credentials.txt", "r") as file:
            data = file.readlines()

        for i in range(len(data)):
            if f"Title: {title}" in data[i]:
                return True
        return False

    except FileNotFoundError:
        return False

# GUI Functions
def show_create_screen():
    choice_frame.pack_forget()
    create_frame.pack(pady=20)

def show_retrieve_screen():
    choice_frame.pack_forget()
    retrieve_frame.pack(pady=20)

def show_update_screen():
    choice_frame.pack_forget()
    update_frame.pack(pady=20)

def go_back():
    create_frame.pack_forget()
    retrieve_frame.pack_forget()
    update_frame.pack_forget()
    choice_frame.pack(pady=20)

def on_generate_button_click():
    try:
        length = int(length_entry.get())
        exclude_chars = exclude_entry.get()
        title = title_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Title is required!")
            return

        # Check if title already exists before generating password
        if check_duplicate_title(title):
            messagebox.showerror("Error", "Title already exists in the file!")
            return

        password = generate_password(length, exclude_chars)

        if password:
            password_label.config(text=f"Generated Password: {password}")
            save_to_file(password, title)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the password length.")

def on_retrieve_button_click():
    retrieve_password(retrieve_title_entry.get().strip(), retrieve_pin_entry.get())

def on_update_button_click():
    update_password(update_title_entry.get().strip(), update_pin_entry.get(), update_new_password_entry.get())

# Setup GUI
root = tk.Tk()
root.title("Password Manager")
root.geometry("600x500")
root.config(bg="#2C2F33")  # Dark background

# Custom button style
button_style = {
    "font": ("Arial", 12, "bold"),
    "fg": "white",
    "bg": "#7289DA",
    "activebackground": "#5A6CA8",
    "activeforeground": "white",
    "bd": 3,
    "relief": "ridge",
    "padx": 20,
    "pady": 10,
    "width": 20
}

entry_style = {
    "font": ("Arial", 12),
    "width": 30,
    "bd": 3,
    "relief": "ridge"
}

# Main choice frame
choice_frame = tk.Frame(root, bg="#2C2F33")
choice_frame.pack(pady=20)

tk.Label(choice_frame, text="Password Manager", font=("Arial", 18, "bold"), fg="white", bg="#2C2F33").pack(pady=10)
tk.Button(choice_frame, text="Create Password", command=show_create_screen, **button_style).pack(pady=10)
tk.Button(choice_frame, text="Retrieve Password", command=show_retrieve_screen, **button_style).pack(pady=10)
tk.Button(choice_frame, text="Update Password", command=show_update_screen, **button_style).pack(pady=10)

# Create Password Frame
create_frame = tk.Frame(root, bg="#2C2F33")

tk.Label(create_frame, text="Title (Required):", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
title_entry = tk.Entry(create_frame, **entry_style)
title_entry.pack()

tk.Label(create_frame, text="Password Length:", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
length_entry = tk.Entry(create_frame, **entry_style)
length_entry.pack()

tk.Label(create_frame, text="Exclude Characters:", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
exclude_entry = tk.Entry(create_frame, **entry_style)
exclude_entry.pack()

tk.Button(create_frame, text="Generate Password", command=on_generate_button_click, **button_style).pack(pady=10)
tk.Button(create_frame, text="Go Back", command=go_back, **button_style).pack(pady=5)

password_label = tk.Label(create_frame, text="Generated Password: ", font=("Arial", 12), fg="white", bg="#2C2F33")
password_label.pack()

# Retrieve Password Frame
retrieve_frame = tk.Frame(root, bg="#2C2F33")

tk.Label(retrieve_frame, text="Title (Required):", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
retrieve_title_entry = tk.Entry(retrieve_frame, **entry_style)
retrieve_title_entry.pack()

tk.Label(retrieve_frame, text="Enter PIN:", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
retrieve_pin_entry = tk.Entry(retrieve_frame, show="*", **entry_style)
retrieve_pin_entry.pack()

tk.Button(retrieve_frame, text="Retrieve Password", command=on_retrieve_button_click, **button_style).pack(pady=10)

retrieve_password_label = tk.Label(retrieve_frame, text="", font=("Arial", 12), fg="white", bg="#2C2F33")
retrieve_password_label.pack()

# Update Password Frame
update_frame = tk.Frame(root, bg="#2C2F33")

tk.Label(update_frame, text="Title (Required):", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
update_title_entry = tk.Entry(update_frame, **entry_style)
update_title_entry.pack()

tk.Label(update_frame, text="Enter PIN:", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
update_pin_entry = tk.Entry(update_frame, show="*", **entry_style)
update_pin_entry.pack()

tk.Label(update_frame, text="New Password (Required):", font=("Arial", 12), fg="white", bg="#2C2F33").pack()
update_new_password_entry = tk.Entry(update_frame, **entry_style)
update_new_password_entry.pack()

tk.Button(update_frame, text="Update Password", command=on_update_button_click, **button_style).pack(pady=10)
tk.Button(update_frame, text="Go Back", command=go_back, **button_style).pack(pady=5)

root.mainloop()
