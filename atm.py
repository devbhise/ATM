import tkinter as tk
from tkinter import messagebox
from database import get_balance, update_balance
import cv2
import os
import face_recognition
from connection import send_withdraw_signal , check_connection

def authenticate(atm_last4):
    face_folder = f"faces/{atm_last4}/"

    if not os.path.exists(face_folder):
        messagebox.showerror("Error", "Face not found! Please register first.")
        return False

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Authentication", "Scanning Face. Look at the camera.")

    ret, input_frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Camera error!")
        return False

    input_encodings = face_recognition.face_encodings(input_frame)

    if not input_encodings:
        messagebox.showerror("Error", "No face detected in the input frame!")
        return False

    input_encoding = input_encodings[0]

    for file in os.listdir(face_folder):
        stored_image = face_recognition.load_image_file(os.path.join(face_folder, file))
        stored_encodings = face_recognition.face_encodings(stored_image)

        if not stored_encodings:
            continue

        stored_encoding = stored_encodings[0]
        matches = face_recognition.compare_faces([stored_encoding], input_encoding)

        if matches[0]:
            return True

    messagebox.showerror("Error", "Face not matched!")
    return False

def atm_menu(atm_last4):
    if not check_connection():
        return
    root = tk.Tk()
    root.title("ATM Menu")
    root.geometry("400x300")

    balance = get_balance(atm_last4)

    tk.Label(root, text=f"Welcome! Your balance is: ₹{balance}", font=("Arial", 12)).pack(pady=10)
    def withdraw():
            amount = int(amount_entry.get())
            if amount % 100 != 0:
                messagebox.showerror("Error", "Please enter an amount that is a multiple of 100.")
                return
            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            if send_withdraw_signal(amount):
                new_balance = balance - amount
                update_balance(atm_last4, new_balance)
                messagebox.showinfo("Success", f"Withdrawn ₹{amount}. New balance: ₹{new_balance}")
                root.destroy()
            else:
                messagebox.showerror("Error", "Failed to communicate with the ATM hardware.")

    def show_balance():
        messagebox.showinfo("Balance", f"Your current balance is: ₹{balance}")

    def exit_atm():
        root.destroy()

    tk.Label(root, text="Enter amount to withdraw:", font=("Arial", 12)).pack(pady=10)
    amount_entry = tk.Entry(root, font=("Arial", 12))
    amount_entry.pack(pady=5)

    tk.Button(root, text="Withdraw", command=withdraw, font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Show Balance", command=show_balance, font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Exit", command=exit_atm, font=("Arial", 12)).pack(pady=10)

    root.mainloop()