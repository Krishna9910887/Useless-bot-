import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import logging

logging.basicConfig(level=logging.INFO)

# Store each user's count and control flag
user_counters = {}
running = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not running.get(user_id):
        running[user_id] = True
        user_counters[user_id] = 0
        await update.message.reply_text("⏱️ Counter started! I’ll count every second.")

        asyncio.create_task(count_user(update, context, user_id))
    else:
        await update.message.reply_text("⏳ I'm already counting for you!")

async def count_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    while running.get(user_id):
        user_counters[user_id] += 1
        logging.info(f"User {user_id} count: {user_counters[user_id]}")
        await asyncio.sleep(1)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if running.get(user_id):
        running[user_id] = False
        await update.message.reply_text(f"🛑 Counter stopped at {user_counters.get(user_id, 0)}.")
    else:
        await update.message.reply_text("⚠️ Counter is not running.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = user_counters.get(user_id, 0)
    await update.message.reply_text(f"⏳ Your current count: {count}")

if __name__ == "__main__":
    # Your bot token
    BOT_TOKEN = "7821756495:AAH_ip-xpgU9wzeQZgv9XlYCYzmFaFVWUT4"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))

    print("✅ Bot is running...")
    app.run_polling()
