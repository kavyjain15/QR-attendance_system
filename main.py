import cv2
import os
import pandas as pd
import numpy as np
from datetime import datetime
from tkinter import Tk, Button, simpledialog, messagebox
from pyzbar.pyzbar import decode
from qr_generator import generate_qr
from openpyxl import Workbook

# -------- Add Student Function --------
def add_student():
    student_id = simpledialog.askstring("Add Student", "Enter Student ID (e.g., S101_Anuj):")
    student_email = simpledialog.askstring("Add Email", f"Enter email for {student_id}:")

    if not student_id or not student_email:
        return

    if not os.path.exists("students.csv"):
        pd.DataFrame(columns=["ID", "Email"]).to_csv("students.csv", index=False)

    df = pd.read_csv("students.csv")

    if student_id in df["ID"].values:
        messagebox.showwarning("Duplicate", "Student already exists.")
        return

    df.loc[len(df)] = [student_id, student_email]
    df.to_csv("students.csv", index=False)

    generate_qr(student_id)
    messagebox.showinfo("Success", f"{student_id} added and QR generated.")

# -------- QR Scan & Attendance Function --------
def scan_qr():
    if not os.path.exists("students.csv"):
        messagebox.showerror("Error", "No student data found.")
        return

    student_list = pd.read_csv("students.csv")["ID"].tolist()
    present_set = set()

    cap = cv2.VideoCapture(2)  # change to 1 or 2 if DroidCam is not showing
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for code in decode(frame):
            student_id = code.data.decode('utf-8')
            if student_id not in present_set and student_id in student_list:
                present_set.add(student_id)
                messagebox.showinfo("Marked", f"{student_id} marked present.")

            pts = code.polygon
            pts = [(pt.x, pt.y) for pt in pts]
            cv2.polylines(frame, [np.array(pts)], True, (0, 255, 0), 3)

        cv2.imshow("Scan QR - Press 'q' to finish", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    save_attendance_to_excel(student_list, present_set)

# -------- Save Excel Attendance Function --------
def save_attendance_to_excel(all_students, present_students):
    today = datetime.now()
    folder = f"Attendance/{today.strftime('%B_%Y')}"
    os.makedirs(folder, exist_ok=True)

    file_name = today.strftime("%d-%m-%Y") + ".xlsx"
    path = os.path.join(folder, file_name)

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["Student ID", "Status"])

    for student in all_students:
        status = "Present" if student in present_students else "Absent"
        ws.append([student, status])

    wb.save(path)
    messagebox.showinfo("Saved", f"Attendance saved to:\n{path}")

# -------- GUI --------
root = Tk()
root.title("QR Code Attendance System")

Button(root, text="➕ Add Student", width=25, command=add_student).pack(pady=10)
Button(root, text="📷 Start QR Attendance", width=25, command=scan_qr).pack(pady=10)

root.mainloop()
