from flask import Flask, request, jsonify
from flask_cors import CORS  # Исправлен импорт
import mysql.connector
import os
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к MySQL (обновлено для базы zuev20023$default)
DATABASE_CONFIG = {
    'host': 'zuev20023.mysql.pythonanywhere-services.com',
    'user': 'zuev20023',
    'password': '123321qaz',
    'database': 'zuev20023$default'  # Используем существующую базу
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        logger.info("Успешное подключение к MySQL")
        return conn
    except mysql.connector.Error as e:
        logger.error(f"Ошибка подключения к MySQL: {str(e)}")
        raise

# Создание таблиц
conn = None
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vilki (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(255),
            event VARCHAR(255),
            bk1 VARCHAR(255),
            outcome1 VARCHAR(255),
            odds1 FLOAT,
            stake1 FLOAT,
            bk2 VARCHAR(255),
            outcome2 VARCHAR(255),
            odds2_history FLOAT,
            stake2 FLOAT,
            profit FLOAT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bonuses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(255),
            bk VARCHAR(255),
            type VARCHAR(255),
            amount FLOAT,
            conditions VARCHAR(255),
            deadline VARCHAR(255),
            status VARCHAR(255),
            profit FLOAT
        )
    ''')
    conn.commit()
    logger.info("Таблицы созданы или уже существуют")
except mysql.connector.Error as e:
    logger.error(f"Ошибка создания таблиц: {str(e)}")
finally:
    if conn and conn.is_connected():
        conn.close()

@app.route('/save-vilka', methods=['POST'])
def save_vilka():
    conn = None
    try:
        data = request.get_json()
        logger.info(f"Получены данные для вилки: {data}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vilki (date, event, bk1, outcome1, odds1, stake1, bk2, outcome2, odds2_history, stake2, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['date'], data['event'], data['bk1'], data['outcome1'], data['odds1'], data['stake1'],
            data['bk2'], data['outcome2'], data['odds2_history'], data['stake2'], data['profit']
        ))
        conn.commit()
        logger.info("Вилка успешно сохранена")
        return jsonify({"status": "success", "message": "Вилка добавлена"})
    except mysql.connector.Error as e:
        logger.error(f"Ошибка сохранения вилки: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/save-bonus', methods=['POST'])
def save_bonus():
    conn = None
    try:
        data = request.get_json()
        logger.info(f"Получены данные для бонуса: {data}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bonuses (date, bk, type, amount, conditions, deadline, status, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['date'], data['bk'], data['type'], data['amount'], data['conditions'],
            data['deadline'], data['status'], data['profit']
        ))
        conn.commit()
        logger.info("Бонус успешно сохранён")
        return jsonify({"status": "success", "message": "Бонус добавлен"})
    except mysql.connector.Error as e:
        logger.error(f"Ошибка сохранения бонуса: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/get-vilki', methods=['GET'])
def get_vilki():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM vilki')
        vilki = cursor.fetchall()
        logger.info(f"Возвращены вилки: {vilki}")
        return jsonify(vilki)
    except mysql.connector.Error as e:
        logger.error(f"Ошибка получения вилок: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/get-bonuses', methods=['GET'])
def get_bonuses():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM bonuses')
        bonuses = cursor.fetchall()
        logger.info(f"Возвращены бонусы: {bonuses}")
        return jsonify(bonuses)
    except mysql.connector.Error as e:
        logger.error(f"Ошибка получения бонусов: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/test', methods=['GET'])
def test():
    logger.info("Тестовый эндпоинт вызван")
    return jsonify({"status": "success", "message": "Тест прошёл"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)