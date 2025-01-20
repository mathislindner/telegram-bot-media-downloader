# Telegram Bot Media Downloader

This Telegram bot allows users to download media from various sources directly within the Telegram app.

## Features

- Download images, videos, and audio files
- Support for multiple media sources
- Easy-to-use commands

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/telegram-bot-media-downloader.git
    ```
2. Navigate to the project directory:
    ```sh
    cd telegram-bot-media-downloader
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Set up your Telegram bot by creating a new bot on [BotFather](https://core.telegram.org/bots#botfather) and obtaining the API token.
2. Configure the bot with your API token:
    ```sh
    export TELEGRAM_API_TOKEN=your_api_token
    ```
3. Create a `.env` file in the root directory, add your API token.
    ```sh
    TELEGRAM_API_TOKEN=your_api_token

    ```
3. Run the bot:
    ```sh
    python bot.py
    ```

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Get a list of available commands
- `/download <URL>` - Download media from the provided URL

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.