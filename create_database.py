import sqlite3

connection = sqlite3.connect("customers.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    password TEXT NOT NULL

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    father_name TEXT,

    mother_name TEXT,

    dob TEXT,

    gender TEXT,

    occupation TEXT,

    mobile TEXT,

    alternate_mobile TEXT,

    email TEXT,

    address TEXT,

    city TEXT,

    state TEXT,

    pincode TEXT,

    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    photo TEXT,

    document TEXT

)
""")

cursor.execute("SELECT * FROM admins")

if cursor.fetchone() is None:

    cursor.execute("""

    INSERT INTO admins(username,password)

    VALUES(?,?)

    """,

    ("admin","aniket_admin"))

connection.commit()

connection.close()

print("Database Created Successfully")