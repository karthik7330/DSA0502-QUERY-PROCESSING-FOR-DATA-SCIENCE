from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

book_id=int(input("Book ID : "))
title=input("Title : ")
author_id=int(input("Author ID : "))
publisher_id=int(input("Publisher ID : "))
category=input("Category : ")
quantity=int(input("Quantity : "))

cursor.execute("""
INSERT INTO Books
VALUES(?,?,?,?,?,?)
""",(book_id,title,author_id,publisher_id,category,quantity))

conn.commit()

print("Book Added Successfully")

conn.close()