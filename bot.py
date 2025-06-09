import logging
from logging import StreamHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Логи в файл
file_handler = logging.FileHandler("bot.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Логи в консоль
console_handler = StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

TOKEN = "7736199793:AAGDDXtTIDGVoiAb0u84EDvo9Ylol4kdTXA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /start от пользователя %s", update.effective_user.id)
    try:
        if not update.message:
            logger.error("update.message отсутствует")
            return

        # Создаём кнопки с web_app
        keyboard = [
            [KeyboardButton(text="Добавить вилку", web_app={"url": "https://arbitrageeerbot-webapp.netlify.app/add-vilka"})],
            [KeyboardButton(text="Добавить бонус", web_app={"url": "https://arbitrageeerbot-webapp.netlify.app/add-bonus"})],
            [KeyboardButton(text="Статистика", web_app={"url": "https://arbitrageeerbot-webapp.netlify.app/stats"})]
        ]
        logger.info("Клавиатура создана: %s", keyboard)
        
        # Отправляем сообщение с клавиатурой
        await update.message.reply_text(
            "Привет! Я бот для учёта вилок и бонусов. Используй кнопки ниже, чтобы начать!",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        )
        logger.info("Сообщение отправлено пользователю %s", update.effective_user.id)
    except Exception as e:
        logger.error("Ошибка при отправке сообщения: %s", str(e))
        raise

def main():
    try:
        logger.info("Запуск бота...")
        app = Application.builder().token(TOKEN).build()
        logger.info("Бот успешно инициализирован")
        
        app.add_handler(CommandHandler("start", start))
        logger.info("Обработчик команд добавлен")
        
        logger.info("Начинаем опрос Telegram API...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Бот завершил работу")
    except Exception as e:
        logger.error("Произошла ошибка при запуске бота: %s", str(e))
        raise

if __name__ == "__main__":
    main()