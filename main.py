import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Setup logging so you can see errors in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Use an environment variable for the token (safer for rendering/hosting)
TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN_HERE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your bot 🤖")

if __name__ == "__main__":
    # 3. Build the application
    app = ApplicationBuilder().token(TOKEN).build()

    # 4. Add handlers
    app.add_handler(CommandHandler("start", start))

    # 5. Run the bot
    print("Bot is polling...")
    app.run_polling()
