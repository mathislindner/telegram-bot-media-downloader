import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from bot.handlers import process_link, help_command
from bot.config import TELEGRAMBOTTOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_bot():
    """ Initializes and starts the Telegram bot. """
    updater = Updater(TELEGRAMBOTTOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(~filters.Filters.command, process_link))

    # Start bot
    updater.start_polling()
    updater.idle()
