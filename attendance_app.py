import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
# -------------------------------
# STEP 1: Sample student data
# -------------------------------
students = {
    101: {"name": "Rahul Sharma", "course": "BCA", "semester": 1},
    102: {"name": "Priya Singh", "course": "BCA", "semester": 1},
    103: {"name": "Aman Kumar", "course": "BCA", "semester": 2},
    104: {"name": "Neha Verma", "course": "MCA", "semester": 1},
    105: {"name": "Arjun Singh", "course": "MCA", "semester": 2}
}

# Attendance records are stored in Python memory.
# This demo does NOT connect to Oracle.
attendance = []
# STEP 2: Create main window
# -------------------------------
root = tk.Tk()
root.title("Student Attendance Management System")
root.geometry("950x600")
root.configure(bg="#f0f4f8")

title = tk.Label(
    root,
    text="Student Attendance Management System",
    font=("Arial", 20, "bold"),
    bg="#17365d",
    fg="white",
    pady=15
)
title.pack(fill="x")

subtitle = tk.Label(
    root,
    text="Manage Students | Mark Attendance | View Reports",
    font=("Arial", 11),
    bg="#f0f4f8"
)
subtitle.pack(pady=8)
# -------------------------------
# STEP 3: Student report table
# -------------------------------
columns = (
    "ID", "Name", "Course", "Semester",
    "Total", "Present", "Absent", "Percentage"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=105, anchor="center")

table.column("Name", width=150)
table.pack(fill="both", expand=True, padx=15, pady=10)

# -------------------------------
# STEP 4: Calculate percentage
# -------------------------------
def get_percentage(student_id):
    records = [
        item for item in attendance
        if item["student_id"] == student_id
    ]

    if not records:
        return 0

    present_count = sum(
        1 for item in records
        if item["status"] == "Present"
    )

    return round(present_count * 100 / len(records), 2)


# -------------------------------
# STEP 5: Refresh report
# -------------------------------
def refresh_report():
    for item in table.get_children():
        table.delete(item)
    for student_id, student in sorted(students.items()):
        records = [
            item for item in attendance
            if item["student_id"] == student_id
        ]

        total = len(records)
        present = sum(
            1 for item in records
            if item["status"] == "Present"
        )
        absent = sum(
            1 for item in records
            if item["status"] == "Absent"
        )

        percentage = get_percentage(student_id)

        table.insert(
            "",
            "end",
            values=(
                student_id,
                student["name"],
                student["course"],
                student["semester"],
                total,
                present,
                absent,
                f"{percentage}%"
            )
        )


# -------------------------------
# STEP 6: Get selected student
# -------------------------------
def get_selected_student():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Please select a student from the table."
        )
        return None

    values = table.item(selected[0], "values")
    return int(values[0])


# -------------------------------
# STEP 7: Mark attendance
# -------------------------------
def mark_attendance(status):
    student_id = get_selected_student()

    if student_id is None:
        return

    today = date.today().isoformat()

    for record in attendance:
        if (
            record["student_id"] == student_id
            and record["date"] == today
        ):
            messagebox.showwarning(
                "Already Marked",
                "Attendance is already marked today."
            )
            return

    attendance.append({
        "student_id": student_id,
        "date": today,
        "status": status
    })

    refresh_report()

    messagebox.showinfo(
        "Success",
        f"{status} attendance marked successfully!"
    )


# -------------------------------
# STEP 8: Add a new student
# -------------------------------
def add_student():
    student_id = simpledialog.askinteger(
        "Add Student", "Enter Student ID:"
    )

    if student_id is None:
        return

    if student_id in students:
        messagebox.showerror(
            "Error", "This Student ID already exists."
        )
        return

    name = simpledialog.askstring(
        "Add Student", "Enter Student Name:"
    )

    if not name or not name.strip():
        messagebox.showerror(
            "Error", "Student name is required."
        )
        return

    course = simpledialog.askstring(
        "Add Student", "Enter Course (BCA/MCA):"
    )

    if not course or not course.strip():
        messagebox.showerror(
            "Error", "Course is required."
        )
        return

    semester = simpledialog.askinteger(
        "Add Student", "Enter Semester:"
    )

    if semester is None or semester < 1:
        messagebox.showerror(
            "Error", "Enter a valid semester."
        )
        return

    students[student_id] = {
        "name": name.strip(),
        "course": course.strip().upper(),
        "semester": semester
    }

    refresh_report()
    messagebox.showinfo(
        "Success", "Student added successfully!"
    )


# -------------------------------
# STEP 9: Show attendance details
# -------------------------------
def show_attendance():
    student_id = get_selected_student()

    if student_id is None:
        return

    records = [
        item for item in attendance
        if item["student_id"] == student_id
    ]

    if not records:
        messagebox.showinfo(
            "Attendance Details",
            "No attendance records found."
        )
        return

    details = "\n".join(
        f'{item["date"]}: {item["status"]}'
        for item in records
    )

    percentage = get_percentage(student_id)

    messagebox.showinfo(
        "Attendance Details",
        f"Student: {students[student_id]['name']}\n\n"
        f"{details}\n\n"
        f"Attendance Percentage: {percentage}%"
    )


# -------------------------------
# STEP 10: Create buttons
# -------------------------------
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=12)

tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    bg="#17365d",
    fg="white",
    width=15
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Mark Present",
    command=lambda: mark_attendance("Present"),
    bg="#198754",
    fg="white",
    width=15
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Mark Absent",
    command=lambda: mark_attendance("Absent"),
    bg="#dc3545",
    fg="white",
    width=15
).grid(row=0, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Attendance Details",
    command=show_attendance,
    width=18
).grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Refresh Report",
    command=refresh_report,
    width=15
).grid(row=0, column=4, padx=5, pady=5)

# -------------------------------
# STEP 11: Start application
# -------------------------------
refresh_report()
root.mainloop()
