import sqlite3

DATABASE_NAME = "data/inventory.db"


# --------------------------------
# CREATE PURCHASE
# --------------------------------
def create_purchase():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        # Show available products
        print("\n--- Available Products ---")

        cursor.execute("""
            SELECT product_id, product_name, category, quantity
            FROM products
        """)

        products = cursor.fetchall()

        if not products:
            print("No products found.")
            return

        for product in products:
            print(
                f"ID: {product[0]} | "
                f"{product[1]} | "
                f"Category: {product[2]} | "
                f"Stock: {product[3]}"
            )

        # Product selection
        product_id = int(input("\nEnter Product ID: "))

        cursor.execute("""
            SELECT product_id, product_name
            FROM products
            WHERE product_id = ?
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            print("Product not found.")
            return

        # Show suppliers
        print("\n--- Available Suppliers ---")

        cursor.execute("""
            SELECT supplier_id, supplier_name
            FROM suppliers
        """)

        suppliers = cursor.fetchall()

        if not suppliers:
            print("No suppliers found.")
            return

        for supplier in suppliers:
            print(
                f"ID: {supplier[0]} | "
                f"{supplier[1]}"
            )

        # Supplier selection
        supplier_id = int(input("\nEnter Supplier ID: "))

        cursor.execute("""
            SELECT supplier_id, supplier_name
            FROM suppliers
            WHERE supplier_id = ?
        """, (supplier_id,))

        supplier = cursor.fetchone()

        if not supplier:
            print("Supplier not found.")
            return

        # Quantity
        quantity = int(input("Enter Purchase Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        # Purchase price
        purchase_price = float(
            input("Enter Purchase Price per Unit: ")
        )

        if purchase_price < 0:
            print("Purchase price cannot be negative.")
            return

        # Calculate total
        total_amount = quantity * purchase_price

        print("\n--- Purchase Summary ---")
        print(f"Product: {product[1]}")
        print(f"Supplier: {supplier[1]}")
        print(f"Quantity: {quantity}")
        print(f"Price per Unit: ₹{purchase_price:.2f}")
        print(f"Total Amount: ₹{total_amount:.2f}")

        confirm = input("\nConfirm purchase? (y/n): ").lower()

        if confirm != "y":
            print("Purchase cancelled.")
            return

        # --------------------------------
        # INSERT PURCHASE
        # --------------------------------
        cursor.execute("""
            INSERT INTO purchases
            (
                product_id,
                supplier_id,
                quantity,
                purchase_price,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_id,
            supplier_id,
            quantity,
            purchase_price,
            total_amount
        ))

        # --------------------------------
        # UPDATE PRODUCT STOCK
        # --------------------------------
        cursor.execute("""
            UPDATE products
            SET quantity = quantity + ?
            WHERE product_id = ?
        """, (quantity, product_id))

        # --------------------------------
        # RECORD STOCK MOVEMENT
        # --------------------------------
        cursor.execute("""
            INSERT INTO stock_movements
            (
                product_id,
                movement_type,
                quantity,
                reference
            )
            VALUES (?, 'IN', ?, ?)
        """, (
            product_id,
            quantity,
            "Purchase"
        ))

        connection.commit()

        print("\nPurchase recorded successfully!")
        print(f"Stock increased by {quantity}.")
        print(f"Total purchase amount: ₹{total_amount:.2f}")

    except ValueError:
        print("Please enter valid numerical values.")

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        connection.close()


# --------------------------------
# VIEW PURCHASES
# --------------------------------
def view_purchases():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                purchases.purchase_id,
                products.product_name,
                suppliers.supplier_name,
                purchases.quantity,
                purchases.purchase_price,
                purchases.total_amount,
                purchases.purchase_date
            FROM purchases

            JOIN products
            ON purchases.product_id = products.product_id

            JOIN suppliers
            ON purchases.supplier_id = suppliers.supplier_id

            ORDER BY purchases.purchase_id DESC
        """)

        purchases = cursor.fetchall()

        if not purchases:
            print("\nNo purchases found.")
            return

        print("\n--- Purchase Records ---")

        for purchase in purchases:

            print(
                f"\nPurchase ID: {purchase[0]}"
                f"\nProduct: {purchase[1]}"
                f"\nSupplier: {purchase[2]}"
                f"\nQuantity: {purchase[3]}"
                f"\nPrice per Unit: ₹{purchase[4]:.2f}"
                f"\nTotal Amount: ₹{purchase[5]:.2f}"
                f"\nDate: {purchase[6]}"
            )

            print("-" * 40)

    finally:
        connection.close()


# --------------------------------
# SEARCH PURCHASES
# --------------------------------
def search_purchases():

    search = input(
        "\nEnter product or supplier name to search: "
    ).strip()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                purchases.purchase_id,
                products.product_name,
                suppliers.supplier_name,
                purchases.quantity,
                purchases.purchase_price,
                purchases.total_amount,
                purchases.purchase_date

            FROM purchases

            JOIN products
            ON purchases.product_id = products.product_id

            JOIN suppliers
            ON purchases.supplier_id = suppliers.supplier_id

            WHERE products.product_name LIKE ?
               OR suppliers.supplier_name LIKE ?

            ORDER BY purchases.purchase_id DESC
        """, (
            f"%{search}%",
            f"%{search}%"
        ))

        purchases = cursor.fetchall()

        if not purchases:
            print("\nNo matching purchases found.")
            return

        print("\n--- Search Results ---")

        for purchase in purchases:

            print(
                f"\nPurchase ID: {purchase[0]}"
                f"\nProduct: {purchase[1]}"
                f"\nSupplier: {purchase[2]}"
                f"\nQuantity: {purchase[3]}"
                f"\nPurchase Price: ₹{purchase[4]:.2f}"
                f"\nTotal: ₹{purchase[5]:.2f}"
                f"\nDate: {purchase[6]}"
            )

            print("-" * 40)

    finally:
        connection.close()


# --------------------------------
# VIEW PURCHASE DETAILS
# --------------------------------
def purchase_details():

    try:
        purchase_id = int(
            input("\nEnter Purchase ID: ")
        )
    except ValueError:
        print("Invalid Purchase ID.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                purchases.purchase_id,
                products.product_name,
                products.category,
                products.specification,
                suppliers.supplier_name,
                suppliers.contact_person,
                suppliers.phone,
                purchases.quantity,
                purchases.purchase_price,
                purchases.total_amount,
                purchases.purchase_date

            FROM purchases

            JOIN products
            ON purchases.product_id = products.product_id

            JOIN suppliers
            ON purchases.supplier_id = suppliers.supplier_id

            WHERE purchases.purchase_id = ?
        """, (purchase_id,))

        purchase = cursor.fetchone()

        if not purchase:
            print("Purchase not found.")
            return

        print("\n========== PURCHASE DETAILS ==========")

        print(f"Purchase ID: {purchase[0]}")
        print(f"Product: {purchase[1]}")
        print(f"Category: {purchase[2]}")
        print(f"Specification: {purchase[3]}")
        print(f"Supplier: {purchase[4]}")
        print(f"Contact Person: {purchase[5]}")
        print(f"Supplier Phone: {purchase[6]}")
        print(f"Quantity: {purchase[7]}")
        print(f"Purchase Price: ₹{purchase[8]:.2f}")
        print(f"Total Amount: ₹{purchase[9]:.2f}")
        print(f"Purchase Date: {purchase[10]}")

        print("======================================")

    finally:
        connection.close()


# --------------------------------
# MAIN MENU
# --------------------------------
def main():

    while True:

        print("\n========== PURCHASE MANAGEMENT ==========")

        print("1. Create Purchase")
        print("2. View Purchases")
        print("3. Search Purchases")
        print("4. View Purchase Details")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_purchase()

        elif choice == "2":
            view_purchases()

        elif choice == "3":
            search_purchases()

        elif choice == "4":
            purchase_details()

        elif choice == "5":
            print("Exiting Purchase Management...")
            break

        else:
            print("Invalid choice. Please try again.")


# --------------------------------
# RUN PROGRAM
# --------------------------------
if __name__ == "__main__":
    main()