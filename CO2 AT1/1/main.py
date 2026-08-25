import os

while True:

    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Create Tables")
    print("2. Add Book")
    print("3. View Books")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Add Member")
    print("7. Issue Book")
    print("8. Return Book")
    print("9. Inventory Report")
    print("10. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        os.system("python database/create_tables.py")

    elif choice == 2:
        os.system("python crud/add_book.py")

    elif choice == 3:
        os.system("python crud/view_books.py")

    elif choice == 4:
        os.system("python crud/update_book.py")

    elif choice == 5:
        os.system("python crud/delete_book.py")

    elif choice == 6:
        os.system("python crud/add_member.py")

    elif choice == 7:
        os.system("python crud/issue_book.py")

    elif choice == 8:
        os.system("python crud/return_book.py")

    elif choice == 9:
        os.system("python crud/inventory_report.py")

    elif choice == 10:
        print("Thank you!")
        break

    else:
        print("Invalid Choice")