
# =====================================================
# Employee Payroll Management System - Part 2
# Attendance CRUD + Salary CRUD
# =====================================================

import sqlite3

conn = sqlite3.connect("payroll.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")

def view_employees():
    for r in cur.execute("SELECT EmployeeID,Name FROM Employees"):
        print(r)

# ---------------- Attendance ----------------

def add_attendance():
    view_employees()
    eid = int(input("Employee ID: "))
    cur.execute("SELECT 1 FROM Employees WHERE EmployeeID=?", (eid,))
    if not cur.fetchone():
        print("Invalid Employee ID")
        return

    cur.execute(
        "INSERT INTO Attendance VALUES(?,?,?,?)",
        (
            int(input("Attendance ID: ")),
            eid,
            input("Month: "),
            int(input("Days Present: "))
        )
    )
    conn.commit()
    print("Attendance added.")

def view_attendance():
    q = """
    SELECT A.AttendanceID,E.Name,A.Month,A.DaysPresent
    FROM Attendance A
    JOIN Employees E
    ON A.EmployeeID=E.EmployeeID
    """
    for r in cur.execute(q):
        print(r)

def update_attendance():
    aid = int(input("Attendance ID: "))
    days = int(input("New Days Present: "))
    cur.execute(
        "UPDATE Attendance SET DaysPresent=? WHERE AttendanceID=?",
        (days, aid)
    )
    conn.commit()
    print("Attendance updated.")

def delete_attendance():
    aid = int(input("Attendance ID: "))
    cur.execute("DELETE FROM Attendance WHERE AttendanceID=?", (aid,))
    conn.commit()
    print("Attendance deleted.")

# ---------------- Salary ----------------

def add_salary():
    view_employees()
    eid = int(input("Employee ID: "))
    cur.execute("SELECT 1 FROM Employees WHERE EmployeeID=?", (eid,))
    if not cur.fetchone():
        print("Invalid Employee ID")
        return

    cur.execute(
        "INSERT INTO Salary VALUES(?,?,?,?,?)",
        (
            int(input("Salary ID: ")),
            eid,
            float(input("Basic Salary: ")),
            float(input("Bonus: ")),
            float(input("Tax: "))
        )
    )
    conn.commit()
    print("Salary added.")

def view_salary():
    q = """
    SELECT S.SalaryID,E.Name,S.BasicSalary,S.Bonus,S.Tax
    FROM Salary S
    JOIN Employees E
    ON S.EmployeeID=E.EmployeeID
    """
    for r in cur.execute(q):
        print(r)

def update_salary():
    sid = int(input("Salary ID: "))
    basic = float(input("New Basic Salary: "))
    bonus = float(input("New Bonus: "))
    tax = float(input("New Tax: "))
    cur.execute(
        "UPDATE Salary SET BasicSalary=?,Bonus=?,Tax=? WHERE SalaryID=?",
        (basic, bonus, tax, sid)
    )
    conn.commit()
    print("Salary updated.")

def delete_salary():
    sid = int(input("Salary ID: "))
    cur.execute("DELETE FROM Salary WHERE SalaryID=?", (sid,))
    conn.commit()
    print("Salary deleted.")

print("Part 2 ready.")
