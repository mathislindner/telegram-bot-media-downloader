import logging
from telegram import Update, ForceReply
from telegram.ext import CallbackContext
from downloader.media_downloader import download_music, get_save_location

logger = logging.getLogger(__name__)

def send_message_to_user(update: Update, message: str) -> None:
    """ Sends a message to the user. """
    update.message.reply_text(message, reply_markup=ForceReply(selective=True))

def process_link(update: Update, context: CallbackContext) -> None:
    """ Handles incoming messages and processes links. """
    logger.info(f"Received a message from {update.message.chat_id}")

    if not update.message.text:
        update.message.copy(update.message.chat_id)
        return

    # Extract and verify URL
    file_link = update.message.text
    if not update.message.entities or update.message.entities[0].type != "url":
        send_message_to_user(update, "Please send a valid link.")
        return

    send_message_to_user(update, "Received the link! Processing...")

    # Determine the source (YouTube or SoundCloud)
    file_website = None
    file_type = "single"

    if "youtube" in file_link or "youtu.be" in file_link:
        file_website = "youtube"
        file_type = "playlist" if "playlist" in file_link else "single"
    elif "soundcloud" in file_link:
        file_website = "soundcloud"
        file_type = "playlist" if "sets" in file_link else "single"
    else:
        send_message_to_user(update, "Only YouTube and SoundCloud links are supported.")
        return

    # Download the file
    save_location = get_save_location(file_website, file_type)
    video_title = download_music(file_link, save_location)

    send_message_to_user(update, f"Downloaded: {video_title}")

def help_command(update: Update, context: CallbackContext) -> None:
    """ Sends help message to the user. """
    update.message.reply_text(
        "Send me a YouTube or SoundCloud link, and I'll download the music for you!",
        reply_markup=ForceReply(selective=True)
    )
