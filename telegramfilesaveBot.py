import os
import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = 'xxxyour tokenhere with '''
files_directory = 'collected_files'

if not os.path.exists(files_directory):
    os.makedirs(files_directory)

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a file with a name and I will save it. Use /get <name> to retrieve it.')

def save_file(update: Update, context: CallbackContext) -> None:
    if update.message.document:
        file_name = update.message.caption
        file_id = update.message.document.file_id

        if not file_name:
            update.message.reply_text('Please provide a name for the file in the caption.')
            return

        file = context.bot.get_file(file_id)
        file.download(os.path.join(files_directory, file_name))
        update.message.reply_text(f'Saved file as {file_name}.')

def get_file(update: Update, context: CallbackContext) -> None:
    file_name = ' '.join(context.args)

    if not file_name:
        update.message.reply_text('Please provide the name of the file you want to retrieve.')
        return

    file_path = os.path.join(files_directory, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f))
    else:
        update.message.reply_text('File not found.')

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document & ~Filters.command, save_file))
    dp.add_handler(CommandHandler('get', get_file, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
