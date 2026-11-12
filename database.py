import sqlite3
import os

DATABASE_NAME = "data/inventory.db"


def create_database():

    # Create data folder if it does not exist
    os.makedirs("data", exist_ok=True)

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # --------------------------------
    # PRODUCTS TABLE
    # --------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            specification TEXT,
            supplier TEXT,
            purchase_price REAL,
            selling_price REAL,
            quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------
    # STOCK MOVEMENTS TABLE
    # --------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_movements (
            movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            movement_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            reference TEXT,
            movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (product_id)
            REFERENCES products(product_id)
        )
    """)

    # --------------------------------
    # SUPPLIERS TABLE
    # --------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # --------------------------------
    # PURCHASES TABLE
    # --------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (product_id)
            REFERENCES products(product_id),

            FOREIGN KEY (supplier_id)
            REFERENCES suppliers(supplier_id)
        )
    """)

        # Save changes
    connection.commit()

    # Close database connection
    connection.close()


# --------------------------------
# RUN DATABASE SETUP
# --------------------------------
if __name__ == "__main__":

    create_database()

    print("Database created successfully!")
    print("Tables available:")
    print("- products")
    print("- stock_movements")
    print("- suppliers")
    print("- purchases")