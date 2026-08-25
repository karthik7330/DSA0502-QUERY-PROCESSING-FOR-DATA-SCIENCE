from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

cursor.execute("""
SELECT title,quantity
FROM Books
""")

rows=cursor.fetchall()

print("\nINVENTORY REPORT\n")

for row in rows:
    print(row)

conn.close()