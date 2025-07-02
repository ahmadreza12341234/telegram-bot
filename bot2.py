import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import subprocess

TOKEN = "7561047010:AAHhFnTvc16yTo3nH_V3ySd-TZfZ_y5ifT4"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک YouTube یا Instagram رو بفرست تا لینک دانلود بهت بدم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("در حال پردازش لینک... لطفاً صبر کن.")

    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-g", url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            download_link = result.stdout.strip()
            await update.message.reply_text(f"✅ لینک دانلود:\n{download_link}")
        else:
            await update.message.reply_text("❌ متأسفم، مشکلی در دریافت لینک پیش اومد.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطا: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()