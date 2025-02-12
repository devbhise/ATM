import tkinter as tk
from tkinter import messagebox
from atm import authenticate
from database import get_balance, update_balance

def start_auth():
    atm_last4 = atm_entry.get()

    if len(atm_last4) != 4 or not atm_last4.isdigit():
        message_label.config(text="Enter a valid 4-digit ATM number!", fg="red")
        return

    if authenticate(atm_last4):
        messagebox.showinfo("Success", "Authentication Successful!")
        show_atm_menu(atm_last4)
    else:
        message_label.config(text="Authentication Failed! Try again.", fg="red")
        atm_entry.delete(0, tk.END)

def show_atm_menu(atm_last4):
    for widget in root.winfo_children():
        widget.destroy()

    balance = get_balance(atm_last4)

    tk.Label(root, text=f"Welcome! Your balance is: ₹{balance}", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    def withdraw():
        amount = int(amount_entry.get())
        if amount % 100 != 0:
            messagebox.showerror("Error", "Please enter an amount that is a multiple of 100.")
            return
        if amount > balance:
            messagebox.showerror("Error", "Insufficient balance.")
            return
        new_balance = balance - amount
        update_balance(atm_last4, new_balance)
        messagebox.showinfo("Success", f"Withdrawn ₹{amount}. New balance: ₹{new_balance}")
        show_atm_menu(atm_last4)

    def show_balance():
        messagebox.showinfo("Balance", f"Your current balance is: ₹{balance}")

    tk.Label(root, text="Enter amount to withdraw:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    amount_entry = tk.Entry(root, font=("Arial", 14))
    amount_entry.pack(pady=5)

    tk.Button(root, text="Withdraw", command=withdraw, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(root, text="Show Balance", command=show_balance, font=("Arial", 14), bg="#2196F3", fg="white").pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14), bg="#f44336", fg="white").pack(pady=10)

root = tk.Tk()
root.title("Real Time Face Detection and Security System for ATM Machine")
root.state('zoomed')  # Maximize the window

root.configure(bg="#f0f0f0")

tk.Label(root, text="Real Time Face Detection and Security System for ATM Machine", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="Developed by: Siddhika Pokharkar, Bhagyashri Bhalerao, Pratiksha Dolas", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

tk.Label(root, text="Enter Last 4 Digits of ATM:", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
atm_entry = tk.Entry(root, font=("Arial", 14))
atm_entry.pack(pady=10)

tk.Button(root, text="Authenticate", command=start_auth, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=20)

message_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
message_label.pack(pady=10)

root.mainloop()