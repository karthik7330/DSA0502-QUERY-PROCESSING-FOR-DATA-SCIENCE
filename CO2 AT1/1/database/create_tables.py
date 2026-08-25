from utils.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Authors(
author_id INTEGER PRIMARY KEY,
author_name TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Publishers(
publisher_id INTEGER PRIMARY KEY,
publisher_name TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books(
book_id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
author_id INTEGER,
publisher_id INTEGER,
category TEXT,
quantity INTEGER,
FOREIGN KEY(author_id) REFERENCES Authors(author_id),
FOREIGN KEY(publisher_id) REFERENCES Publishers(publisher_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Members(
member_id INTEGER PRIMARY KEY,
member_name TEXT,
department TEXT,
phone TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions(
transaction_id INTEGER PRIMARY KEY,
member_id INTEGER,
book_id INTEGER,
issue_date TEXT,
return_date TEXT,
fine REAL,
FOREIGN KEY(member_id) REFERENCES Members(member_id),
FOREIGN KEY(book_id) REFERENCES Books(book_id))
""")

conn.commit()
conn.close()

print("Tables Created Successfully")