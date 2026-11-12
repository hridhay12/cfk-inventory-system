import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd


# ============================================================
# DATABASE
# ============================================================

DATABASE_NAME = "data/inventory.db"
EXPORT_FOLDER = "exports"


def connect_database():
    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# DASHBOARD
# ============================================================

def get_database_values():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM products"
    )
    total_stock = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE quantity <= 10"
    )
    low_stock = cursor.fetchone()[0]

    conn.close()

    return (
        total_products,
        total_suppliers,
        total_stock,
        low_stock
    )


def update_dashboard():

    total_products, total_suppliers, total_stock, low_stock = \
        get_database_values()

    products_value.config(
        text=str(total_products)
    )

    suppliers_value.config(
        text=str(total_suppliers)
    )

    stock_value.config(
        text=str(total_stock)
    )

    low_stock_value.config(
        text=str(low_stock)
    )


# ============================================================
# PRODUCTS
# ============================================================

def open_products():

    window = tk.Toplevel(root)
    window.title("Products Management")
    window.geometry("1100x650")

    product_name_var = tk.StringVar()
    category_var = tk.StringVar()
    specification_var = tk.StringVar()
    supplier_var = tk.StringVar()
    purchase_price_var = tk.StringVar()
    selling_price_var = tk.StringVar()
    quantity_var = tk.StringVar()
    search_var = tk.StringVar()

    # --------------------------------------------------------
    # Clear fields
    # --------------------------------------------------------

    def clear_fields():

        product_name_var.set("")
        category_var.set("")
        specification_var.set("")
        supplier_var.set("")
        purchase_price_var.set("")
        selling_price_var.set("")
        quantity_var.set("")

    # --------------------------------------------------------
    # Load products
    # --------------------------------------------------------

    def load_products(search=""):

        for item in product_tree.get_children():
            product_tree.delete(item)

        conn = connect_database()
        cursor = conn.cursor()

        if search:

            cursor.execute("""
                SELECT product_id,
                       product_name,
                       category,
                       specification,
                       supplier,
                       purchase_price,
                       selling_price,
                       quantity
                FROM products
                WHERE product_name LIKE ?
                   OR category LIKE ?
                   OR supplier LIKE ?
                ORDER BY product_id
            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""
                SELECT product_id,
                       product_name,
                       category,
                       specification,
                       supplier,
                       purchase_price,
                       selling_price,
                       quantity
                FROM products
                ORDER BY product_id
            """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            product_tree.insert(
                "",
                tk.END,
                values=row
            )

    # --------------------------------------------------------
    # Add product
    # --------------------------------------------------------

    def add_product():

        if not product_name_var.get().strip():

            messagebox.showerror(
                "Error",
                "Product name is required."
            )

            return

        try:

            purchase_price = float(
                purchase_price_var.get()
            )

            selling_price = float(
                selling_price_var.get()
            )

            quantity = int(
                quantity_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid numeric values."
            )

            return

        if purchase_price < 0 or selling_price < 0 or quantity < 0:

            messagebox.showerror(
                "Error",
                "Prices and quantity cannot be negative."
            )

            return

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products
            (
                product_name,
                category,
                specification,
                supplier,
                purchase_price,
                selling_price,
                quantity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product_name_var.get(),
            category_var.get(),
            specification_var.get(),
            supplier_var.get(),
            purchase_price,
            selling_price,
            quantity
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Product added successfully."
        )

        clear_fields()
        load_products()
        update_dashboard()

    # --------------------------------------------------------
    # Select product
    # --------------------------------------------------------

    def select_product(event):

        selected = product_tree.focus()

        if not selected:
            return

        values = product_tree.item(
            selected,
            "values"
        )

        product_name_var.set(values[1])
        category_var.set(values[2])
        specification_var.set(values[3])
        supplier_var.set(values[4])
        purchase_price_var.set(values[5])
        selling_price_var.set(values[6])
        quantity_var.set(values[7])

    # --------------------------------------------------------
    # Update product
    # --------------------------------------------------------

    def update_product():

        selected = product_tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a product first."
            )

            return

        values = product_tree.item(
            selected,
            "values"
        )

        product_id = values[0]

        try:

            purchase_price = float(
                purchase_price_var.get()
            )

            selling_price = float(
                selling_price_var.get()
            )

            quantity = int(
                quantity_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid numeric values."
            )

            return

        conn = connect_database()
        cursor = conn.cursor()

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
            product_name_var.get(),
            category_var.get(),
            specification_var.get(),
            supplier_var.get(),
            purchase_price,
            selling_price,
            quantity,
            product_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Product updated successfully."
        )

        clear_fields()
        load_products()
        update_dashboard()

    # --------------------------------------------------------
    # Delete product
    # --------------------------------------------------------

    def delete_product():

        selected = product_tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a product first."
            )

            return

        values = product_tree.item(
            selected,
            "values"
        )

        product_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not confirm:
            return

        conn = connect_database()
        cursor = conn.cursor()

        try:

            cursor.execute(
                "DELETE FROM products WHERE product_id = ?",
                (product_id,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully."
            )

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "This product is linked to other records and cannot be deleted."
            )

        finally:

            conn.close()

        load_products()
        clear_fields()
        update_dashboard()

    # --------------------------------------------------------
    # Input frame
    # --------------------------------------------------------

    input_frame = ttk.LabelFrame(
        window,
        text="Product Information"
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    fields = [
        ("Product Name", product_name_var),
        ("Category", category_var),
        ("Specification", specification_var),
        ("Supplier", supplier_var),
        ("Purchase Price", purchase_price_var),
        ("Selling Price", selling_price_var),
        ("Quantity", quantity_var)
    ]

    for i, (label, variable) in enumerate(fields):

        ttk.Label(
            input_frame,
            text=label
        ).grid(
            row=i // 4,
            column=(i % 4) * 2,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            input_frame,
            textvariable=variable,
            width=22
        ).grid(
            row=i // 4,
            column=(i % 4) * 2 + 1,
            padx=5,
            pady=5
        )

    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    button_frame = ttk.Frame(window)
    button_frame.pack(
        fill="x",
        padx=10
    )

    ttk.Button(
        button_frame,
        text="Add Product",
        command=add_product
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Update Product",
        command=update_product
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Delete Product",
        command=delete_product
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Clear",
        command=clear_fields
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search_frame = ttk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    ttk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left")

    ttk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Search",
        command=lambda: load_products(
            search_var.get().strip()
        )
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Show All",
        command=lambda: load_products()
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    table_frame = ttk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    columns = (
        "ID",
        "Product",
        "Category",
        "Specification",
        "Supplier",
        "Purchase Price",
        "Selling Price",
        "Quantity"
    )

    product_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        product_tree.heading(
            column,
            text=column
        )

        product_tree.column(
            column,
            width=130
        )

    product_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=product_tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    product_tree.configure(
        yscrollcommand=scrollbar.set
    )

    product_tree.bind(
        "<ButtonRelease-1>",
        select_product
    )

    load_products()


# ============================================================
# SUPPLIERS
# ============================================================

def open_suppliers():

    window = tk.Toplevel(root)
    window.title("Supplier Management")
    window.geometry("1050x600")

    supplier_name_var = tk.StringVar()
    contact_person_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()
    search_var = tk.StringVar()

    def clear_fields():

        supplier_name_var.set("")
        contact_person_var.set("")
        phone_var.set("")
        email_var.set("")
        address_var.set("")

    def load_suppliers(search=""):

        for item in supplier_tree.get_children():
            supplier_tree.delete(item)

        conn = connect_database()
        cursor = conn.cursor()

        if search:

            cursor.execute("""
                SELECT supplier_id,
                       supplier_name,
                       contact_person,
                       phone,
                       email,
                       address
                FROM suppliers
                WHERE supplier_name LIKE ?
                   OR contact_person LIKE ?
                   OR phone LIKE ?
                ORDER BY supplier_id
            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""
                SELECT supplier_id,
                       supplier_name,
                       contact_person,
                       phone,
                       email,
                       address
                FROM suppliers
                ORDER BY supplier_id
            """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:

            supplier_tree.insert(
                "",
                tk.END,
                values=row
            )

    def add_supplier():

        if not supplier_name_var.get().strip():

            messagebox.showerror(
                "Error",
                "Supplier name is required."
            )

            return

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO suppliers
            (
                supplier_name,
                contact_person,
                phone,
                email,
                address
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            supplier_name_var.get(),
            contact_person_var.get(),
            phone_var.get(),
            email_var.get(),
            address_var.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Supplier added successfully."
        )

        clear_fields()
        load_suppliers()
        update_dashboard()

    def select_supplier(event):

        selected = supplier_tree.focus()

        if not selected:
            return

        values = supplier_tree.item(
            selected,
            "values"
        )

        supplier_name_var.set(values[1])
        contact_person_var.set(values[2])
        phone_var.set(values[3])
        email_var.set(values[4])
        address_var.set(values[5])

    def update_supplier():

        selected = supplier_tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a supplier first."
            )

            return

        values = supplier_tree.item(
            selected,
            "values"
        )

        supplier_id = values[0]

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE suppliers
            SET supplier_name = ?,
                contact_person = ?,
                phone = ?,
                email = ?,
                address = ?
            WHERE supplier_id = ?
        """, (
            supplier_name_var.get(),
            contact_person_var.get(),
            phone_var.get(),
            email_var.get(),
            address_var.get(),
            supplier_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Supplier updated successfully."
        )

        clear_fields()
        load_suppliers()

    def delete_supplier():

        selected = supplier_tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a supplier first."
            )

            return

        values = supplier_tree.item(
            selected,
            "values"
        )

        supplier_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this supplier?"
        )

        if not confirm:
            return

        conn = connect_database()
        cursor = conn.cursor()

        try:

            cursor.execute(
                "DELETE FROM suppliers WHERE supplier_id = ?",
                (supplier_id,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Supplier deleted successfully."
            )

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "This supplier is linked to purchases and cannot be deleted."
            )

        finally:

            conn.close()

        load_suppliers()
        clear_fields()

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    input_frame = ttk.LabelFrame(
        window,
        text="Supplier Information"
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    fields = [
        ("Supplier Name", supplier_name_var),
        ("Contact Person", contact_person_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var)
    ]

    for i, (label, variable) in enumerate(fields):

        ttk.Label(
            input_frame,
            text=label
        ).grid(
            row=i // 3,
            column=(i % 3) * 2,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            input_frame,
            textvariable=variable,
            width=25
        ).grid(
            row=i // 3,
            column=(i % 3) * 2 + 1,
            padx=5,
            pady=5
        )

    button_frame = ttk.Frame(window)
    button_frame.pack(
        fill="x",
        padx=10
    )

    ttk.Button(
        button_frame,
        text="Add Supplier",
        command=add_supplier
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Update Supplier",
        command=update_supplier
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Delete Supplier",
        command=delete_supplier
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Clear",
        command=clear_fields
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search_frame = ttk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    ttk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left")

    ttk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Search",
        command=lambda: load_suppliers(
            search_var.get().strip()
        )
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Show All",
        command=lambda: load_suppliers()
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    table_frame = ttk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    columns = (
        "ID",
        "Supplier",
        "Contact Person",
        "Phone",
        "Email",
        "Address"
    )

    supplier_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        supplier_tree.heading(
            column,
            text=column
        )

        supplier_tree.column(
            column,
            width=150
        )

    supplier_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=supplier_tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    supplier_tree.configure(
        yscrollcommand=scrollbar.set
    )

    supplier_tree.bind(
        "<ButtonRelease-1>",
        select_supplier
    )

    load_suppliers()


# ============================================================
# INVENTORY
# ============================================================

def open_inventory():

    window = tk.Toplevel(root)
    window.title("Inventory Management")
    window.geometry("1100x650")

    product_var = tk.StringVar()
    quantity_var = tk.StringVar()
    search_var = tk.StringVar()

    def load_product_list():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT product_id,
                   product_name
            FROM products
            ORDER BY product_name
        """)

        rows = cursor.fetchall()
        conn.close()

        product_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

    def clear_fields():

        product_var.set("")
        quantity_var.set("")

    def load_stock(search=""):

        for item in stock_tree.get_children():
            stock_tree.delete(item)

        conn = connect_database()
        cursor = conn.cursor()

        if search:

            cursor.execute("""
                SELECT product_id,
                       product_name,
                       category,
                       quantity,
                       purchase_price,
                       selling_price
                FROM products
                WHERE product_name LIKE ?
                   OR category LIKE ?
                ORDER BY product_id
            """, (
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""
                SELECT product_id,
                       product_name,
                       category,
                       quantity,
                       purchase_price,
                       selling_price
                FROM products
                ORDER BY product_id
            """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:

            stock_tree.insert(
                "",
                tk.END,
                values=row
            )

    def stock_change(movement_type):

        if not product_var.get():

            messagebox.showerror(
                "Error",
                "Select a product."
            )

            return

        try:

            quantity = int(
                quantity_var.get()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quantity must be a positive integer."
            )

            return

        try:

            product_id = int(
                product_var.get().split(" - ")[0]
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid product selected."
            )

            return

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT quantity FROM products WHERE product_id = ?",
            (product_id,)
        )

        result = cursor.fetchone()

        if not result:

            conn.close()

            messagebox.showerror(
                "Error",
                "Product not found."
            )

            return

        current_stock = result[0]

        if movement_type == "OUT" and quantity > current_stock:

            conn.close()

            messagebox.showerror(
                "Error",
                "Not enough stock available."
            )

            return

        if movement_type == "IN":

            new_quantity = current_stock + quantity

        else:

            new_quantity = current_stock - quantity

        cursor.execute("""
            UPDATE products
            SET quantity = ?
            WHERE product_id = ?
        """, (
            new_quantity,
            product_id
        ))

        cursor.execute("""
            INSERT INTO stock_movements
            (
                product_id,
                movement_type,
                quantity,
                reference
            )
            VALUES (?, ?, ?, ?)
        """, (
            product_id,
            movement_type,
            quantity,
            "Manual Stock Adjustment"
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            f"Stock {movement_type} recorded successfully."
        )

        clear_fields()
        load_stock()
        update_dashboard()

    def show_stock_history():

        history_window = tk.Toplevel(window)
        history_window.title("Stock History")
        history_window.geometry("950x550")

        columns = (
            "ID",
            "Product",
            "Type",
            "Quantity",
            "Reference",
            "Date"
        )

        history_tree = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            history_tree.heading(
                column,
                text=column
            )

            history_tree.column(
                column,
                width=140
            )

        history_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                sm.movement_id,
                p.product_name,
                sm.movement_type,
                sm.quantity,
                sm.reference,
                sm.movement_date
            FROM stock_movements sm
            LEFT JOIN products p
                ON sm.product_id = p.product_id
            ORDER BY sm.movement_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:

            history_tree.insert(
                "",
                tk.END,
                values=row
            )

    # --------------------------------------------------------
    # Input frame
    # --------------------------------------------------------

    input_frame = ttk.LabelFrame(
        window,
        text="Stock Movement"
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    ttk.Label(
        input_frame,
        text="Product:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    product_combo = ttk.Combobox(
        input_frame,
        textvariable=product_var,
        width=35,
        state="readonly"
    )

    product_combo.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    ttk.Label(
        input_frame,
        text="Quantity:"
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    ttk.Entry(
        input_frame,
        textvariable=quantity_var,
        width=15
    ).grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    ttk.Button(
        input_frame,
        text="Stock In",
        command=lambda: stock_change("IN")
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    ttk.Button(
        input_frame,
        text="Stock Out",
        command=lambda: stock_change("OUT")
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    ttk.Button(
        input_frame,
        text="Clear",
        command=clear_fields
    ).grid(
        row=0,
        column=6,
        padx=5
    )

    ttk.Button(
        input_frame,
        text="Stock History",
        command=show_stock_history
    ).grid(
        row=0,
        column=7,
        padx=5
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search_frame = ttk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left")

    ttk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Search",
        command=lambda: load_stock(
            search_var.get().strip()
        )
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Show All",
        command=lambda: load_stock()
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    table_frame = ttk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    columns = (
        "ID",
        "Product",
        "Category",
        "Quantity",
        "Purchase Price",
        "Selling Price"
    )

    stock_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        stock_tree.heading(
            column,
            text=column
        )

        stock_tree.column(
            column,
            width=150
        )

    stock_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=stock_tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    stock_tree.configure(
        yscrollcommand=scrollbar.set
    )

    load_product_list()
    load_stock()


# ============================================================
# PURCHASES
# ============================================================

def open_purchases():

    window = tk.Toplevel(root)
    window.title("Purchase Management")
    window.geometry("1150x650")

    product_var = tk.StringVar()
    supplier_var = tk.StringVar()
    quantity_var = tk.StringVar()
    purchase_price_var = tk.StringVar()
    total_var = tk.StringVar(value="0.00")
    search_var = tk.StringVar()

    product_data = {}

    # --------------------------------------------------------
    # Load products
    # --------------------------------------------------------

    def load_products():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT product_id,
                   product_name,
                   purchase_price
            FROM products
            ORDER BY product_name
        """)

        rows = cursor.fetchall()
        conn.close()

        product_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

        product_data.clear()

        for row in rows:

            product_data[row[0]] = row[2]

    # --------------------------------------------------------
    # Load suppliers
    # --------------------------------------------------------

    def load_suppliers():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT supplier_id,
                   supplier_name
            FROM suppliers
            ORDER BY supplier_name
        """)

        rows = cursor.fetchall()
        conn.close()

        supplier_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

    def product_selected(event=None):

        if not product_var.get():
            return

        try:

            product_id = int(
                product_var.get().split(" - ")[0]
            )

            if product_id in product_data:

                purchase_price_var.set(
                    str(product_data[product_id])
                )

        except ValueError:
            pass

        calculate_total()

    def calculate_total(event=None):

        try:

            quantity = int(
                quantity_var.get()
            )

            price = float(
                purchase_price_var.get()
            )

            total_var.set(
                f"{quantity * price:.2f}"
            )

        except ValueError:

            total_var.set("0.00")

    def clear_fields():

        product_var.set("")
        supplier_var.set("")
        quantity_var.set("")
        purchase_price_var.set("")
        total_var.set("0.00")

    # --------------------------------------------------------
    # Load purchases
    # --------------------------------------------------------

    def load_purchases(search=""):

        for item in purchase_tree.get_children():
            purchase_tree.delete(item)

        conn = connect_database()
        cursor = conn.cursor()

        if search:

            cursor.execute("""
                SELECT
                    pu.purchase_id,
                    p.product_name,
                    s.supplier_name,
                    pu.quantity,
                    pu.purchase_price,
                    pu.total_amount,
                    pu.purchase_date
                FROM purchases pu
                JOIN products p
                    ON pu.product_id = p.product_id
                JOIN suppliers s
                    ON pu.supplier_id = s.supplier_id
                WHERE p.product_name LIKE ?
                   OR s.supplier_name LIKE ?
                ORDER BY pu.purchase_id DESC
            """, (
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""
                SELECT
                    pu.purchase_id,
                    p.product_name,
                    s.supplier_name,
                    pu.quantity,
                    pu.purchase_price,
                    pu.total_amount,
                    pu.purchase_date
                FROM purchases pu
                JOIN products p
                    ON pu.product_id = p.product_id
                JOIN suppliers s
                    ON pu.supplier_id = s.supplier_id
                ORDER BY pu.purchase_id DESC
            """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:

            purchase_tree.insert(
                "",
                tk.END,
                values=row
            )

    # --------------------------------------------------------
    # Create purchase
    # --------------------------------------------------------

    def create_purchase():

        if not product_var.get():

            messagebox.showerror(
                "Error",
                "Select a product."
            )

            return

        if not supplier_var.get():

            messagebox.showerror(
                "Error",
                "Select a supplier."
            )

            return

        try:

            product_id = int(
                product_var.get().split(" - ")[0]
            )

            supplier_id = int(
                supplier_var.get().split(" - ")[0]
            )

            quantity = int(
                quantity_var.get()
            )

            purchase_price = float(
                purchase_price_var.get()
            )

            if quantity <= 0:
                raise ValueError

            if purchase_price < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid quantity and purchase price."
            )

            return

        total_amount = quantity * purchase_price

        conn = connect_database()
        cursor = conn.cursor()

        try:

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

            cursor.execute("""
                UPDATE products
                SET quantity = quantity + ?
                WHERE product_id = ?
            """, (
                quantity,
                product_id
            ))

            cursor.execute("""
                INSERT INTO stock_movements
                (
                    product_id,
                    movement_type,
                    quantity,
                    reference
                )
                VALUES (?, ?, ?, ?)
            """, (
                product_id,
                "IN",
                quantity,
                "Purchase"
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Purchase created successfully."
            )

        except Exception as error:

            conn.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            conn.close()

        clear_fields()
        load_purchases()
        load_products()
        update_dashboard()

    def view_purchase_details():

        selected = purchase_tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a purchase first."
            )

            return

        values = purchase_tree.item(
            selected,
            "values"
        )

        messagebox.showinfo(
            "Purchase Details",
            f"Purchase ID: {values[0]}\n\n"
            f"Product: {values[1]}\n"
            f"Supplier: {values[2]}\n"
            f"Quantity: {values[3]}\n"
            f"Purchase Price: {values[4]}\n"
            f"Total Amount: {values[5]}\n"
            f"Date: {values[6]}"
        )

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    input_frame = ttk.LabelFrame(
        window,
        text="Create Purchase"
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    ttk.Label(
        input_frame,
        text="Product:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    product_combo = ttk.Combobox(
        input_frame,
        textvariable=product_var,
        width=30,
        state="readonly"
    )

    product_combo.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    product_combo.bind(
        "<<ComboboxSelected>>",
        product_selected
    )

    ttk.Label(
        input_frame,
        text="Supplier:"
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    supplier_combo = ttk.Combobox(
        input_frame,
        textvariable=supplier_var,
        width=30,
        state="readonly"
    )

    supplier_combo.grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    ttk.Label(
        input_frame,
        text="Quantity:"
    ).grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    quantity_entry = ttk.Entry(
        input_frame,
        textvariable=quantity_var,
        width=15
    )

    quantity_entry.grid(
        row=1,
        column=1,
        padx=5,
        pady=5
    )

    quantity_entry.bind(
        "<KeyRelease>",
        calculate_total
    )

    ttk.Label(
        input_frame,
        text="Purchase Price:"
    ).grid(
        row=1,
        column=2,
        padx=5,
        pady=5
    )

    price_entry = ttk.Entry(
        input_frame,
        textvariable=purchase_price_var,
        width=15
    )

    price_entry.grid(
        row=1,
        column=3,
        padx=5,
        pady=5
    )

    price_entry.bind(
        "<KeyRelease>",
        calculate_total
    )

    ttk.Label(
        input_frame,
        text="Total Amount:"
    ).grid(
        row=1,
        column=4,
        padx=5,
        pady=5
    )

    ttk.Label(
        input_frame,
        textvariable=total_var
    ).grid(
        row=1,
        column=5,
        padx=5,
        pady=5
    )

    ttk.Button(
        input_frame,
        text="Create Purchase",
        command=create_purchase
    ).grid(
        row=1,
        column=6,
        padx=10
    )

    ttk.Button(
        input_frame,
        text="Clear",
        command=clear_fields
    ).grid(
        row=1,
        column=7,
        padx=5
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search_frame = ttk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left")

    ttk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Search",
        command=lambda: load_purchases(
            search_var.get().strip()
        )
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="Show All",
        command=lambda: load_purchases()
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        search_frame,
        text="View Details",
        command=view_purchase_details
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    table_frame = ttk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    columns = (
        "ID",
        "Product",
        "Supplier",
        "Quantity",
        "Purchase Price",
        "Total Amount",
        "Date"
    )

    purchase_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        purchase_tree.heading(
            column,
            text=column
        )

        purchase_tree.column(
            column,
            width=150
        )

    purchase_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=purchase_tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    purchase_tree.configure(
        yscrollcommand=scrollbar.set
    )

    load_products()
    load_suppliers()
    load_purchases()


# ============================================================
# REPORTS
# ============================================================

def open_reports():

    window = tk.Toplevel(root)
    window.title("Reports")
    window.geometry("1200x700")

    threshold_var = tk.StringVar(
        value="10"
    )

    search_var = tk.StringVar()

    current_report = {
        "name": ""
    }

    # --------------------------------------------------------
    # Clear table
    # --------------------------------------------------------

    def clear_table():

        for item in report_tree.get_children():
            report_tree.delete(item)

        report_tree["columns"] = ()

    # --------------------------------------------------------
    # Display report
    # --------------------------------------------------------

    def display_report(
        title,
        columns,
        rows
    ):

        current_report["name"] = title

        clear_table()

        report_tree["columns"] = columns

        for column in columns:

            report_tree.heading(
                column,
                text=column
            )

            report_tree.column(
                column,
                width=150
            )

        for row in rows:

            report_tree.insert(
                "",
                tk.END,
                values=row
            )

        report_title.config(
            text=title
        )

    # --------------------------------------------------------
    # Inventory Summary
    # --------------------------------------------------------

    def inventory_summary():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                quantity,
                purchase_price,
                selling_price,
                quantity * purchase_price
            FROM products
            ORDER BY product_id
        """)

        rows = cursor.fetchall()
        conn.close()

        display_report(
            "Inventory Summary",
            (
                "ID",
                "Product",
                "Category",
                "Quantity",
                "Purchase Price",
                "Selling Price",
                "Stock Value"
            ),
            rows
        )

    # --------------------------------------------------------
    # Low Stock
    # --------------------------------------------------------

    def low_stock_report():

        try:

            threshold = int(
                threshold_var.get()
            )

            if threshold < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid stock threshold."
            )

            return

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                quantity,
                purchase_price,
                selling_price
            FROM products
            WHERE quantity <= ?
            ORDER BY quantity ASC
        """, (
            threshold,
        ))

        rows = cursor.fetchall()
        conn.close()

        display_report(
            f"Low Stock Report - Threshold {threshold}",
            (
                "ID",
                "Product",
                "Category",
                "Quantity",
                "Purchase Price",
                "Selling Price"
            ),
            rows
        )

    # --------------------------------------------------------
    # Purchase Summary
    # --------------------------------------------------------

    def purchase_summary():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pu.purchase_id,
                p.product_name,
                s.supplier_name,
                pu.quantity,
                pu.purchase_price,
                pu.total_amount,
                pu.purchase_date
            FROM purchases pu
            JOIN products p
                ON pu.product_id = p.product_id
            JOIN suppliers s
                ON pu.supplier_id = s.supplier_id
            ORDER BY pu.purchase_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        display_report(
            "Purchase Summary",
            (
                "ID",
                "Product",
                "Supplier",
                "Quantity",
                "Purchase Price",
                "Total Amount",
                "Date"
            ),
            rows
        )

    # --------------------------------------------------------
    # Stock Movement
    # --------------------------------------------------------

    def stock_movement_report():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                sm.movement_id,
                p.product_name,
                sm.movement_type,
                sm.quantity,
                sm.reference,
                sm.movement_date
            FROM stock_movements sm
            LEFT JOIN products p
                ON sm.product_id = p.product_id
            ORDER BY sm.movement_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        display_report(
            "Stock Movement Report",
            (
                "ID",
                "Product",
                "Type",
                "Quantity",
                "Reference",
                "Date"
            ),
            rows
        )

    # --------------------------------------------------------
    # Product Value
    # --------------------------------------------------------

    def product_value_report():

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                product_name,
                quantity,
                purchase_price,
                quantity * purchase_price
            FROM products
            ORDER BY quantity * purchase_price DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        display_report(
            "Product Value Report",
            (
                "Product",
                "Quantity",
                "Purchase Price",
                "Total Value"
            ),
            rows
        )

    # --------------------------------------------------------
    # Report title
    # --------------------------------------------------------

    report_title = ttk.Label(
        window,
        text="Select a report",
        font=("Arial", 16, "bold")
    )

    report_title.pack(
        pady=10
    )

    # --------------------------------------------------------
    # Report buttons
    # --------------------------------------------------------

    button_frame = ttk.Frame(window)
    button_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Button(
        button_frame,
        text="Inventory Summary",
        command=inventory_summary
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Purchase Summary",
        command=purchase_summary
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Stock Movement",
        command=stock_movement_report
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        button_frame,
        text="Product Value",
        command=product_value_report
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Low stock
    # --------------------------------------------------------

    low_stock_frame = ttk.Frame(window)
    low_stock_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Label(
        low_stock_frame,
        text="Low Stock Threshold:"
    ).pack(
        side="left"
    )

    ttk.Entry(
        low_stock_frame,
        textvariable=threshold_var,
        width=10
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        low_stock_frame,
        text="Low Stock Report",
        command=low_stock_report
    ).pack(
        side="left",
        padx=5
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    table_frame = ttk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    report_tree = ttk.Treeview(
        table_frame,
        show="headings"
    )

    report_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=report_tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    report_tree.configure(
        yscrollcommand=scrollbar.set
    )


# ============================================================
# EXCEL EXPORT
# ============================================================

def open_export():

    window = tk.Toplevel(root)

    window.title(
        "Export Data"
    )

    window.geometry(
        "650x550"
    )

    # --------------------------------------------------------
    # Create export folder
    # --------------------------------------------------------

    os.makedirs(
        EXPORT_FOLDER,
        exist_ok=True
    )

    # --------------------------------------------------------
    # General export function
    # --------------------------------------------------------

    def save_dataframe(
        dataframe,
        filename
    ):

        filepath = os.path.join(
            EXPORT_FOLDER,
            filename
        )

        dataframe.to_excel(
            filepath,
            index=False
        )

        return filepath

    # --------------------------------------------------------
    # Products export
    # --------------------------------------------------------

    def export_products():

        try:

            conn = connect_database()

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
                ORDER BY product_id
            """

            dataframe = pd.read_sql_query(
                query,
                conn
            )

            conn.close()

            filepath = save_dataframe(
                dataframe,
                "products_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Products exported successfully.\n\n"
                f"File:\n{filepath}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Suppliers export
    # --------------------------------------------------------

    def export_suppliers():

        try:

            conn = connect_database()

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
                ORDER BY supplier_id
            """

            dataframe = pd.read_sql_query(
                query,
                conn
            )

            conn.close()

            filepath = save_dataframe(
                dataframe,
                "suppliers_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Suppliers exported successfully.\n\n"
                f"File:\n{filepath}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Purchases export
    # --------------------------------------------------------

    def export_purchases():

        try:

            conn = connect_database()

            query = """
                SELECT
                    pu.purchase_id,
                    p.product_name,
                    s.supplier_name,
                    pu.quantity,
                    pu.purchase_price,
                    pu.total_amount,
                    pu.purchase_date
                FROM purchases pu
                JOIN products p
                    ON pu.product_id = p.product_id
                JOIN suppliers s
                    ON pu.supplier_id = s.supplier_id
                ORDER BY pu.purchase_id
            """

            dataframe = pd.read_sql_query(
                query,
                conn
            )

            conn.close()

            filepath = save_dataframe(
                dataframe,
                "purchases_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Purchases exported successfully.\n\n"
                f"File:\n{filepath}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Stock movements export
    # --------------------------------------------------------

    def export_stock_movements():

        try:

            conn = connect_database()

            query = """
                SELECT
                    sm.movement_id,
                    p.product_name,
                    sm.movement_type,
                    sm.quantity,
                    sm.reference,
                    sm.movement_date
                FROM stock_movements sm
                LEFT JOIN products p
                    ON sm.product_id = p.product_id
                ORDER BY sm.movement_id
            """

            dataframe = pd.read_sql_query(
                query,
                conn
            )

            conn.close()

            filepath = save_dataframe(
                dataframe,
                "stock_movements_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Stock movements exported successfully.\n\n"
                f"File:\n{filepath}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Inventory export
    # --------------------------------------------------------

    def export_inventory():

        try:

            conn = connect_database()

            query = """
                SELECT
                    product_id,
                    product_name,
                    category,
                    specification,
                    supplier,
                    quantity,
                    purchase_price,
                    selling_price,
                    quantity * purchase_price AS stock_value
                FROM products
                ORDER BY product_id
            """

            dataframe = pd.read_sql_query(
                query,
                conn
            )

            conn.close()

            filepath = save_dataframe(
                dataframe,
                "inventory_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Inventory report exported successfully.\n\n"
                f"File:\n{filepath}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Export all
    # --------------------------------------------------------

    def export_all():

        try:

            conn = connect_database()

            # Products
            products_df = pd.read_sql_query("""
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
                ORDER BY product_id
            """, conn)

            # Suppliers
            suppliers_df = pd.read_sql_query("""
                SELECT
                    supplier_id,
                    supplier_name,
                    contact_person,
                    phone,
                    email,
                    address,
                    created_at
                FROM suppliers
                ORDER BY supplier_id
            """, conn)

            # Purchases
            purchases_df = pd.read_sql_query("""
                SELECT
                    pu.purchase_id,
                    p.product_name,
                    s.supplier_name,
                    pu.quantity,
                    pu.purchase_price,
                    pu.total_amount,
                    pu.purchase_date
                FROM purchases pu
                JOIN products p
                    ON pu.product_id = p.product_id
                JOIN suppliers s
                    ON pu.supplier_id = s.supplier_id
                ORDER BY pu.purchase_id
            """, conn)

            # Stock movements
            movements_df = pd.read_sql_query("""
                SELECT
                    sm.movement_id,
                    p.product_name,
                    sm.movement_type,
                    sm.quantity,
                    sm.reference,
                    sm.movement_date
                FROM stock_movements sm
                LEFT JOIN products p
                    ON sm.product_id = p.product_id
                ORDER BY sm.movement_id
            """, conn)

            # Inventory
            inventory_df = pd.read_sql_query("""
                SELECT
                    product_id,
                    product_name,
                    category,
                    specification,
                    supplier,
                    quantity,
                    purchase_price,
                    selling_price,
                    quantity * purchase_price AS stock_value
                FROM products
                ORDER BY product_id
            """, conn)

            conn.close()

            save_dataframe(
                products_df,
                "products_report.xlsx"
            )

            save_dataframe(
                suppliers_df,
                "suppliers_report.xlsx"
            )

            save_dataframe(
                purchases_df,
                "purchases_report.xlsx"
            )

            save_dataframe(
                movements_df,
                "stock_movements_report.xlsx"
            )

            save_dataframe(
                inventory_df,
                "inventory_report.xlsx"
            )

            messagebox.showinfo(
                "Export Successful",
                "All reports exported successfully.\n\n"
                "Check the 'exports' folder."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # --------------------------------------------------------
    # Window heading
    # --------------------------------------------------------

    ttk.Label(
        window,
        text="Excel Data Export",
        font=("Arial", 18, "bold")
    ).pack(
        pady=20
    )

    ttk.Label(
        window,
        text="Select the data you want to export:"
    ).pack(
        pady=5
    )

    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    button_frame = ttk.Frame(window)
    button_frame.pack(
        pady=20
    )

    ttk.Button(
        button_frame,
        text="Export Products",
        command=export_products,
        width=30
    ).pack(
        pady=7
    )

    ttk.Button(
        button_frame,
        text="Export Suppliers",
        command=export_suppliers,
        width=30
    ).pack(
        pady=7
    )

    ttk.Button(
        button_frame,
        text="Export Purchases",
        command=export_purchases,
        width=30
    ).pack(
        pady=7
    )

    ttk.Button(
        button_frame,
        text="Export Stock Movements",
        command=export_stock_movements,
        width=30
    ).pack(
        pady=7
    )

    ttk.Button(
        button_frame,
        text="Export Inventory Report",
        command=export_inventory,
        width=30
    ).pack(
        pady=7
    )

    ttk.Separator(
        window,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=100,
        pady=10
    )

    ttk.Button(
        window,
        text="EXPORT ALL REPORTS",
        command=export_all,
        width=30
    ).pack(
        pady=10,
        ipady=5
    )

    ttk.Label(
        window,
        text="Files will be saved inside the 'exports' folder.",
    ).pack(
        pady=10
    )


# ============================================================
# EXIT
# ============================================================

def exit_application():

    confirm = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit the CFK Inventory System?"
    )

    if confirm:
        root.destroy()


# ============================================================
# APPLICATION STYLE
# ============================================================

def configure_styles():

    style = ttk.Style()

    # Use a reliable built-in theme available on Windows.
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Main colours are kept professional and simple so the UI remains
    # compatible with standard Tkinter without external packages.
    BG = "#F4F7FB"
    PANEL = "#FFFFFF"
    PRIMARY = "#1F4E78"
    PRIMARY_DARK = "#163A5C"
    ACCENT = "#2F75B5"
    TEXT = "#1F2937"
    MUTED = "#64748B"
    BORDER = "#D9E2EC"
    SUCCESS = "#2E7D32"
    DANGER = "#C62828"

    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=PANEL)

    style.configure(
        "TLabel",
        background=BG,
        foreground=TEXT,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Title.TLabel",
        background=BG,
        foreground=PRIMARY_DARK,
        font=("Segoe UI", 22, "bold")
    )

    style.configure(
        "Subtitle.TLabel",
        background=BG,
        foreground=MUTED,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Section.TLabel",
        background=BG,
        foreground=PRIMARY_DARK,
        font=("Segoe UI", 14, "bold")
    )

    style.configure(
        "CardTitle.TLabel",
        background=PANEL,
        foreground=MUTED,
        font=("Segoe UI", 10, "bold")
    )

    style.configure(
        "CardValue.TLabel",
        background=PANEL,
        foreground=PRIMARY_DARK,
        font=("Segoe UI", 25, "bold")
    )

    style.configure(
        "CardHint.TLabel",
        background=PANEL,
        foreground=MUTED,
        font=("Segoe UI", 9)
    )

    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(14, 9),
        background=PANEL,
        foreground=TEXT,
        borderwidth=1,
        relief="flat"
    )

    style.map(
        "TButton",
        background=[("active", "#E8F1FA"), ("pressed", "#D7E7F5")],
        foreground=[("active", PRIMARY_DARK)]
    )

    style.configure(
        "Primary.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(16, 10),
        background=PRIMARY,
        foreground="white",
        borderwidth=0
    )

    style.map(
        "Primary.TButton",
        background=[("active", ACCENT), ("pressed", PRIMARY_DARK)]
    )

    style.configure(
        "Danger.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(16, 10),
        background=DANGER,
        foreground="white",
        borderwidth=0
    )

    style.map(
        "Danger.TButton",
        background=[("active", "#A61B1B"), ("pressed", "#8E1616")]
    )

    style.configure(
        "TLabelFrame",
        background=BG,
        foreground=PRIMARY_DARK,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        relief="solid",
        borderwidth=1,
        padding=12
    )

    style.configure(
        "TLabelFrame.Label",
        background=BG,
        foreground=PRIMARY_DARK,
        font=("Segoe UI", 11, "bold")
    )

    style.configure(
        "TEntry",
        padding=7,
        fieldbackground="white",
        foreground=TEXT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER
    )

    style.configure(
        "TCombobox",
        padding=7,
        fieldbackground="white",
        foreground=TEXT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER
    )

    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=TEXT,
        rowheight=30,
        font=("Segoe UI", 9),
        bordercolor=BORDER,
        borderwidth=1
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY,
        foreground="white",
        font=("Segoe UI", 9, "bold"),
        padding=8,
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#DCEAF7")],
        foreground=[("selected", PRIMARY_DARK)]
    )

    style.configure(
        "TScrollbar",
        background="#CBD5E1",
        troughcolor="#EEF2F7",
        borderwidth=0,
        arrowsize=12
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

root = tk.Tk()
root.title("CFK Inventory & Record Management System")
root.geometry("1180x760")
root.minsize(1000, 680)
root.configure(bg="#F4F7FB")

configure_styles()

# Give the application a simple professional icon-like header bar.
header = tk.Frame(root, bg="#1F4E78", height=86)
header.pack(fill="x")
header.pack_propagate(False)

header_left = tk.Frame(header, bg="#1F4E78")
header_left.pack(side="left", padx=28, pady=13)

tk.Label(
    header_left,
    text="CFK",
    bg="#1F4E78",
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(anchor="w")

tk.Label(
    header_left,
    text="Inventory & Record Management System",
    bg="#1F4E78",
    fg="#DCEAF7",
    font=("Segoe UI", 10)
).pack(anchor="w")

header_right = tk.Frame(header, bg="#1F4E78")
header_right.pack(side="right", padx=28)

tk.Label(
    header_right,
    text="IT & DATA MANAGEMENT",
    bg="#1F4E78",
    fg="white",
    font=("Segoe UI", 9, "bold")
).pack(anchor="e")

tk.Label(
    header_right,
    text="Management Dashboard",
    bg="#1F4E78",
    fg="#DCEAF7",
    font=("Segoe UI", 9)
).pack(anchor="e")

# Main content area.
content = ttk.Frame(root)
content.pack(fill="both", expand=True, padx=28, pady=24)

intro = ttk.Frame(content)
intro.pack(fill="x", pady=(0, 18))

intro_left = ttk.Frame(intro)
intro_left.pack(side="left", fill="x", expand=True)

ttk.Label(
    intro_left,
    text="Dashboard Overview",
    style="Title.TLabel"
).pack(anchor="w")

ttk.Label(
    intro_left,
    text="Monitor products, suppliers, stock levels, purchases and reporting from one place.",
    style="Subtitle.TLabel"
).pack(anchor="w", pady=(4, 0))

# Dashboard cards.
dashboard_frame = ttk.Frame(content)
dashboard_frame.pack(fill="x", pady=(0, 22))


def create_dashboard_card(parent, title, hint):
    card = ttk.Frame(parent, style="Card.TFrame", padding=18)
    card.pack(side="left", fill="both", expand=True, padx=6)

    ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
    value = ttk.Label(card, text="0", style="CardValue.TLabel")
    value.pack(anchor="w", pady=(8, 2))
    ttk.Label(card, text=hint, style="CardHint.TLabel").pack(anchor="w")

    return value


products_value = create_dashboard_card(
    dashboard_frame, "TOTAL PRODUCTS", "Registered products"
)
suppliers_value = create_dashboard_card(
    dashboard_frame, "TOTAL SUPPLIERS", "Registered suppliers"
)
stock_value = create_dashboard_card(
    dashboard_frame, "TOTAL STOCK", "Units currently available"
)
low_stock_value = create_dashboard_card(
    dashboard_frame, "LOW STOCK ITEMS", "Products at or below 10 units"
)

# Navigation panel.
module_header = ttk.Frame(content)
module_header.pack(fill="x", pady=(0, 10))
ttk.Label(
    module_header,
    text="System Modules",
    style="Section.TLabel"
).pack(side="left")

module_panel = ttk.Frame(content, style="Card.TFrame", padding=18)
module_panel.pack(fill="both", expand=True)

# Configure equal-width columns.
for col in range(4):
    module_panel.columnconfigure(col, weight=1)
for row in range(2):
    module_panel.rowconfigure(row, weight=1)


def module_button(text, command, row, column, primary=False):
    ttk.Button(
        module_panel,
        text=text,
        command=command,
        style="Primary.TButton" if primary else "TButton"
    ).grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=8,
        pady=8,
        ipadx=8,
        ipady=12
    )


module_button("Products", open_products, 0, 0, True)
module_button("Suppliers", open_suppliers, 0, 1)
module_button("Inventory", open_inventory, 0, 2)
module_button("Purchases", open_purchases, 0, 3)
module_button("Reports", open_reports, 1, 0)
module_button("Export Data", open_export, 1, 1)
module_button("Refresh Dashboard", update_dashboard, 1, 2)
module_button("Exit", exit_application, 1, 3, False)

# Footer/status area.
footer = tk.Frame(root, bg="#E8EEF5", height=34)
footer.pack(fill="x", side="bottom")
footer.pack_propagate(False)

tk.Label(
    footer,
    text="CFK Inventory System  |  SQLite Database  |  Python + Tkinter",
    bg="#E8EEF5",
    fg="#64748B",
    font=("Segoe UI", 8)
).pack(side="left", padx=28, pady=8)

tk.Label(
    footer,
    text="Ready",
    bg="#E8EEF5",
    fg="#2E7D32",
    font=("Segoe UI", 8, "bold")
).pack(side="right", padx=28, pady=8)

# Initial dashboard update.
update_dashboard()

# Start application.
root.mainloop()
