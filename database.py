import sqlite3

def create_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn


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
    cursor.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()


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