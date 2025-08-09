import os
print("TELEGRAM_TOKEN from env:", repr(os.getenv("TELEGRAM_TOKEN")))
import logging
import requests
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Для Render (решает проблему с event loop)
nest_asyncio.apply()

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("7707276762:AAHFo53byakbAIXBTLE6sEUmwY4BvRMgqjk").strip() 
OPENROUTER_API_KEY = os.getenv("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")

# Команда /start
async def start(update, context):
    await update.message.reply_text("Привет! Я твой GPT-бот через OpenRouter.")

# Ответ на любое сообщение
async def handle_message(update, context):
    user_message = update.message.text

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-7b",
                "messages": [{"role": "user", "content": user_message}]
            }
        )

        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        else:
            bot_reply = f"Ошибка API: {response.text}"

    except Exception as e:
        bot_reply = f"Произошла ошибка: {e}"

    await update.message.reply_text(bot_reply)

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()