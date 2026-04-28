import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id
    user_state[user_id] = False

    await update.message.reply_text(
        "👋 Hello!\n\nShould we start the translation?\nReply YES or NO"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id
    text = update.message.text.lower()

    if user_id not in user_state:
        user_state[user_id] = False

    if text == "yes":
        user_state[user_id] = True
        await update.message.reply_text("✅ Great! Send me a sentence to translate.")
        return

    if text == "no":
        user_state[user_id] = False
        await update.message.reply_text("❌ Okay, translation stopped. Send /start to restart.")
        return

    if user_state[user_id]:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            await update.message.reply_text(f"🌍 Translated:\n{translated}")
        except Exception:
            await update.message.reply_text("⚠️ Translation failed. Try again.")
    else:
        await update.message.reply_text("⚠️ Please type /start first.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
