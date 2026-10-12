"""Екі демо үшін ортақ дерекқор жасайды: users.db"""
import sqlite3

db = sqlite3.connect("users.db")
db.execute("DROP TABLE IF EXISTS users")
db.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
""")
db.execute("INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
           ("admin@shop.kz", "AdminSecret123", 1))
db.execute("INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
           ("user@shop.kz", "user123", 0))
db.commit()
db.close()
print("users.db дайын. 2 қолданушы қосылды (admin@shop.kz, user@shop.kz).")
