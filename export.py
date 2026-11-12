import sqlite3
import pandas as pd
import os


DATABASE_NAME = "data/inventory.db"
EXPORT_FOLDER = "exports"


# --------------------------------
# CREATE EXPORT FOLDER
# --------------------------------
def create_export_folder():

    os.makedirs(EXPORT_FOLDER, exist_ok=True)


# --------------------------------
# EXPORT PRODUCTS
# --------------------------------
def export_products():

    connection = sqlite3.connect(DATABASE_NAME)

    try:

        query = """
            SELECT
                product_id,
                product_name,
                category,
                specification,
                supplier,
                purchase_price,
                selling_price,
                quantity,
                created_at
            FROM products
        """

        data = pd.read_sql_query(query, connection)

        filename = os.path.join(
            EXPORT_FOLDER,
            "products_report.xlsx"
        )

        data.to_excel(filename, index=False)

        print("\nProducts report exported successfully!")
        print(f"File: {filename}")

    finally:
        connection.close()


# --------------------------------
# EXPORT SUPPLIERS
# --------------------------------
def export_suppliers():

    connection = sqlite3.connect(DATABASE_NAME)

    try:

        query = """
            SELECT
                supplier_id,
                supplier_name,
                contact_person,
                phone,
                email,
                address,
                created_at
            FROM suppliers
        """

        data = pd.read_sql_query(query, connection)

        filename = os.path.join(
            EXPORT_FOLDER,
            "suppliers_report.xlsx"
        )

        data.to_excel(filename, index=False)

        print("\nSuppliers report exported successfully!")
        print(f"File: {filename}")

    finally:
        connection.close()


# --------------------------------
# EXPORT PURCHASES
# --------------------------------
def export_purchases():

    connection = sqlite3.connect(DATABASE_NAME)

    try:

        query = """
            SELECT
                purchases.purchase_id,
                products.product_name,
                products.category,
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
        """

        data = pd.read_sql_query(query, connection)

        filename = os.path.join(
            EXPORT_FOLDER,
            "purchases_report.xlsx"
        )

        data.to_excel(filename, index=False)

        print("\nPurchases report exported successfully!")
        print(f"File: {filename}")

    finally:
        connection.close()


# --------------------------------
# EXPORT STOCK MOVEMENTS
# --------------------------------
def export_stock_movements():

    connection = sqlite3.connect(DATABASE_NAME)

    try:

        query = """
            SELECT
                stock_movements.movement_id,
                products.product_name,
                products.category,
                stock_movements.movement_type,
                stock_movements.quantity,
                stock_movements.reference,
                stock_movements.movement_date

            FROM stock_movements

            JOIN products
            ON stock_movements.product_id = products.product_id

            ORDER BY stock_movements.movement_id DESC
        """

        data = pd.read_sql_query(query, connection)

        filename = os.path.join(
            EXPORT_FOLDER,
            "stock_movements_report.xlsx"
        )

        data.to_excel(filename, index=False)

        print("\nStock movement report exported successfully!")
        print(f"File: {filename}")

    finally:
        connection.close()


# --------------------------------
# EXPORT INVENTORY REPORT
# --------------------------------
def export_inventory():

    connection = sqlite3.connect(DATABASE_NAME)

    try:

        query = """
            SELECT
                product_id,
                product_name,
                category,
                specification,
                quantity,
                purchase_price,
                selling_price,

                quantity * COALESCE(purchase_price, 0)
                AS inventory_value

            FROM products

            ORDER BY product_name
        """

        data = pd.read_sql_query(query, connection)

        filename = os.path.join(
            EXPORT_FOLDER,
            "inventory_report.xlsx"
        )

        data.to_excel(filename, index=False)

        print("\nInventory report exported successfully!")
        print(f"File: {filename}")

    finally:
        connection.close()


# --------------------------------
# EXPORT ALL REPORTS
# --------------------------------
def export_all():

    print("\nExporting all reports...")

    export_products()
    export_suppliers()
    export_purchases()
    export_stock_movements()
    export_inventory()

    print("\nAll reports exported successfully!")


# --------------------------------
# MAIN MENU
# --------------------------------
def main():

    create_export_folder()

    while True:

        print("\n========== DATA EXPORT ==========")

        print("1. Export Products")
        print("2. Export Suppliers")
        print("3. Export Purchases")
        print("4. Export Stock Movements")
        print("5. Export Inventory Report")
        print("6. Export All Reports")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            export_products()

        elif choice == "2":
            export_suppliers()

        elif choice == "3":
            export_purchases()

        elif choice == "4":
            export_stock_movements()

        elif choice == "5":
            export_inventory()

        elif choice == "6":
            export_all()

        elif choice == "7":
            print("Exiting Data Export...")
            break

        else:
            print("Invalid choice. Please try again.")


# --------------------------------
# RUN PROGRAM
# --------------------------------
if __name__ == "__main__":
    main()