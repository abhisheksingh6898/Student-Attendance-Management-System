import sqlite3
import tkinter as tk
from tkinter import messagebox

# --- STEP 1: DATABASE SETUP (Table banana) ---
def init_db():
  conn = sqlite3.connect("calculator.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS calc_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num1 REAL,
            num2 REAL,
            operation TEXT,
            result REAL,
            calc_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


# --- STEP 2: DATA SAVE KARNE KA FUNCTION ---
def save_to_database(num1, num2, operation, result):
  try:
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO calc_history (num1, num2, operation, result) 
            VALUES (?, ?, ?, ?)
        """,
        (num1, num2, operation, result),
    )
    conn.commit()
    conn.close()
  except Exception as e:
    print("Database Error:", e)


# --- STEP 3: CALCULATOR LOGIC & GUI CONNECTION ---
def calculate():
  try:
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    choice = operation_var.get()
    op_name = ""
    res = 0

    if choice == "1. Addition":
      op_name = "Addition"
      res = num1 + num2
    elif choice == "2. Subtraction":
      op_name = "Subtraction"
      res = num1 - num2
    elif choice == "3. Multiplication":
      op_name = "Multiplication"
      res = num1 * num2
    elif choice == "4. Division":
      if num2 == 0:
        messagebox.showerror("Error", "Division by zero is not allowed!")
        return
      op_name = "Division"
      res = num1 / num2
    elif choice == "5. Average":
      op_name = "Average"
      res = (num1 + num2) / 2

    # Result screen par show karo
    result_label.config(text=f"Result: {res}")

    # Calculation ko database mein save karo
    save_to_database(num1, num2, op_name, res)

  except ValueError:
    messagebox.showerror("Error", "Please enter valid numbers!")


# Program shuru hote hi database table ready kar lo
init_db()

# --- STEP 4: TKINTER GUI (Interface Design) ---
root = tk.Tk()
root.title("Python Calculator Project with Database")
root.geometry("350x420")
root.config(bg="#f4f4f9")

tk.Label(
    root,
    text="My Calculator Project",
    font=("Arial", 14, "bold"),
    bg="#f4f4f9",
    fg="#333",
).pack(pady=15)

tk.Label(root, text="Enter First Number:", bg="#f4f4f9").pack()
entry1 = tk.Entry(root, font=("Arial", 11), width=20)
entry1.pack(pady=5)

tk.Label(root, text="Enter Second Number:", bg="#f4f4f9").pack()
entry2 = tk.Entry(root, font=("Arial", 11), width=20)
entry2.pack(pady=5)

tk.Label(root, text="Select Operation:", bg="#f4f4f9").pack()
operation_var = tk.StringVar(root)
operation_var.set("1. Addition")

options = [
    "1. Addition",
    "2. Subtraction",
    "3. Multiplication",
    "4. Division",
    "5. Average",
]
dropdown = tk.OptionMenu(root, operation_var, *options)
dropdown.config(width=18, font=("Arial", 10))
dropdown.pack(pady=5)

tk.Button(
    root,
    text="Calculate & Save",
    command=calculate,
    bg="#007bff",
    fg="white",
    font=("Arial", 11, "bold"),
    width=16,
).pack(pady=15)

result_label = tk.Label(
    root,
    text="Result: ",
    font=("Arial", 11, "bold"),
    bg="#f4f4f9",
    fg="#007bff",
)
result_label.pack(pady=10)

root.mainloop()