-- ===========================================
-- EMPLOYEE PAYROLL MANAGEMENT SYSTEM
-- Database : SQLite
-- ===========================================

PRAGMA foreign_keys = ON;

-- ==========================
-- DEPARTMENTS TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS Departments
(
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName TEXT NOT NULL
);

-- ==========================
-- EMPLOYEES TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS Employees
(
    EmployeeID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    DepartmentID INTEGER,
    Designation TEXT,
    Phone TEXT,

    FOREIGN KEY (DepartmentID)
    REFERENCES Departments(DepartmentID)
);

-- ==========================
-- ATTENDANCE TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS Attendance
(
    AttendanceID INTEGER PRIMARY KEY,
    EmployeeID INTEGER,
    Month TEXT,
    DaysPresent INTEGER,

    FOREIGN KEY (EmployeeID)
    REFERENCES Employees(EmployeeID)
);

-- ==========================
-- SALARY TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS Salary
(
    SalaryID INTEGER PRIMARY KEY,
    EmployeeID INTEGER,
    BasicSalary REAL,
    Bonus REAL,
    Tax REAL,

    FOREIGN KEY (EmployeeID)
    REFERENCES Employees(EmployeeID)
);

-- ==========================
-- PAYROLL TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS Payroll
(
    PayrollID INTEGER PRIMARY KEY,
    EmployeeID INTEGER,
    Month TEXT,
    NetSalary REAL,

    FOREIGN KEY (EmployeeID)
    REFERENCES Employees(EmployeeID)
);

---------------------------------------------------
-- SAMPLE DATA
---------------------------------------------------

INSERT INTO Departments VALUES
(1,'Human Resources'),
(2,'Finance'),
(3,'Production'),
(4,'Information Technology'),
(5,'Sales');

INSERT INTO Employees VALUES
(101,'Rahul',1,'HR Executive','9876543210'),
(102,'Priya',2,'Accountant','9876501234'),
(103,'Karthik',4,'Software Engineer','9876512345'),
(104,'Anitha',3,'Production Supervisor','9876523456'),
(105,'Vijay',5,'Sales Executive','9876534567');

INSERT INTO Attendance VALUES
(1,101,'August',26),
(2,102,'August',28),
(3,103,'August',30),
(4,104,'August',27),
(5,105,'August',29);

INSERT INTO Salary VALUES
(1,101,35000,2000,1500),
(2,102,40000,3000,1800),
(3,103,55000,5000,2500),
(4,104,42000,2500,1700),
(5,105,38000,2200,1600);

INSERT INTO Payroll VALUES
(1,101,'August',35500),
(2,102,'August',41200),
(3,103,'August',57500),
(4,104,'August',42800),
(5,105,'August',38600);

---------------------------------------------------
-- CRUD OPERATIONS
---------------------------------------------------

-- CREATE
INSERT INTO Employees
VALUES
(106,'Suresh',4,'System Analyst','9876549876');

-- READ
SELECT * FROM Employees;

-- UPDATE
UPDATE Employees
SET Phone='9999988888'
WHERE EmployeeID=106;

-- DELETE
DELETE FROM Employees
WHERE EmployeeID=106;

---------------------------------------------------
-- REPORTS
---------------------------------------------------

-- Employee Details
SELECT
Employees.EmployeeID,
Employees.Name,
Departments.DepartmentName,
Employees.Designation
FROM Employees
JOIN Departments
ON Employees.DepartmentID = Departments.DepartmentID;

-- Attendance Report
SELECT
Employees.Name,
Attendance.Month,
Attendance.DaysPresent
FROM Attendance
JOIN Employees
ON Attendance.EmployeeID = Employees.EmployeeID;

-- Salary Report
SELECT
Employees.Name,
Salary.BasicSalary,
Salary.Bonus,
Salary.Tax
FROM Salary
JOIN Employees
ON Salary.EmployeeID = Employees.EmployeeID;

-- Payroll Report
SELECT
Employees.Name,
Payroll.Month,
Payroll.NetSalary
FROM Payroll
JOIN Employees
ON Payroll.EmployeeID = Employees.EmployeeID;

-- Department-wise Employee Count
SELECT
Departments.DepartmentName,
COUNT(Employees.EmployeeID) AS TotalEmployees
FROM Departments
LEFT JOIN Employees
ON Departments.DepartmentID = Employees.DepartmentID
GROUP BY Departments.DepartmentName;

-- Highest Net Salary
SELECT
Employees.Name,
Payroll.NetSalary
FROM Payroll
JOIN Employees
ON Payroll.EmployeeID = Employees.EmployeeID
ORDER BY Payroll.NetSalary DESC
LIMIT 1;
