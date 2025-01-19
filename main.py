#from dotenv import load_dotenv
import os
import logging
import yt_dlp
import json
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler


# https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py
logger = logging.getLogger(__name__)

# Pre-assign button text
SELECT_GROUP = "Select a group"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

def download_music(file_link: str, folder: str) -> str:
    """
    This function downloads the music from the link and saves it in the folder
    """

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'ffmpeg_location': r'C:\Users\mathi\Documents\GH\telegram-bot-media-downloader\ffmpeg',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(file_link, download=False)
        video_title = info_dict.get('title', None)
        ydl.download([file_link])
    return video_title

def process_link(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """
    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    file_info = {
        "file_link" : None,
        "file_name" : None,
        "file_website" : None,
    }
    if not update.message.text:
        # This is equivalent to forwarding, without the sender's name
        update.message.copy(update.message.chat_id)

    #verify if the message is a link
    if update.message.entities[0].type == "url":
        file_info["file_link"] = update.message.text
        context.bot.send_message(
            update.message.chat_id,
            text="Successfully received the link! Processing...",
            # To preserve the markdown, we attach entities (bold, italic...)
            entities=update.message.entities
            )
        # cehck which website the link is from (youtube or soundcloud)
        if "youtube" in file_info["file_link"]:
            file_info["file_website"] = "youtube"
        elif "soundcloud" in file_info["file_link"]:
            file_info["file_website"] = "soundcloud"
        else:
            update.message.reply_text(
                "Sorry, I can only process links from YouTube and SoundCloud. Please try again.",
                reply_markup=ForceReply(selective=True)
            )
            return
        download_music(file_info["file_link"], "downloads")
        
        
    else:
        update.message.reply_text(
            "Please send a link to proceed.",
            reply_markup=ForceReply(selective=True)
        )
        return
    

def help(update: Update, context: CallbackContext) -> None:
    """
    This function is called when the user sends the /start command
    """
    update.message.reply_text(
        "Hello! I am a bot that can help you with your group management. Please select a group to start.",
        reply_markup=ForceReply(selective=True)
    )

def main() -> None:
    """
    This is the main function that runs the bot
    """
    # Load the environment variables
    #load_dotenv('.env')
    TELEGRAMBOTTOKEN = os.getenv("TELEGRAMBOTTOKEN")
    DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER")
    updater = Updater(TELEGRAMBOTTOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # send any message to the process_link function that is not a command
    dispatcher.add_handler(MessageHandler(~filters.Filters.command, process_link))

    # Register commands
    dispatcher.add_handler(CommandHandler("help", help))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()