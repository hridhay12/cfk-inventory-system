import sqlite3

DATABASE_NAME = "data/inventory.db"


# --------------------------------
# STOCK IN
# --------------------------------
def stock_in():
    print("\n--- Stock In ---")

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter quantity received: "))
    except ValueError:
        print("\nPlease enter valid numbers.")
        return

    if quantity <= 0:
        print("\nQuantity must be greater than 0.")
        return

    reference = input("Enter reference/purchase number: ")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Check if product exists
    cursor.execute(
        "SELECT product_name, quantity FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        print("\nProduct not found.")
        connection.close()
        return

    product_name = product[0]
    current_quantity = product[1]

    # Increase product quantity
    new_quantity = current_quantity + quantity

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE product_id = ?
    """, (new_quantity, product_id))

    # Record stock movement
    cursor.execute("""
        INSERT INTO stock_movements
        (product_id, movement_type, quantity, reference)
        VALUES (?, 'IN', ?, ?)
    """, (product_id, quantity, reference))

    connection.commit()
    connection.close()

    print(f"\nStock added successfully!")
    print(f"Product: {product_name}")
    print(f"Previous stock: {current_quantity}")
    print(f"Added: {quantity}")
    print(f"New stock: {new_quantity}")


# --------------------------------
# STOCK OUT
# --------------------------------
def stock_out():
    print("\n--- Stock Out ---")

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter quantity issued/sold: "))
    except ValueError:
        print("\nPlease enter valid numbers.")
        return

    if quantity <= 0:
        print("\nQuantity must be greater than 0.")
        return

    reference = input("Enter reference/order number: ")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Get current stock
    cursor.execute(
        "SELECT product_name, quantity FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        print("\nProduct not found.")
        connection.close()
        return

    product_name = product[0]
    current_quantity = product[1]

    # Prevent negative stock
    if quantity > current_quantity:
        print("\nInsufficient stock!")
        print(f"Available stock: {current_quantity}")
        print(f"Requested: {quantity}")

        connection.close()
        return

    # Decrease stock
    new_quantity = current_quantity - quantity

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE product_id = ?
    """, (new_quantity, product_id))

    # Record movement
    cursor.execute("""
        INSERT INTO stock_movements
        (product_id, movement_type, quantity, reference)
        VALUES (?, 'OUT', ?, ?)
    """, (product_id, quantity, reference))

    connection.commit()
    connection.close()

    print(f"\nStock removed successfully!")
    print(f"Product: {product_name}")
    print(f"Previous stock: {current_quantity}")
    print(f"Removed: {quantity}")
    print(f"New stock: {new_quantity}")


# --------------------------------
# CURRENT STOCK
# --------------------------------
def view_current_stock():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, product_name, category,
               specification, quantity
        FROM products
        ORDER BY product_id
    """)

    products = cursor.fetchall()

    connection.close()

    print("\n--- Current Stock ---")

    if not products:
        print("No products found.")
        return

    for product in products:

        print(f"""
ID: {product[0]}
Product: {product[1]}
Category: {product[2]}
Specification: {product[3]}
Current Stock: {product[4]}
------------------------------
""")


# --------------------------------
# STOCK HISTORY
# --------------------------------
def view_stock_history():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stock_movements.movement_id,
            products.product_name,
            stock_movements.movement_type,
            stock_movements.quantity,
            stock_movements.reference,
            stock_movements.movement_date
        FROM stock_movements
        JOIN products
        ON stock_movements.product_id = products.product_id
        ORDER BY stock_movements.movement_id DESC
    """)

    movements = cursor.fetchall()

    connection.close()

    print("\n--- Stock Movement History ---")

    if not movements:
        print("No stock movements recorded yet.")
        return

    for movement in movements:

        print(f"""
Movement ID: {movement[0]}
Product: {movement[1]}
Type: {movement[2]}
Quantity: {movement[3]}
Reference: {movement[4]}
Date: {movement[5]}
------------------------------
""")


# --------------------------------
# MAIN MENU
# --------------------------------
if __name__ == "__main__":

    while True:

        print("\n================================")
        print("       STOCK MANAGEMENT")
        print("================================")
        print("1. Stock In")
        print("2. Stock Out")
        print("3. View Current Stock")
        print("4. View Stock History")
        print("5. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            stock_in()

        elif choice == "2":
            stock_out()

        elif choice == "3":
            view_current_stock()

        elif choice == "4":
            view_stock_history()

        elif choice == "5":
            print("\nExiting Stock Management...")
            break

        else:
            print("\nInvalid choice. Please select 1-5.")