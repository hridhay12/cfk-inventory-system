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

⚙️Prerequisites
Python 3.8 or higher installed on your machine.

Git installed (to clone the repository).

💻 Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/yourusername/cfk-inventory-system.git](https://github.com/yourusername/cfk-inventory-system.git)
cd cfk-inventory-system
Install required dependencies:(If you used any external libraries like pandas, list them in a requirements.txt or install them directly)

Bash
pip install -r requirements.txt
Run the application:

Bash
python gui_updated.py
Note: The local database file will automatically initialize in the data/ folder upon the first launch.

📖 Usage Guide
Launch the app using python gui_updated.py.

Navigate to the Suppliers and Products tabs to populate your base catalog.

Use the Purchase module to log incoming stock. The system will automatically update the total stock count.

Navigate to the Reports tab to export current stock levels directly to the exports/ folder.
