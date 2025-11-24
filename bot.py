#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load env variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Add your chat ID in .env


# ----------------------------
# Commands
# ----------------------------
async def start(update, context):
    await update.message.reply_text("Hello! Your credit-card reminder bot is active. 🚀")

async def test(update, context):
    await update.message.reply_text("Test successful — bot is working! ✅")


# ----------------------------
# Monthly Reminder Function
# ----------------------------
async def send_monthly_reminder(app):
    msg = (
        "📅 *Monthly Credit Card Tasks*\n"
        "--------------------------------------\n"
        "➡️ Buy Amazon Pay vouchers (Infinia/Emeralde)\n"
        "➡️ Buy Flipkart vouchers\n"
        "➡️ Buy Myntra vouchers\n"
        "➡️ Track ICICI Emeralde 10L milestone\n"
        "➡️ Log monthly spends in tracker\n"
    )

    await app.bot.send_message(
        chat_id=CHAT_ID,
        text=msg,
        parse_mode="Markdown"
    )


# ----------------------------
# MAIN
# ----------------------------
async def main():
    app = Application.builder().token(TOKEN).build()

    # Add bot commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))

    # APScheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_monthly_reminder,
        trigger="cron",
        day=1,
        hour=9,
        minute=0,
        args=[app]
    )
    scheduler.start()

    print("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
