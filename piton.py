from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

TOKEN = "8787883919:AAEYdCdjmLYEz9UN85ARVX2OlAzMSywXGTc"

# stores user state (who agreed or not)
user_state = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_state[user_id] = False  # not ready yet

    await update.message.reply_text(
        "👋 Hello!\n\nShould we start the translation?\nReply YES or NO"
    )

# handle YES / NO + translations
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # if user hasn't been set yet
    if user_id not in user_state:
        user_state[user_id] = False

    # STEP 1: check YES/NO
    if text == "yes":
        user_state[user_id] = True
        await update.message.reply_text("✅ Great! Send me a sentence to translate.")
        return

    if text == "no":
        user_state[user_id] = False
        await update.message.reply_text("❌ Okay, translation stopped. Send /start to restart.")
        return

    # STEP 2: translation only if user agreed
    if user_state[user_id]:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        await update.message.reply_text(f"🌍 Translated:\n{translated}")
    else:
        await update.message.reply_text("⚠️ Please type /start first.")

# setup bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling() 