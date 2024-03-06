# Telegram Email Sender Bot

This is a Telegram bot script that allows users to send files via email. Users can interact with the bot to provide their email address and upload files, which will then be sent as email attachments.

## Features

- Provides a simple interface for users to enter their email address and send files.
- Validates email addresses to ensure proper formatting.
- Downloads files from Telegram and sends them as attachments via email.

## Getting Started

To use this bot, you need to follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your Telegram bot token and email credentials in the `main.py` script.
4. Run the bot by executing `python main.py`.
5. Start interacting with the bot in your Telegram chat.

## Usage

1. Start the bot by sending the `/start` command.
2. Follow the prompts to enter your email address and upload a file.
3. The bot will send the uploaded file to the provided email address as an attachment.

## Docker Support

You can also run this bot using Docker. Follow these steps:

1. Build the Docker image using the provided Dockerfile: `docker build -t telegram-email-bot .`
2. Run the Docker container: `docker run -d --name telegram-bot telegram-email-bot`

