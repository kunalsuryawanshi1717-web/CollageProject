import sqlite3

def connect_db():
    return sqlite3.connect("expense.db")

# ---------------- USER TABLE ----------------
def create_user_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES(?,?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

# ---------------- EXPENSE TABLE ----------------
def create_expense_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_expense(username, date, category, amount, note):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO expenses(username,date,category,amount,note) VALUES(?,?,?,?,?)",
              (username, date, category, amount, note))
    conn.commit()
    conn.close()

def get_expenses(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE username=?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

# DEBUG TOOL - See users in DB
def debug_users():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    print("USERS:", c.fetchall())
    conn.close()
