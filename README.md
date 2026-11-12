# cfk-inventory-system
A local Python-based inventory and record management system built for CFK OVERSEAS LLP.

# CFK Inventory and Record Management System

A custom-built, offline desktop application developed for CFK OVERSEAS LLP to streamline their supply chain, supplier tracking, and bulk import operations. 

This system replaces manual spreadsheet tracking with a secure, local SQL database and a user-friendly Python GUI, ensuring real-time inventory accuracy and instant report generation.

## 🚀 Key Features
* **Unified Dashboard:** Manage products, suppliers, and purchases from a single interface.
* **Automated Inventory Tracking:** Logging a purchase automatically updates the total stock levels without manual calculation.
* **Local Database:** Uses a relational SQL database for secure, offline data storage with zero cloud dependencies.
* **One-Click Exports:** Instantly generate and save formatted inventory reports to the local file system.

## 🛠️ Technology Stack
* **Frontend:** Python GUI (Tkinter)
* **Backend:** Python 3
* **Database:** SQLite / MySQL 

## 📂 Project Structure
```text
cfk-inventory-system/
│
├── data/                 # Local database storage directory
├── exports/              # Generated reports and CSV exports
├── database.py           # Database connection and SQL queries
├── export.py             # Logic for formatting and exporting data
├── gui_updated.py        # Main application entry point and dashboard
├── inventory.py          # Inventory calculation logic
├── products.py           # Product catalog management
├── purchase.py           # Purchase logging and transaction handling
├── reports.py            # Analytics and report generation
└── supplier.py           # Supplier relations module
