import tkinter as tk
from tkinter import messagebox
from atm import authenticate, atm_menu

def start_auth():
    atm_last4 = atm_entry.get()

    if len(atm_last4) != 4 or not atm_last4.isdigit():
        message_label.config(text="Enter a valid 4-digit ATM number!", fg="red")
        return

    if authenticate(atm_last4):
        messagebox.showinfo("Success", "Authentication Successful!")
        root.destroy()
        atm_menu(atm_last4)
    else:
        message_label.config(text="Authentication Failed! Try again.", fg="red")
        atm_entry.delete(0, tk.END)

root = tk.Tk()
root.title("ATM Authentication")
root.geometry("400x250")

tk.Label(root, text="Enter Last 4 Digits of ATM:", font=("Arial", 12)).pack(pady=10)
atm_entry = tk.Entry(root, font=("Arial", 12))
atm_entry.pack(pady=5)

tk.Button(root, text="Authenticate", command=start_auth, font=("Arial", 12)).pack(pady=20)

message_label = tk.Label(root, text="", font=("Arial", 12))
message_label.pack(pady=10)

root.mainloop()