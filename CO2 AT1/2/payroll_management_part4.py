
# =====================================================
# Employee Payroll Management System - Part 4
# Reports + Main Menu Template
# =====================================================

import sqlite3

conn = sqlite3.connect("payroll.db")
cur = conn.cursor()

def department_employee_report():
    q = """
    SELECT D.DepartmentName, COUNT(E.EmployeeID)
    FROM Departments D
    LEFT JOIN Employees E ON D.DepartmentID=E.DepartmentID
    GROUP BY D.DepartmentID
    """
    for r in cur.execute(q):
        print(r)

def attendance_report():
    q = """
    SELECT E.Name,A.Month,A.DaysPresent
    FROM Attendance A
    JOIN Employees E ON A.EmployeeID=E.EmployeeID
    """
    for r in cur.execute(q):
        print(r)

def salary_report():
    q = """
    SELECT E.Name,S.BasicSalary,S.Bonus,S.Tax
    FROM Salary S
    JOIN Employees E ON S.EmployeeID=E.EmployeeID
    """
    for r in cur.execute(q):
        print(r)

def payroll_report():
    q = """
    SELECT E.Name,P.Month,P.NetSalary
    FROM Payroll P
    JOIN Employees E ON P.EmployeeID=E.EmployeeID
    """
    for r in cur.execute(q):
        print(r)

def highest_salary():
    q = """
    SELECT E.Name,P.NetSalary
    FROM Payroll P
    JOIN Employees E ON P.EmployeeID=E.EmployeeID
    ORDER BY P.NetSalary DESC
    LIMIT 1
    """
    row = cur.execute(q).fetchone()
    print(row if row else "No payroll records.")

def reports_menu():
    while True:
        print("""
========= REPORTS =========
1. Department-wise Employees
2. Attendance Report
3. Salary Report
4. Payroll Report
5. Highest Salary
6. Exit
""")
        ch=input("Choice: ")
        if ch=="1":
            department_employee_report()
        elif ch=="2":
            attendance_report()
        elif ch=="3":
            salary_report()
        elif ch=="4":
            payroll_report()
        elif ch=="5":
            highest_salary()
        elif ch=="6":
            break
        else:
            print("Invalid Choice")

if __name__=="__main__":
    print("Import Parts 1-3, then call reports_menu().")
