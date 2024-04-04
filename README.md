# IP Information Discord Bot

This is a Discord bot that allows users to check detailed information about any IP address using the ip-api.com API. The bot provides information such as country, city, region, district, zip code, latitude, longitude, timezone, currency, ISP, organization, AS number, AS name, reverse DNS, mobile status, proxy status, and hosting status.

## Features

- Discord command `/check <ip_address>` to retrieve detailed information about the specified IP address.
- Logging of user information and bot responses in a `logger.txt` file.
- Error handling for invalid IP addresses or API failures.

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

## Requirements

- Python 3.6 or higher
- `discord.py` library
- `requests` library

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a new Discord bot and obtain the bot token.
4. Create a new Discord server or use an existing one, and obtain the server ID (Guild ID).
5. Create a `config.json` file in the project directory with the following structure:

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "guildId": "YOUR_GUILD_ID_HERE"
}
```

Replace `YOUR_BOT_TOKEN_HERE` with your Discord bot token, and `YOUR_GUILD_ID_HERE` with the ID of your Discord server.

## Usage

1. Run the `main.py` script to start the bot.
2. In your Discord server, use the `/check <ip_address>` command to retrieve detailed information about the specified IP address.

The bot will respond with a formatted message containing the IP information, and the response will also be logged in the `logger.txt` file.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Warning:
This bot is not designed to scan or retrieve the IP addresses of Discord users. Using this bot for malicious purposes, such as attempting to obtain sensitive information or compromising user privacy, is strictly prohibited and goes against Discord's Terms of Service. Any unauthorized or unethical use of this bot will not be tolerated.
