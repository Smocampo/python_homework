import os
import sqlite3

db_path = os.path.join("..", "db", "magazines.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# ==========================================
# DATA INSERTION FUNCTIONS
# ==========================================
def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?);", (name,))
    except sqlite3.IntegrityError:
        pass

def add_magazine(cursor, name, publisher_name):
    try:
        cursor.execute("SELECT id FROM publishers WHERE name = ?;", (publisher_name,))
        row = cursor.fetchone()
        if row:
            cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?);", (name, row[0]))
    except sqlite3.IntegrityError:
        pass

def add_subscriber(cursor, name, address):
    cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?;", (name, address))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?);", (name, address))

def add_subscription(cursor, subscriber_name, magazine_name, expiration_date):
    cursor.execute("SELECT id FROM subscribers WHERE name = ?;", (subscriber_name,))
    sub_row = cursor.fetchone()
    cursor.execute("SELECT id FROM magazines WHERE name = ?;", (magazine_name,))
    mag_row = cursor.fetchone()
    
    if sub_row and mag_row:
        cursor.execute("""
            SELECT id FROM subscriptions 
            WHERE subscriber_id = ? AND magazine_id = ? AND expiration_date = ?;
        """, (sub_row[0], mag_row[0], expiration_date))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?);", (sub_row[0], mag_row[0], expiration_date))

# ==========================================
# MAIN EXECUTION & QUERIES
# ==========================================
conn = None
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Setup tables & data silently
    cursor.execute("CREATE TABLE IF NOT EXISTS publishers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS magazines (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, publisher_id INTEGER NOT NULL, FOREIGN KEY (publisher_id) REFERENCES publishers(id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER PRIMARY KEY AUTOINCREMENT, subscriber_id INTEGER NOT NULL, magazine_id INTEGER NOT NULL, expiration_date TEXT NOT NULL, FOREIGN KEY (subscriber_id) REFERENCES subscribers(id), FOREIGN KEY (magazine_id) REFERENCES magazines(id));")

    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Hearst Communications")
    add_publisher(cursor, "Dotdash Meredith")
    add_magazine(cursor, "Vogue", "Condé Nast")
    add_magazine(cursor, "Cosmopolitan", "Hearst Communications")
    add_magazine(cursor, "Better Homes & Gardens", "Dotdash Meredith")
    add_subscriber(cursor, "Alice Smith", "123 Maple St")
    add_subscriber(cursor, "Bob Jones", "456 Oak Rd")
    add_subscriber(cursor, "Alice Smith", "789 Pine Ave")
    add_subscription(cursor, "Alice Smith", "Vogue", "2027-12-31")
    add_subscription(cursor, "Bob Jones", "Cosmopolitan", "2026-11-30")
    add_subscription(cursor, "Alice Smith", "Better Homes & Gardens", "2027-06-15")
    conn.commit()

    # ==========================================
    # TASK 4: WRITE SQL QUERIES
    # ==========================================
    print("\n==========================================")
    print("QUERY 1: All information from subscribers")
    print("==========================================")
    cursor.execute("SELECT * FROM subscribers;")
    for row in cursor.fetchall():
        print(row)

    print("\n==========================================")
    print("QUERY 2: All magazines sorted by name")
    print("==========================================")
    cursor.execute("SELECT * FROM magazines ORDER BY name ASC;")
    for row in cursor.fetchall():
        print(row)

    print("\n==========================================")
    print("QUERY 3: Magazines for a particular publisher (JOIN)")
    print("==========================================")
    # This matches the publisher_id column to the publisher's main id
    target_publisher = "Condé Nast"
    cursor.execute("""
        SELECT magazines.id, magazines.name 
        FROM magazines
        INNER JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?;
    """, (target_publisher,))
    
    for row in cursor.fetchall():
        print(f"Publisher: {target_publisher} | Magazine: {row[1]} (ID: {row[0]})")
    print("==========================================\n")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()
