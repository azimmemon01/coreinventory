import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def create_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn



# ---------------- USERS TABLE ----------------
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    conn.commit()


def add_user(conn, username, password):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?,?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False


def login(conn, username, password):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    return cursor.fetchone()


def update_password(conn, username, new_password):

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_password, username)
    )

    conn.commit()


# ---------------- PRODUCTS TABLE ----------------
def create_products_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        min_stock INTEGER,
        quantity INTEGER
    )
    """)

    conn.commit()


def add_product(conn, name, category, price, min_stock):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name,category,price,min_stock,quantity) VALUES (?,?,?,?,0)",
        (name, category, price, min_stock)
    )

    conn.commit()


def get_products(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    return cursor.fetchall()
def create_stock_transactions_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        action TEXT,
        quantity INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

def add_stock_transaction(conn, product, action, quantity):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO stock_transactions (product, action, quantity) VALUES (?, ?, ?)",
        (product, action, quantity)
    )

    conn.commit()
def update_stock(conn, product_id, quantity_change):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM products WHERE id=?",
        (product_id,)
    )

    product_name = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE products SET quantity = quantity + ? WHERE id=?",
        (quantity_change, product_id)
    )

    action = "Stock In" if quantity_change > 0 else "Stock Out"

    add_stock_transaction(conn, product_name, action, abs(quantity_change))

    conn.commit()

def total_products(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")

    return cursor.fetchone()[0]


def low_stock(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE quantity <= min_stock"
    )

    return cursor.fetchone()[0]


def out_of_stock(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE quantity = 0"
    )

    return cursor.fetchone()[0]


# ---------------- DELIVERIES ----------------
def create_deliveries_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        quantity INTEGER,
        status TEXT
    )
    """)

    conn.commit()


def pending_deliveries(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM deliveries WHERE status='Pending'"
    )

    return cursor.fetchone()[0]


def get_deliveries(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, product, quantity, status FROM deliveries"
    )

    return cursor.fetchall()


# ---------------- TRANSFERS ----------------
def create_transfers_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transfers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_wh TEXT,
        to_wh TEXT,
        product TEXT,
        quantity INTEGER,
        status TEXT
    )
    """)

    conn.commit()


def add_transfer(conn, from_wh, to_wh, product, quantity):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transfers (from_wh,to_wh,product,quantity,status) VALUES (?,?,?,?,?)",
        (from_wh, to_wh, product, quantity, "Scheduled")
    )

    conn.commit()


def scheduled_transfers(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transfers WHERE status='Scheduled'"
    )

    return cursor.fetchone()[0]


def get_transfers(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT from_wh, to_wh, product, quantity FROM transfers"
    )

    return cursor.fetchall()


# ---------------- DASHBOARD DATA ----------------
def get_product_stock(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, quantity FROM products"
    )

    return cursor.fetchall()


def get_inventory(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, category, price, quantity FROM products"
    )

    return cursor.fetchall()


def get_product_names(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM products")

    return cursor.fetchall()
def add_delivery(conn, product, quantity, status):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO deliveries (product, quantity, status) VALUES (?, ?, ?)",
        (product, quantity, status)
    )

    conn.commit()
def update_delivery_status(conn, delivery_id, status):

    cursor = conn.cursor()

    # get delivery information
    cursor.execute(
        "SELECT product, quantity FROM deliveries WHERE id=?",
        (delivery_id,)
    )

    product, qty = cursor.fetchone()

    # update delivery status
    cursor.execute(
        "UPDATE deliveries SET status=? WHERE id=?",
        (status, delivery_id)
    )

    if status == "Delivered":

     product_id = get_product_id(conn, product)

     cursor.execute(
        "SELECT quantity FROM products WHERE id=?",
        (product_id,)
     )

     current_stock = cursor.fetchone()[0]

     if current_stock >= qty:

          cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id=?",
            (qty, product_id)
            )

          add_stock_transaction(conn, product, "Delivery", -qty)

     else:
        return "Not enough stock"

    conn.commit()
def get_product_id(conn, product_name):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM products WHERE name=?",
        (product_name,)
    )

    result = cursor.fetchone()

    return result[0] if result else None
def get_stock_history(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT product, action, quantity, date FROM stock_transactions ORDER BY date DESC"
    )

    return cursor.fetchall()

def create_receipts_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        quantity INTEGER,
        status TEXT
    )
    """)

    conn.commit()
def add_receipt(conn, product, quantity, status):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO receipts (product, quantity, status) VALUES (?,?,?)",
        (product, quantity, status)
    )

    conn.commit()
def get_receipts(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, product, quantity, status FROM receipts"
    )

    return cursor.fetchall()
def update_receipt_status(conn, receipt_id, status):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT product, quantity FROM receipts WHERE id=?",
        (receipt_id,)
    )

    product, qty = cursor.fetchone()

    cursor.execute(
        "UPDATE receipts SET status=? WHERE id=?",
        (status, receipt_id)
    )

    if status == "Received":

        product_id = get_product_id(conn, product)

        cursor.execute(
            "UPDATE products SET quantity = quantity + ? WHERE id=?",
            (qty, product_id)
        )

        add_stock_transaction(conn, product, "Receipt", qty)

    conn.commit()
def pending_receipts(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM receipts WHERE status='Pending'"
    )

    return cursor.fetchone()[0]