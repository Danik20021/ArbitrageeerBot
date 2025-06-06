import logging
from flask import Flask, request, jsonify
from database import add_vilka, add_bonus, get_vilki, get_bonuses

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Логи в файл
file_handler = logging.FileHandler("server.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Логи в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

app = Flask(__name__)

@app.route("/save-vilka", methods=["POST"])
def save_vilka():
    logger.info("Получен запрос на сохранение вилки")
    try:
        data = request.json
        add_vilka(
            data["date"],
            data["event"],
            data["bk1"],
            data["outcome1"],
            data["odds1"],
            data["stake1"],
            data["bk2"],
            data["outcome2"],
            data["odds2_history"],
            data["stake2"],
            data["profit"]
        )
        logger.info("Вилка успешно сохранена")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error("Ошибка при сохранении вилки: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/save-bonus", methods=["POST"])
def save_bonus():
    logger.info("Получен запрос на сохранение бонуса")
    try:
        data = request.json
        add_bonus(
            data["date"],
            data["bk"],
            data["type"],
            data["amount"],
            data["conditions"],
            data["deadline"],
            data["status"],
            data["profit"]
        )
        logger.info("Бонус успешно сохранён")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error("Ошибка при сохранении бонуса: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get-vilki", methods=["GET"])
def get_vilki_route():
    logger.info("Получен запрос на получение списка вилок")
    try:
        vilki = get_vilki()
        logger.info("Список вилок успешно отправлен")
        return jsonify(vilki)
    except Exception as e:
        logger.error("Ошибка при получении списка вилок: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get-bonuses", methods=["GET"])
def get_bonuses_route():
    logger.info("Получен запрос на получение списка бонусов")
    try:
        bonuses = get_bonuses()
        logger.info("Список бонусов успешно отправлен")
        return jsonify(bonuses)
    except Exception as e:
        logger.error("Ошибка при получении списка бонусов: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    logger.info("Запуск сервера...")
    app.run(debug=True, host="0.0.0.0", port=5000)
    logger.info("Сервер запущен")