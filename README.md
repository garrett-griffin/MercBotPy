# Mercbot

This project is a quality-of-life tool for the game Mercatorio, designed to automate and optimize various in-game tasks.

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/mercbot.git
   cd mercbot
   ```

2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

3. Create a `.env` file with your credentials:
   ```sh
   echo 'BOT_USER=["youruser@gmail.com"]' > mercbot/.env
   echo 'BOT_TOKEN=["yourtoken"]' >> mercbot/.env
   echo 'BOT_NICKNAMES=["nickname"]' >> mercbot/.env
   ```

4. Initialize settings:
   ```sh
   poetry run initialize-settings
   ```

5. Run the bot:
   ```sh
   poetry run run-bot
   ```

## Development

To add new dependencies, use:
```sh
poetry add <package-name>
```
