<div align="center">

# IP Information and Network Utilities Discord Bot

This is a Discord bot that provides various network utilities and IP information retrieval capabilities. It allows users to retrieve detailed information about IP addresses, perform DNS lookups, find shared DNS entries, conduct WHOIS queries, and make custom requests to APIs or web pages.

</div>

## Features

- `/check <ip_address>` to retrieve detailed information about the specified IP address, including country, city, region, geolocation, ISP, organization, and more.

- `/request <url>` to make custom requests to any API or web page and display the response.

- `/reversedns <ip_address>` to perform a reverse DNS lookup.

- `/dnslookup <domain>` to perform a DNS lookup.

- `/hostsearch <domain>` to search for hosts sharing the same DNS.

- `/shareddns <dns>` to find shared DNS entries.

- `/whois <domain_or_ip>` to perform a WHOIS lookup.

- `/reverseip <ip_address>` to perform a reverse IP lookup.

- `/aslookup <ip_or_as>` to perform an AS lookup.

- `/ipgeo <ip_address>` to retrieve IP geolocation information.

- `/checkinvite <invite_link>` to check discord invite links.

- Logging of user information, commands, and bot responses in a `logger.txt` file.

- Error handling for invalid inputs or API failures.

## Requirements

- Python 3.9.x recommended
- `discord.py==2.3.2`
- `requests==2.26.0`
- `python-whois==0.9.4`
- `aiohttp==3.9.5`
- `aiosignal==1.3.1`
- `attrs==23.2.0`
- `certifi==2024.2.2`
- `charset-normalizer==2.0.12`
- `discord-py-interactions==4.4.1`
- `frozenlist==1.4.1`
- `future==1.0.0`
- `idna==3.7`
- `multidict==6.0.5`
- `python-dotenv==1.0.1`
- `urllib3==1.26.18`
- `yarl==1.9.4`

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Installation

1. Clone the repository or download the source code.

2. Install the required dependencies by running `pip install -r requirements.txt`.

3. Create a new Discord bot and obtain the bot token.

4. Create a new Discord server or use an existing one, and obtain the server ID (Guild ID).

5. Create a `.env` file in the project directory, copy `.env.example` contents and paste in the new file.

6. Replace `TOKEN` with your bot token and `GUILDID` with your guild ID.

<div align="center">

# [Join my Discord server](https://discord.gg/2nHHHBWNDw)

</div>

## Usage

1. Run the `main.py` script to start the bot.

2. In your Discord server, use the various slash commands (e.g., `/check`, `/request`, `/reversedns`, etc.) to utilize the bot's network utilities and IP information retrieval capabilities.

The bot will respond with the requested information or the API/web page response, and the responses will also be logged in the `logger.txt` file.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

### Contributors

- Thanks to [Nitrrine](https://github.com/Nitrrine) for various improvements and fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Warning

This bot is designed for educational and network analysis purposes only. Using this bot for malicious purposes, such as attempting to obtain sensitive information or compromising user privacy, is strictly prohibited and goes against Discord's Terms of Service. Any unauthorized or unethical use of this bot will not be tolerated.
