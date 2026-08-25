from utils.db_connection import get_connection

conn=get_connection()
cursor=conn.cursor()

member_id=int(input("Member ID : "))
name=input("Name : ")
department=input("Department : ")
phone=input("Phone : ")

cursor.execute("""
INSERT INTO Members
VALUES(?,?,?,?)
""",(member_id,name,department,phone))

conn.commit()

print("Member Added Successfully")

conn.close()