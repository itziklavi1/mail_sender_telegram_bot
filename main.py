import logging
import re
import subprocess
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import smtplib
from email.message import EmailMessage

TOKEN = "7068105090:AAHQYtOzTDAAQZTEnNkuVdXSfmCPpBcVAr0"
BOT_USERNAME = "@Itzik_mail_sender_bot"

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter email")
    logger.info("Requested user to enter email")
    context.chat_data['last_message'] = "Please enter email"


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    context.chat_data['last_message'] = "What's your file?"
    # Validate email address
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        await update.message.reply_text("Email address is not valid. Try again with /start command.")
        logger.info("Invalid email address provided")
        return
    context.user_data['email'] = email
    await update.message.reply_text("What's your file?")
    logger.info(f"Received email: {email}")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received file.")
    file = update.message.document
    file_name = file.file_name
    logger.info(f"Received file: {file_name}")
    email = context.user_data.get('email')
    context.chat_data['last_message'] = "What's your file?"
    # Get file information
    file_obj = await context.bot.get_file(file_id=file.file_id)
    file_url = file_obj.file_path
    # Download the file
    logger.info("file url is: ", file_url)
    logger.info("file name is: ", file_name)
    # Download the file using wget
    download_command = f"wget -O {file_name} {file_url}"
    logger.info(download_command)
    try:
        subprocess.run(download_command, shell=True, check=True)
        logger.info("File downloaded successfully")
        # Read the downloaded file
        with open(file_name, 'rb') as f:
            file_content = f.read()
        # Send email with attachment
        try:
            msg = EmailMessage()
            msg['From'] = 'telegramfilessebderbot038@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'File from Telegram Bot'
            msg.set_content('Please find the file attached.')
            msg.add_attachment(file_content, maintype='application', subtype='octet-stream', filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('telegramfilessebderbot038@gmail.com', 'lgwxbmngrfvaepqy')
                smtp.send_message(msg)
            await update.message.reply_text("Success")
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            await update.message.reply_text(f"Failed to send email: {e}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download file: {e}")
        await update.message.reply_text("Failure")

    # Clean up: remove the downloaded file
    # subprocess.run(f"rm -f {file_name}", shell=True)


async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_message = context.chat_data.get('last_message')
    if last_message == "Please enter email":
        email = update.message.text
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            await handle_email(update, context)
        else:
            await update.message.reply_text("Email address is not valid. Try again with /start command.")
            logger.info("Invalid email address provided")
    elif last_message == "What's your file?":
        if update.message.document:
            await handle_file(update, context)
        else:
            await update.message.reply_text("Please send a file.")
    else:
        await update.message.reply_text("Please use a valid command, try again with /start command")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


# Store the last message sent by the bot
async def store_last_message(update, context):
    if update.message and update.message.text:
        context.chat_data['last_message'] = update.message.text


# Test: Send file
async def send_document(update, context):
    chat_id = update.message.chat_id
    document = open('11.png', 'rb')
    await context.bot.send_document(chat_id, document)


if __name__ == '__main__':
    logger.info('The bot starting')
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('send', send_document))

    # Message Handlers
    app.add_handler(MessageHandler(filters.Regex(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"), handle_email))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT, handle_response))

    # Errors
    app.add_error_handler(error)

    logger.info('Polling ...')
    app.run_polling(poll_interval=3)
