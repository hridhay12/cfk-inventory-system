import sqlite3

DATABASE_NAME = "data/inventory.db"


# -------------------------------
# ADD PRODUCT
# -------------------------------
def add_product():
    print("\n--- Add New Product ---")

    product_name = input("Product name: ")
    category = input("Category: ")
    specification = input("Specification: ")
    supplier = input("Supplier: ")

    try:
        purchase_price = float(input("Purchase price: "))
        selling_price = float(input("Selling price: "))
        quantity = int(input("Initial quantity: "))
    except ValueError:
        print("\nInvalid input! Price must be a number and quantity must be a whole number.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (product_name, category, specification, supplier,
         purchase_price, selling_price, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        product_name,
        category,
        specification,
        supplier,
        purchase_price,
        selling_price,
        quantity
    ))

    connection.commit()
    connection.close()

    print("\nProduct added successfully!")


# -------------------------------
# VIEW ALL PRODUCTS
# -------------------------------
def view_products():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    print("\n--- Product List ---")

    if not products:
        print("No products found.")
        return

    for product in products:
        print(f"""
ID: {product[0]}
Product: {product[1]}
Category: {product[2]}
Specification: {product[3]}
Supplier: {product[4]}
Purchase Price: ₹{product[5]}
Selling Price: ₹{product[6]}
Quantity: {product[7]}
Created: {product[8]}
------------------------------
""")


# -------------------------------
# SEARCH PRODUCT
# -------------------------------
def search_product():
    print("\n--- Search Product ---")

    search = input("Enter product name or category: ")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE product_name LIKE ?
        OR category LIKE ?
    """, (f"%{search}%", f"%{search}%"))

    products = cursor.fetchall()

    connection.close()

    if not products:
        print("\nNo matching products found.")
        return

    print("\n--- Search Results ---")

    for product in products:
        print(f"""
ID: {product[0]}
Product: {product[1]}
Category: {product[2]}
Specification: {product[3]}
Supplier: {product[4]}
Purchase Price: ₹{product[5]}
Selling Price: ₹{product[6]}
Quantity: {product[7]}
------------------------------
""")


# -------------------------------
# EDIT PRODUCT
# -------------------------------
def edit_product():
    print("\n--- Edit Product ---")

    try:
        product_id = int(input("Enter Product ID to edit: "))
    except ValueError:
        print("\nInvalid Product ID.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        print("\nProduct not found.")
        connection.close()
        return

    print("\nCurrent Product Details:")
    print(f"Product Name: {product[1]}")
    print(f"Category: {product[2]}")
    print(f"Specification: {product[3]}")
    print(f"Supplier: {product[4]}")
    print(f"Purchase Price: ₹{product[5]}")
    print(f"Selling Price: ₹{product[6]}")
    print(f"Quantity: {product[7]}")

    print("\nEnter new details.")
    print("Press Enter to keep the existing value.")

    product_name = input(f"Product name [{product[1]}]: ") or product[1]
    category = input(f"Category [{product[2]}]: ") or product[2]
    specification = input(
        f"Specification [{product[3]}]: "
    ) or product[3]

    supplier = input(
        f"Supplier [{product[4]}]: "
    ) or product[4]

    purchase_input = input(
        f"Purchase price [{product[5]}]: "
    )

    selling_input = input(
        f"Selling price [{product[6]}]: "
    )

    quantity_input = input(
        f"Quantity [{product[7]}]: "
    )

    try:
        purchase_price = (
            float(purchase_input)
            if purchase_input
            else product[5]
        )

        selling_price = (
            float(selling_input)
            if selling_input
            else product[6]
        )

        quantity = (
            int(quantity_input)
            if quantity_input
            else product[7]
        )

    except ValueError:
        print("\nInvalid number entered. Product was not changed.")
        connection.close()
        return

    cursor.execute("""
        UPDATE products
        SET product_name = ?,
            category = ?,
            specification = ?,
            supplier = ?,
            purchase_price = ?,
            selling_price = ?,
            quantity = ?
        WHERE product_id = ?
    """, (
        product_name,
        category,
        specification,
        supplier,
        purchase_price,
        selling_price,
        quantity,
        product_id
    ))

    connection.commit()
    connection.close()

    print("\nProduct updated successfully!")


# -------------------------------
# DELETE PRODUCT
# -------------------------------
def delete_product():
    print("\n--- Delete Product ---")

    try:
        product_id = int(input("Enter Product ID to delete: "))
    except ValueError:
        print("\nInvalid Product ID.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT product_name FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        print("\nProduct not found.")
        connection.close()
        return

    print(f"\nProduct found: {product[0]}")

    confirmation = input(
        "Are you sure you want to delete it? (yes/no): "
    ).lower()

    if confirmation == "yes":

        cursor.execute(
            "DELETE FROM products WHERE product_id = ?",
            (product_id,)
        )

        connection.commit()

        print("\nProduct deleted successfully!")

    else:
        print("\nDelete cancelled.")

    connection.close()


# -------------------------------
# MAIN MENU
# -------------------------------
if __name__ == "__main__":

    while True:

        print("\n================================")
        print("     CFK INVENTORY SYSTEM")
        print("================================")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Edit Product")
        print("5. Delete Product")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            search_product()

        elif choice == "4":
            edit_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            print("\nThank you for using CFK Inventory System!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")