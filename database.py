import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("arbitrage.db")
    c = conn.cursor()
    
    # Таблица для вилок
    c.execute('''CREATE TABLE IF NOT EXISTS vilki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        event TEXT,
        bk1 TEXT,
        outcome1 TEXT,
        odds1 REAL,
        stake1 REAL,
        bk2 TEXT,
        outcome2 TEXT,
        odds2_history REAL,
        stake2 REAL,
        profit REAL
    )''')
    
    # Таблица для бонусов
    c.execute('''CREATE TABLE IF NOT EXISTS bonuses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        bk TEXT,
        type TEXT,
        amount REAL,
        conditions TEXT,
        deadline TEXT,
        status TEXT,
        profit REAL
    )''')
    
    conn.commit()
    conn.close()

def add_vilka(date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2, stake2, profit):
    conn = sqlite3.connect("arbitrage.db")
    c = conn.cursor()
    c.execute("INSERT INTO vilki (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2_history, stake2, profit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2, stake2, profit))
    conn.commit()
    conn.close()

def add_bonus(date, bk, type, amount, conditions, deadline, status, profit):
    conn = sqlite3.connect("arbitrage.db")
    c = conn.cursor()
    c.execute("INSERT INTO bonuses (date, bk, type, amount, conditions, deadline, status, profit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (date, bk, type, amount, conditions, deadline, status, profit))
    conn.commit()
    conn.close()

def get_vilki():
    conn = sqlite3.connect("arbitrage.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vilki")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "date": row[1], "event": row[2], "bk1": row[3], "outcome1": row[4], "odds1": row[5],
             "stake1": row[6], "bk2": row[7], "outcome2": row[8], "odds2_history": row[9], "stake2": row[10], "profit": row[11]} for row in rows]

def get_bonuses():
    conn = sqlite3.connect("arbitrage.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bonuses")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "date": row[1], "bk": row[2], "type": row[3], "amount": row[4], "conditions": row[5],
             "deadline": row[6], "status": row[7], "profit": row[8]} for row in rows]

if __name__ == "__main__":
    init_db()