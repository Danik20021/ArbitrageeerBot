from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Создание базы при запуске
if not os.path.exists('arbitrage.db'):
    conn = sqlite3.connect('arbitrage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vilki (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, event TEXT, bk1 TEXT, outcome1 TEXT, odds1 REAL, stake1 REAL,
            bk2 TEXT, outcome2 TEXT, odds2_history REAL, stake2 REAL, profit REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bonuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, bk TEXT, type TEXT, amount REAL, conditions TEXT,
            deadline TEXT, status TEXT, profit REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('arbitrage.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/save-vilka', methods=['POST'])
def save_vilka():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vilki (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2_history, stake2, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['date'], data['event'], data['bk1'], data['outcome1'], data['odds1'], data['stake1'],
        data['bk2'], data['outcome2'], data['odds2_history'], data['stake2'], data['profit']
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Вилка добавлена"})

@app.route('/save-bonus', methods=['POST'])
def save_bonus():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bonuses (date, bk, type, amount, conditions, deadline, status, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['date'], data['bk'], data['type'], data['amount'], data['conditions'],
        data['deadline'], data['status'], data['profit']
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Бонус добавлен"})

@app.route('/get-vilki', methods=['GET'])
def get_vilki():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vilki')
    vilki = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in vilki])

@app.route('/get-bonuses', methods=['GET'])
def get_bonuses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bonuses')
    bonuses = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in bonuses])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)