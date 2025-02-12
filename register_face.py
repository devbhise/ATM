import cv2
import os
import tkinter as tk
from tkinter import messagebox
from database import add_user
import time

def capture_faces():
    atm_number = atm_entry.get()

    if len(atm_number) != 4 or not atm_number.isdigit():
        messagebox.showerror("Error", "Enter a valid 4-digit ATM number!")
        return

    if not add_user(atm_number):
        messagebox.showerror("Error", "User already exists!")
        return

    face_folder = f"faces/{atm_number}/"
    os.makedirs(face_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Face Capture", "Look at the camera. Capturing multiple face images...")

    for i in range(5):  # Capture 5 images
        for j in range(3, 0, -1):
            message_label.config(text=f"Capturing Image {i+1}/5 in {j} seconds...", fg="blue")
            root.update()
            time.sleep(1)
        ret, frame = cap.read()
        if ret:
            file_path = os.path.join(face_folder, f"face_{i+1}.jpg")
            cv2.imwrite(file_path, frame)
            message_label.config(text=f"Captured Image {i+1}/5", fg="green")
            root.update()
            time.sleep(1)  # Delay before capturing the next image

    cap.release()
    messagebox.showinfo("Success", "Face Registered Successfully!")
    atm_entry.delete(0, tk.END)
    message_label.config(text="")

root = tk.Tk()
root.title("Register Face")
root.geometry("400x200")

label = tk.Label(root, text="Enter Last 4 Digits of ATM Number:", font=("Arial", 12))
label.pack(pady=10)

atm_entry = tk.Entry(root, font=("Arial", 12))
atm_entry.pack(pady=5)

capture_btn = tk.Button(root, text="Register Face", command=capture_faces, font=("Arial", 12))
capture_btn.pack(pady=20)

message_label = tk.Label(root, text="", font=("Arial", 12))
message_label.pack(pady=10)

root.mainloop()