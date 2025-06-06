import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = 'postgres://koyeb-adm:npg_VwG31dKNezXr@ep-muddy-king-a2lzfc2n.eu-central-1.pg.koyeb.app/koyebdb'

def init_db():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.cursor_factory = RealDictCursor
        c = conn.cursor()
        
        # Таблица для вилок
        c.execute('''CREATE TABLE IF NOT EXISTS vilki (
            id SERIAL PRIMARY KEY,
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
            id SERIAL PRIMARY KEY,
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
    except Exception as e:
        print(f"Ошибка создания таблиц: {str(e)}")
    finally:
        if conn:
            conn.close()

def add_vilka(date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2, stake2, profit):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        c.execute('''
            INSERT INTO vilki (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2_history, stake2, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2, stake2, profit))
        conn.commit()
    except Exception as e:
        print(f"Ошибка добавления вилки: {str(e)}")
    finally:
        if conn:
            conn.close()

def add_bonus(date, bk, type, amount, conditions, deadline, status, profit):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        c.execute('''
            INSERT INTO bonuses (date, bk, type, amount, conditions, deadline, status, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (date, bk, type, amount, conditions, deadline, status, profit))
        conn.commit()
    except Exception as e:
        print(f"Ошибка добавления бонуса: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_vilki():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.cursor_factory = RealDictCursor
        c = conn.cursor()
        c.execute("SELECT * FROM vilki")
        rows = c.fetchall()
        return rows
    except Exception as e:
        print(f"Ошибка получения вилок: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_bonuses():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.cursor_factory = RealDictCursor
        c = conn.cursor()
        c.execute("SELECT * FROM bonuses")
        rows = c.fetchall()
        return rows
    except Exception as e:
        print(f"Ошибка получения бонусов: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()