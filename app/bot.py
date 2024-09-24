# app/bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from app.config import BOT_TOKEN, API_ID, API_HASH
from app.session_generator import generate_session_string

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PHONE, CODE = range(2)

async def start(update: Update, context):
    await update.message.reply_text("Welcome! Please send your phone number to generate a session string.")
    return PHONE

async def phone_number(update: Update, context):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Great! Now, please send the OTP you received.")
    return CODE

async def otp(update: Update, context):
    phone = context.user_data['phone']
    otp = update.message.text
    
    try:
        session_string = await generate_session_string(API_ID, API_HASH, phone, otp)
        await update.message.reply_text(f"Here's your session string:\n\n{session_string}\n\nKeep this string safe and do not share it with anyone!")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
    
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_number)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
