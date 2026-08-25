from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

cursor.execute("SELECT * FROM Books")

rows=cursor.fetchall()

print("\nBOOK LIST\n")

for row in rows:
    print(row)

conn.close()