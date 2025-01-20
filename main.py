from dotenv import load_dotenv
import os
import logging
import yt_dlp
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Load the environment variables
load_dotenv('.env')
TELEGRAMBOTTOKEN = os.getenv("TELEGRAMBOTTOKEN")
logger = logging.getLogger(__name__)

def download_music(file_link: str, folder: str) -> str:
    """
    This function downloads the music from the link and saves it in the folder
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
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
    logger.info(f"Received a message from {update.message.chat_id}")

    file_info = {
        "file_link" : None,
        "file_website" : None,
    }
    if not update.message.text:
        # This is equivalent to forwarding, without the sender's name
        update.message.copy(update.message.chat_id)

    #verify if the message is a link
    if update.message.entities[0].type == "url":
        file_info["file_link"] = update.message.text
        send_message_to_user(update, context, "Successfully received the link! Processing...")
        # cehck which website the link is from (youtube or soundcloud)
        if "youtube" in file_info["file_link"] or "youtu.be" in file_info["file_link"]:
            file_info["file_website"] = "youtube"
        elif "soundcloud" in file_info["file_link"]:
            file_info["file_website"] = "soundcloud"
        else:
            send_message_to_user(update, context, "Sorry, I can only download from Youtube and Soundcloud. Please send a valid link.")
            return
        video_title = download_music(file_info["file_link"], f"/downloads/{file_info['file_website']}/")
        logger.info(f"Downloaded {video_title}")
        send_message_to_user(update, context, f"Successfully downloaded {video_title}.")
        
    else:
        update.message.reply_text(
            "Please send a link to proceed.",
            reply_markup=ForceReply(selective=True)
        )
        return
    
def send_message_to_user(update: Update, context: CallbackContext, message: str) -> None:
    """
    This function sends a message to the user
    """
    update.message.reply_text(
        message,
        reply_markup=ForceReply(selective=True)
    )

def help(update: Update, context: CallbackContext) -> None:
    """
    This function is called when the user sends the /help command
    """
    update.message.reply_text(
        "Hello! I am a bot that can help you with downloading music from Youtube and Soundcloud. Please send me a link to the music you want to download.",
        reply_markup=ForceReply(selective=True)
    )

def main() -> None:
    """
    This is the main function that runs the bot
    """
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