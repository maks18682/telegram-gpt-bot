import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import nest_asyncio
import asyncio
import sys

# 🔑 ВСТАВЬ сюда свой OpenRouter API-ключ
OPENROUTER_API_KEY = "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"

# 🔑 ВСТАВЬ свой Telegram бот-токен
TELEGRAM_TOKEN = "7707276762:AAHFo53byakbAIXBTLE6sEUmwY4BvRMgqjk"

# 📋 Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ChatGPT-бот через OpenRouter. Напиши мне что-нибудь 🧠")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "TelegramBotGPT"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Ты вежливый ассистент, отвечай кратко и ясно."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply.strip())

    except Exception as e:
        logger.error(f"OpenRouter Error: {e}")
        await update.message.reply_text("Ошибка при запросе к OpenRouter API 😓")

# Основной запуск
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")

    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

# Запуск в VS Code
if __name__ == "__main__":
    nest_asyncio.apply()

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()