from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

book_id=int(input("Book ID : "))
quantity=int(input("New Quantity : "))

cursor.execute("""
UPDATE Books
SET quantity=?
WHERE book_id=?
""",(quantity,book_id))

conn.commit()

print("Book Updated Successfully")

conn.close()