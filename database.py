import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database():
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atm_last4 TEXT UNIQUE,
                balance INTEGER DEFAULT 5000
            )
        """)
        conn.commit()
        logging.info("Database created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error creating database: {e}")
    finally:
        conn.close()

def add_user(atm_last4):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (atm_last4) VALUES (?)", (atm_last4,))
        conn.commit()
        logging.info(f"User with ATM last 4 digits {atm_last4} added successfully.")
        return True
    except sqlite3.IntegrityError:
        logging.warning(f"User with ATM last 4 digits {atm_last4} already exists.")
        return False
    except sqlite3.Error as e:
        logging.error(f"Error adding user: {e}")
        return False
    finally:
        conn.close()

def get_balance(atm_last4):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT balance FROM users WHERE atm_last4=?", (atm_last4,))
        row = c.fetchone()
        logging.info(f"Balance retrieved for ATM last 4 digits {atm_last4}.")
        return row[0] if row else None
    except sqlite3.Error as e:
        logging.error(f"Error retrieving balance: {e}")
        return None
    finally:
        conn.close()

def update_balance(atm_last4, amount):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET balance = ? WHERE atm_last4=?", (amount, atm_last4))
        conn.commit()
        logging.info(f"Balance updated for ATM last 4 digits {atm_last4}.")
    except sqlite3.Error as e:
        logging.error(f"Error updating balance: {e}")
    finally:
        conn.close()

create_database()