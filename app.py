from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://koyeb-adm:npg_VwG31dKNezXr@ep-muddy-king-a2lzfc2n.eu-central-1.pg.koyeb.app/koyebdb')

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.cursor_factory = RealDictCursor
        logger.info("Успешное подключение к PostgreSQL")
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к PostgreSQL: {str(e)}")
        raise

# Создание таблиц
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vilki (
            id SERIAL PRIMARY KEY,
            date TEXT, event TEXT, bk1 TEXT, outcome1 TEXT, odds1 REAL, stake1 REAL,
            bk2 TEXT, outcome2 TEXT, odds2_history REAL, stake2 REAL, profit REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bonuses (
            id SERIAL PRIMARY KEY,
            date TEXT, bk TEXT, type TEXT, amount REAL, conditions TEXT,
            deadline TEXT, status TEXT, profit REAL
        )
    ''')
    conn.commit()
    logger.info("Таблицы созданы или уже существуют")
except Exception as e:
    logger.error(f"Ошибка создания таблиц: {str(e)}")
finally:
    if conn:
        conn.close()

@app.route('/save-vilka', methods=['POST'])
def save_vilka():
    try:
        data = request.get_json()
        logger.info(f"Получены данные для вилки: {data}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vilki (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2_history, stake2, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['date'], data['event'], data['bk1'], data['outcome1'], data['odds1'], data['stake1'],
            data['bk2'], data['outcome2'], data['odds2_history'], data['stake2'], data['profit']
        ))
        conn.commit()
        logger.info("Вилка успешно сохранена")
        return jsonify({"status": "success", "message": "Вилка добавлена"})
    except Exception as e:
        logger.error(f"Ошибка сохранения вилки: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/save-bonus', methods=['POST'])
def save_bonus():
    try:
        data = request.get_json()
        logger.info(f"Получены данные для бонуса: {data}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bonuses (date, bk, type, amount, conditions, deadline, status, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['date'], data['bk'], data['type'], data['amount'], data['conditions'],
            data['deadline'], data['status'], data['profit']
        ))
        conn.commit()
        logger.info("Бонус успешно сохранён")
        return jsonify({"status": "success", "message": "Бонус добавлен"})
    except Exception as e:
        logger.error(f"Ошибка сохранения бонуса: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/get-vilki', methods=['GET'])
def get_vilki():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vilki')
        vilki = cursor.fetchall()
        logger.info(f"Возвращены вилки: {vilki}")
        return jsonify(vilki)
    except Exception as e:
        logger.error(f"Ошибка получения вилок: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/get-bonuses', methods=['GET'])
def get_bonuses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonuses')
        bonuses = cursor.fetchall()
        logger.info(f"Возвращены бонусы: {bonuses}")
        return jsonify(bonuses)
    except Exception as e:
        logger.error(f"Ошибка получения бонусов: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)