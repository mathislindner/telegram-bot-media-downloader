# Telegram Bot Media Downloader

This Telegram bot allows users to download media from various sources directly within the Telegram app using the well maintained yt-dlp.

## Features

- Download music from youtube or souncloud through a telegram bot
- Support for multiple media sources
- Easy-to-use commands

## Installation

### Using Docker

1. Pull the Docker image:
    ```sh
    docker pull ghcr.io/mathislindner/telegrambotmediadownloader:latest
    ```
2. Run the Docker container with your Telegram API token and mount a local directory to `/downloads`:
    ```sh
    docker run -e TELEGRAM_API_TOKEN=your_api_token -v /path/to/local/downloads:/downloads ghcr.io/mathislindner/telegrambotmediadownloader:latest
    ```
### Note:
if you have ffmpeg installed on your host machine, consider building the container yourself to not waste space
## Commands

- `<URL>` - Download media from the provided URL
- `/help` - Get a list of available commands

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.