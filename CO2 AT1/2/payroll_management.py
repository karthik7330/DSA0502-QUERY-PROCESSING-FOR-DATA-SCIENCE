
import sqlite3

conn=sqlite3.connect("payroll.db")
cur=conn.cursor()

cur.executescript("""
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS Departments(
 DepartmentID INTEGER PRIMARY KEY,
 DepartmentName TEXT);

CREATE TABLE IF NOT EXISTS Employees(
 EmployeeID INTEGER PRIMARY KEY,
 Name TEXT,
 DepartmentID INTEGER,
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

def add_employee():
    data=(int(input("Employee ID: ")),input("Name: "),
          int(input("Department ID: ")),input("Designation: "),
          input("Phone: "))
    cur.execute("INSERT INTO Employees VALUES(?,?,?,?,?)",data)
    conn.commit()
    print("Employee added.")

def view_employees():
    for r in cur.execute("SELECT * FROM Employees"):
        print(r)

def add_salary():
    sid=int(input("Salary ID: "))
    eid=int(input("Employee ID: "))
    basic=float(input("Basic Salary: "))
    bonus=float(input("Bonus: "))
    tax=float(input("Tax: "))
    cur.execute("INSERT INTO Salary VALUES(?,?,?,?,?)",(sid,eid,basic,bonus,tax))
    conn.commit()

def generate_payroll():
    pid=int(input("Payroll ID: "))
    eid=int(input("Employee ID: "))
    month=input("Month: ")
    cur.execute("SELECT BasicSalary,Bonus,Tax FROM Salary WHERE EmployeeID=?",(eid,))
    row=cur.fetchone()
    if not row:
        print("Salary record not found.")
        return
    net=row[0]+row[1]-row[2]
    cur.execute("INSERT INTO Payroll VALUES(?,?,?,?)",(pid,eid,month,net))
    conn.commit()
    print("Payroll generated. Net Salary =",net)

def payroll_report():
    q="""SELECT Employees.Name,Payroll.Month,Payroll.NetSalary
         FROM Payroll JOIN Employees
         ON Payroll.EmployeeID=Employees.EmployeeID"""
    for r in cur.execute(q):
        print(r)

while True:
    print("""
==== Employee Payroll System ====
1. Add Employee
2. View Employees
3. Add Salary
4. Generate Payroll
5. Payroll Report
6. Exit
""")
    ch=input("Choice: ")
    if ch=="1": add_employee()
    elif ch=="2": view_employees()
    elif ch=="3": add_salary()
    elif ch=="4": generate_payroll()
    elif ch=="5": payroll_report()
    elif ch=="6": break
    else: print("Invalid choice")

conn.close()
