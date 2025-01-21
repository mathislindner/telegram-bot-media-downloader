import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAMBOTTOKEN = os.getenv("TELEGRAMBOTTOKEN")
DOWNLOADS_DIR = "/downloads"
