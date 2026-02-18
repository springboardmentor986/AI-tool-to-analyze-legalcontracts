import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, plan TEXT)''')
    conn.commit()
    conn.close()

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = make_hash(password)
    try:
        c.execute("INSERT INTO users (username, password, plan) VALUES (?, ?, ?)", 
                  (username, hashed_pw, 'Free'))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False # User already exists
    conn.close()
    return result

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = make_hash(password)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    data = c.fetchone()
    conn.close()
    return data # Returns (username, password, plan) or None

def update_plan(username, new_plan):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET plan=? WHERE username=?", (new_plan, username))
    conn.commit()
    conn.close()