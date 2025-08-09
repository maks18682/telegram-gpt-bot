import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем переменные окружения
TELEGRAM_TOKEN = os.getenv("7707276762:AAHFo53byakbAIXBTLE6sEUmwY4BvRMgqjk", "").strip()
OPENROUTER_API_KEY = os.getenv("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", "").strip()

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не найден! Проверь переменные окружения на Render.")
if not OPENROUTER_API_KEY:
    logger.error("❌ OPENROUTER_API_KEY не найден! Проверь переменные окружения на Render.")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ChatGPT бот через OpenRouter. Напиши мне что-нибудь.")

# Ответ на сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )

        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            await update.message.reply_text(bot_reply)
        else:
            logger.error(f"OpenRouter error {response.status_code}: {response.text}")
            await update.message.reply_text("⚠️ Произошла ошибка при обращении к OpenRouter.")

    except Exception as e:
        logger.error(f"Ошибка запроса к OpenRouter: {e}")
        await update.message.reply_text("⚠️ Не удалось связаться с OpenRouter.")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Бот запущен.")
    app.run_polling()