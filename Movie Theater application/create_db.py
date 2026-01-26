import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS seats (
    movie TEXT,
    seat_no TEXT,
    user TEXT
)
""")

con.commit()
con.close()
