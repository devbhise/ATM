import serial
import serial.tools.list_ports
import time
from tkinter import messagebox

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None

def check_connection():
    port = find_arduino_port()
    if port is None:
        messagebox.showerror("Error", "Arduino not found")
        return False

    try:
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Wait for the connection to establish
        arduino.close()
        messagebox.showinfo("Connection", "Arduino connected successfully")
        return True
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error communicating with Arduino: {e}")
        return False

def send_withdraw_signal(amount):
    port = find_arduino_port()
    if port is None:
        messagebox.showerror("Error", "Arduino not found")
        return False

    try:
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Wait for the connection to establish

        notes = amount // 100  # Calculate the number of 100 notes to dispense

        for _ in range(notes):
            arduino.write(b'WITHDRAW\n')  # Send the withdraw signal
            response = arduino.readline().decode('utf-8').strip()
            if response != 'OK':
                arduino.close()
                return False
            time.sleep(1)  # Delay between signals

        arduino.close()
        return True
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error communicating with Arduino: {e}")
        return False