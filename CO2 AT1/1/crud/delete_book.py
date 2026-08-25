from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

book_id=int(input("Book ID : "))

cursor.execute("""
DELETE FROM Books
WHERE book_id=?
""",(book_id,))

conn.commit()

print("Book Deleted Successfully")

conn.close()