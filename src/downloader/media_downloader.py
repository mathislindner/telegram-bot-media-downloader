import os
import yt_dlp
import logging

logger = logging.getLogger(__name__)

def get_save_location(file_website: str, file_type: str) -> str:
    """
    Returns the folder where the music will be saved.
    """
    return f"/downloads/{file_website}/{'singles' if file_type == 'single' else ''}"

def download_music(file_link: str, folder: str) -> str:
    """
    Downloads music and saves it in the specified folder.
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

    logger.info(f"Downloaded {video_title}")
    return video_title
