import sqlite3

DATABASE_NAME = "data/inventory.db"


# --------------------------------
# INVENTORY SUMMARY
# --------------------------------
def inventory_summary():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        # Total number of products
        cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)

        total_products = cursor.fetchone()[0]

        # Total stock units
        cursor.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM products
        """)

        total_stock = cursor.fetchone()[0]

        # Total inventory value
        cursor.execute("""
            SELECT COALESCE(
                SUM(quantity * COALESCE(purchase_price, 0)), 0
            )
            FROM products
        """)

        inventory_value = cursor.fetchone()[0]

        print("\n========== INVENTORY SUMMARY ==========")
        print(f"Total Products: {total_products}")
        print(f"Total Stock Units: {total_stock}")
        print(f"Total Inventory Value: ₹{inventory_value:.2f}")
        print("=======================================")

    finally:
        connection.close()


# --------------------------------
# LOW STOCK REPORT
# --------------------------------
def low_stock_report():

    try:
        limit = int(
            input("\nEnter low stock limit: ")
        )

        if limit < 0:
            print("Limit cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                quantity
            FROM products
            WHERE quantity <= ?
            ORDER BY quantity ASC
        """, (limit,))

        products = cursor.fetchall()

        print("\n========== LOW STOCK REPORT ==========")

        if not products:
            print("No products are currently below the selected limit.")
            return

        for product in products:

            print(
                f"ID: {product[0]} | "
                f"Product: {product[1]} | "
                f"Category: {product[2]} | "
                f"Stock: {product[3]}"
            )

        print("=======================================")

    finally:
        connection.close()


# --------------------------------
# PURCHASE SUMMARY
# --------------------------------
def purchase_summary():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        # Number of purchases
        cursor.execute("""
            SELECT COUNT(*)
            FROM purchases
        """)

        total_purchases = cursor.fetchone()[0]

        # Total quantity purchased
        cursor.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM purchases
        """)

        total_quantity = cursor.fetchone()[0]

        # Total purchase amount
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM purchases
        """)

        total_amount = cursor.fetchone()[0]

        print("\n========== PURCHASE SUMMARY ==========")
        print(f"Total Purchase Records: {total_purchases}")
        print(f"Total Units Purchased: {total_quantity}")
        print(f"Total Purchase Amount: ₹{total_amount:.2f}")
        print("======================================")

    finally:
        connection.close()


# --------------------------------
# STOCK MOVEMENT REPORT
# --------------------------------
def stock_movement_report():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

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

        print("\n========== STOCK MOVEMENT REPORT ==========")

        if not movements:
            print("No stock movements found.")
            return

        for movement in movements:

            print(
                f"\nMovement ID: {movement[0]}"
                f"\nProduct: {movement[1]}"
                f"\nType: {movement[2]}"
                f"\nQuantity: {movement[3]}"
                f"\nReference: {movement[4]}"
                f"\nDate: {movement[5]}"
            )

            print("-" * 45)

    finally:
        connection.close()


# --------------------------------
# PRODUCT VALUE REPORT
# --------------------------------
def product_value_report():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                quantity,
                purchase_price,
                quantity * COALESCE(purchase_price, 0)
            FROM products

            ORDER BY
                quantity * COALESCE(purchase_price, 0) DESC
        """)

        products = cursor.fetchall()

        print("\n========== PRODUCT VALUE REPORT ==========")

        if not products:
            print("No products found.")
            return

        for product in products:

            print(
                f"\nID: {product[0]}"
                f"\nProduct: {product[1]}"
                f"\nQuantity: {product[2]}"
                f"\nPurchase Price: ₹{product[3]:.2f}"
                f"\nStock Value: ₹{product[4]:.2f}"
            )

            print("-" * 45)

    finally:
        connection.close()


# --------------------------------
# MAIN MENU
# --------------------------------
def main():

    while True:

        print("\n========== REPORTS & DASHBOARD ==========")

        print("1. Inventory Summary")
        print("2. Low Stock Report")
        print("3. Purchase Summary")
        print("4. Stock Movement Report")
        print("5. Product Value Report")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            inventory_summary()

        elif choice == "2":
            low_stock_report()

        elif choice == "3":
            purchase_summary()

        elif choice == "4":
            stock_movement_report()

        elif choice == "5":
            product_value_report()

        elif choice == "6":
            print("Exiting Reports & Dashboard...")
            break

        else:
            print("Invalid choice. Please try again.")


# --------------------------------
# RUN PROGRAM
# --------------------------------
if __name__ == "__main__":
    main()