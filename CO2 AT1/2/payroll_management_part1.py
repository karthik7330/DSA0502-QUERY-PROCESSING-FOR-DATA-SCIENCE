
# =====================================================
# Employee Payroll Management System - Part 1
# Database + Department CRUD + Employee CRUD
# Run this first.
# =====================================================

import sqlite3

conn = sqlite3.connect("payroll.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")

cur.executescript("""
CREATE TABLE IF NOT EXISTS Departments(
 DepartmentID INTEGER PRIMARY KEY,
 DepartmentName TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS Employees(
 EmployeeID INTEGER PRIMARY KEY,
 Name TEXT NOT NULL,
 DepartmentID INTEGER NOT NULL,
 Designation TEXT,
 Phone TEXT,
 FOREIGN KEY(DepartmentID) REFERENCES Departments(DepartmentID));

CREATE TABLE IF NOT EXISTS Attendance(
 AttendanceID INTEGER PRIMARY KEY,
 EmployeeID INTEGER,
 Month TEXT,
 DaysPresent INTEGER,
 FOREIGN KEY(EmployeeID) REFERENCES Employees(EmployeeID));

CREATE TABLE IF NOT EXISTS Salary(
 SalaryID INTEGER PRIMARY KEY,
 EmployeeID INTEGER,
 BasicSalary REAL,
 Bonus REAL,
 Tax REAL,
 FOREIGN KEY(EmployeeID) REFERENCES Employees(EmployeeID));

CREATE TABLE IF NOT EXISTS Payroll(
 PayrollID INTEGER PRIMARY KEY,
 EmployeeID INTEGER,
 Month TEXT,
 NetSalary REAL,
 FOREIGN KEY(EmployeeID) REFERENCES Employees(EmployeeID));
""")
conn.commit()

def seed_departments():
    cur.execute("SELECT COUNT(*) FROM Departments")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO Departments VALUES(?,?)",[
            (1,"Human Resources"),
            (2,"Finance"),
            (3,"Production"),
            (4,"Information Technology"),
            (5,"Sales")
        ])
        conn.commit()
        print("Default departments inserted.")

# -------- Department CRUD --------

def add_department():
    cur.execute("INSERT INTO Departments VALUES(?,?)",(
        int(input("Department ID: ")),
        input("Department Name: ")
    ))
    conn.commit()

def view_departments():
    for r in cur.execute("SELECT * FROM Departments"):
        print(r)

# -------- Employee CRUD --------

def add_employee():
    view_departments()
    dept = int(input("Choose Department ID: "))
    cur.execute("SELECT 1 FROM Departments WHERE DepartmentID=?", (dept,))
    if not cur.fetchone():
        print("Invalid Department ID.")
        return

    cur.execute("INSERT INTO Employees VALUES(?,?,?,?,?)",(
        int(input("Employee ID: ")),
        input("Employee Name: "),
        dept,
        input("Designation: "),
        input("Phone: ")
    ))
    conn.commit()
    print("Employee added.")

def view_employees():
    q="""SELECT E.EmployeeID,E.Name,D.DepartmentName,E.Designation,E.Phone
         FROM Employees E
         JOIN Departments D ON E.DepartmentID=D.DepartmentID"""
    for r in cur.execute(q):
        print(r)

seed_departments()
print("Part 1 ready.")
