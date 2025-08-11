import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========================
# CONFIGURATION
# ========================
BOT_TOKEN = "7639952982:AAGqiiF4amQmv0yGD9MlzeXve6pz2MrGfGY"
FAST2SMS_API_KEY = "6CWt5YVjazIwOsuATZFMEo7m1H0RXLcJSU9G28Qvdxif4lyqN3kT5tENuMJw70fxemSiFqLa3UoQHDBr"

# Only these 2 Telegram IDs can use the bot
ALLOWED_USERS = [7993455374, 7357160729]  # Replace with your IDs

# ========================
# FUNCTIONS
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access Denied.")
        return
    await update.message.reply_text("✅ Welcome! Use /sms <number> <message> to send an SMS.")

async def send_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access Denied.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /sms <number> <message>")
        return

    number = context.args[0]
    message = " ".join(context.args[1:])

    # Send SMS via Fast2SMS API
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": number
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            await update.message.reply_text("📩 SMS Sent Successfully!")
        else:
            await update.message.reply_text(f"❌ Failed: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {e}")

# ========================
# MAIN
# ========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sms", send_sms))

    app.run_polling()

if __name__ == "__main__":
    main()
