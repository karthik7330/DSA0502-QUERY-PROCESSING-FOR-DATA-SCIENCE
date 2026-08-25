from utils.db_connection import get_connection
from utils.fine_calculator import calculate_fine

conn=get_connection()
cursor=conn.cursor()

transaction_id=int(input("Transaction ID : "))
return_date=input("Return Date (YYYY-MM-DD): ")

cursor.execute("""
SELECT issue_date,book_id
FROM Transactions
WHERE transaction_id=?
""",(transaction_id,))

row=cursor.fetchone()

issue_date=row[0]
book_id=row[1]

fine=calculate_fine(issue_date,return_date)

cursor.execute("""
UPDATE Transactions
SET return_date=?,fine=?
WHERE transaction_id=?
""",(return_date,fine,transaction_id))

cursor.execute("""
UPDATE Books
SET quantity=quantity+1
WHERE book_id=?
""",(book_id,))

conn.commit()

print("Book Returned")
print("Fine =",fine)

conn.close()