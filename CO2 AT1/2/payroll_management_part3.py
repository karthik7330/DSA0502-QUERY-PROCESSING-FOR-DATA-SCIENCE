
# =====================================================
# Employee Payroll Management System - Part 3
# Payroll Generation + Search
# =====================================================

import sqlite3

conn=sqlite3.connect("payroll.db")
cur=conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")

def generate_payroll():
    eid=int(input("Employee ID: "))
    month=input("Month: ")

    cur.execute("SELECT Name FROM Employees WHERE EmployeeID=?",(eid,))
    emp=cur.fetchone()
    if not emp:
        print("Employee not found.")
        return

    cur.execute("SELECT BasicSalary,Bonus,Tax FROM Salary WHERE EmployeeID=?",(eid,))
    sal=cur.fetchone()
    if not sal:
        print("Salary record not found.")
        return

    basic,bonus,tax=sal
    net=basic+bonus-tax

    cur.execute("SELECT COALESCE(MAX(PayrollID),0)+1 FROM Payroll")
    pid=cur.fetchone()[0]

    cur.execute("INSERT INTO Payroll VALUES(?,?,?,?)",(pid,eid,month,net))
    conn.commit()

    print("\nPayroll Generated")
    print("Employee :",emp[0])
    print("Basic    :",basic)
    print("Bonus    :",bonus)
    print("Tax      :",tax)
    print("Net Salary:",net)

def view_payroll():
    q="""
    SELECT P.PayrollID,E.Name,P.Month,P.NetSalary
    FROM Payroll P
    JOIN Employees E
    ON P.EmployeeID=E.EmployeeID
    ORDER BY P.PayrollID
    """
    for r in cur.execute(q):
        print(r)

def search_employee():
    name=input("Employee Name: ")
    q="""
    SELECT E.EmployeeID,E.Name,D.DepartmentName,E.Designation,E.Phone
    FROM Employees E
    JOIN Departments D
    ON E.DepartmentID=D.DepartmentID
    WHERE E.Name LIKE ?
    """
    rows=cur.execute(q,('%'+name+'%',)).fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("No employee found.")

def search_payroll():
    eid=int(input("Employee ID: "))
    q="""
    SELECT P.PayrollID,P.Month,P.NetSalary
    FROM Payroll P
    WHERE P.EmployeeID=?
    """
    rows=cur.execute(q,(eid,)).fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("No payroll record found.")

print("Part 3 ready.")
