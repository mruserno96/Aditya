import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read credentials from environment variables (set these in Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")

ALLOWED_USERS = [
    int(os.getenv("TELEGRAM_ID_1", "0")),
    int(os.getenv("TELEGRAM_ID_2", "0"))
]

if not BOT_TOKEN or not FAST2SMS_API_KEY:
    raise SystemExit("Missing BOT_TOKEN or FAST2SMS_API_KEY environment variables.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access Denied.")
        return
    await update.message.reply_text("✅ Hello! Use /sms <number> <message> to send SMS.")

async def send_sms_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access Denied.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /sms <number> <message>")
        return

    number = context.args[0]
    message = " ".join(context.args[1:])

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "message": message,
        "route": "v3",
        "numbers": number
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        resp = requests.post(url, data=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            # Fast2sms returns JSON; adapt messaging if needed
            await update.message.reply_text("📩 SMS Sent Successfully!")
        else:
            await update.message.reply_text(f"❌ Failed ({resp.status_code}): {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sms", send_sms_cmd))
    print("Bot started. Waiting for updates...")
    app.run_polling()

if __name__ == "__main__":
    main()
