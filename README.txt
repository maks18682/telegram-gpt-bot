
📦 GPT Telegram Bot (Render Deployment)

1. Перейди на https://render.com и зарегистрируйся (можно через GitHub)
2. Создай новый Web Service → подключи репозиторий GitHub (с этим архивом)
3. Render автоматически прочтёт `render.yaml` и развернёт бота
4. Перейди в Settings → Environment → Add Environment Variables:

   TELEGRAM_TOKEN = (твой токен бота из BotFather)
   OPENROUTER_API_KEY = (твой токен вида sk-or-...)

5. Нажми "Deploy" — бот будет работать 24/7 🎉

Модель по умолчанию: mistralai/mistral-7b-instruct:free
