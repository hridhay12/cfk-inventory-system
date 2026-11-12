import sqlite3

DATABASE_NAME = "data/inventory.db"


# --------------------------------
# ADD SUPPLIER
# --------------------------------
def add_supplier():

    print("\n--- Add New Supplier ---")

    supplier_name = input("Supplier name: ")
    contact_person = input("Contact person: ")
    phone = input("Phone number: ")
    email = input("Email: ")
    address = input("Address: ")

    if not supplier_name:
        print("\nSupplier name cannot be empty.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO suppliers
        (supplier_name, contact_person, phone, email, address)
        VALUES (?, ?, ?, ?, ?)
    """, (
        supplier_name,
        contact_person,
        phone,
        email,
        address
    ))

    connection.commit()
    connection.close()

    print("\nSupplier added successfully!")


# --------------------------------
# VIEW SUPPLIERS
# --------------------------------
def view_suppliers():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    connection.close()

    print("\n--- Supplier List ---")

    if not suppliers:
        print("No suppliers found.")
        return

    for supplier in suppliers:

        print(f"""
Supplier ID: {supplier[0]}
Supplier Name: {supplier[1]}
Contact Person: {supplier[2]}
Phone: {supplier[3]}
Email: {supplier[4]}
Address: {supplier[5]}
Created: {supplier[6]}
------------------------------
""")


# --------------------------------
# SEARCH SUPPLIER
# --------------------------------
def search_supplier():

    print("\n--- Search Supplier ---")

    search = input("Enter supplier name or phone: ")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM suppliers
        WHERE supplier_name LIKE ?
        OR phone LIKE ?
    """, (
        f"%{search}%",
        f"%{search}%"
    ))

    suppliers = cursor.fetchall()

    connection.close()

    if not suppliers:
        print("\nNo matching suppliers found.")
        return

    print("\n--- Search Results ---")

    for supplier in suppliers:

        print(f"""
Supplier ID: {supplier[0]}
Supplier Name: {supplier[1]}
Contact Person: {supplier[2]}
Phone: {supplier[3]}
Email: {supplier[4]}
Address: {supplier[5]}
------------------------------
""")


# --------------------------------
# EDIT SUPPLIER
# --------------------------------
def edit_supplier():

    print("\n--- Edit Supplier ---")

    try:
        supplier_id = int(input("Enter Supplier ID to edit: "))
    except ValueError:
        print("\nInvalid Supplier ID.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM suppliers WHERE supplier_id = ?",
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if not supplier:
        print("\nSupplier not found.")
        connection.close()
        return

    print("\nCurrent Supplier Details:")
    print(f"Supplier Name: {supplier[1]}")
    print(f"Contact Person: {supplier[2]}")
    print(f"Phone: {supplier[3]}")
    print(f"Email: {supplier[4]}")
    print(f"Address: {supplier[5]}")

    print("\nEnter new details.")
    print("Press Enter to keep the existing value.")

    supplier_name = (
        input(f"Supplier name [{supplier[1]}]: ")
        or supplier[1]
    )

    contact_person = (
        input(f"Contact person [{supplier[2]}]: ")
        or supplier[2]
    )

    phone = (
        input(f"Phone [{supplier[3]}]: ")
        or supplier[3]
    )

    email = (
        input(f"Email [{supplier[4]}]: ")
        or supplier[4]
    )

    address = (
        input(f"Address [{supplier[5]}]: ")
        or supplier[5]
    )

    cursor.execute("""
        UPDATE suppliers
        SET supplier_name = ?,
            contact_person = ?,
            phone = ?,
            email = ?,
            address = ?
        WHERE supplier_id = ?
    """, (
        supplier_name,
        contact_person,
        phone,
        email,
        address,
        supplier_id
    ))

    connection.commit()
    connection.close()

    print("\nSupplier updated successfully!")


# --------------------------------
# DELETE SUPPLIER
# --------------------------------
def delete_supplier():

    print("\n--- Delete Supplier ---")

    try:
        supplier_id = int(input("Enter Supplier ID to delete: "))
    except ValueError:
        print("\nInvalid Supplier ID.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT supplier_name FROM suppliers WHERE supplier_id = ?",
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if not supplier:
        print("\nSupplier not found.")
        connection.close()
        return

    print(f"\nSupplier found: {supplier[0]}")

    confirmation = input(
        "Are you sure you want to delete it? (yes/no): "
    ).lower()

    if confirmation == "yes":

        cursor.execute(
            "DELETE FROM suppliers WHERE supplier_id = ?",
            (supplier_id,)
        )

        connection.commit()

        print("\nSupplier deleted successfully!")

    else:
        print("\nDelete cancelled.")

    connection.close()


# --------------------------------
# MAIN MENU
# --------------------------------
if __name__ == "__main__":

    while True:

        print("\n================================")
        print("       SUPPLIER MANAGEMENT")
        print("================================")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Search Supplier")
        print("4. Edit Supplier")
        print("5. Delete Supplier")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_supplier()

        elif choice == "2":
            view_suppliers()

        elif choice == "3":
            search_supplier()

        elif choice == "4":
            edit_supplier()

        elif choice == "5":
            delete_supplier()

        elif choice == "6":
            print("\nExiting Supplier Management...")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")