from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

transaction_id=int(input("Transaction ID : "))
member_id=int(input("Member ID : "))
book_id=int(input("Book ID : "))
issue_date=input("Issue Date (YYYY-MM-DD): ")

cursor.execute("""
INSERT INTO Transactions
VALUES(?,?,?,?,?,?)
""",(transaction_id,member_id,book_id,issue_date,None,0))

cursor.execute("""
UPDATE Books
SET quantity=quantity-1
WHERE book_id=?
""",(book_id,))

conn.commit()

print("Book Issued Successfully")

conn.close()