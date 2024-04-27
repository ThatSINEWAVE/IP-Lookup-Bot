import discord
from discord.ext import commands
import requests
import json
import logging
from datetime import datetime
import whois

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Configure logging
logging.basicConfig(filename='logger.txt', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Read config from file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Access token and guild ID
TOKEN = config.get('token')
GUILD_ID = int(config.get('guildId'))
bot = commands.Bot(command_prefix='/', intents=intents)

API_BASE_URL = 'https://api.hackertarget.com/'


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="networks"))

    # Sync the slash commands with Discord
    await bot.tree.sync()


@bot.tree.command(name='check', description="Check any IP")
async def check_ip_info(interaction: discord.Interaction, ip_address: str):
    try:
        # Log user information
        user_info = f'User: {interaction.user.name} (ID: {interaction.user.id})'
        logging.info(user_info)

        # Make a request to ip-api.com
        response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query')
        data = response.json()

        # Check if the request was successful
        if data['status'] == 'fail':
            raise Exception(data.get('message', 'Unknown error'))

        # Extract relevant information
        country = data.get('country', 'N/A')
        city = data.get('city', 'N/A')
        region = data.get('regionName', 'N/A')
        district = data.get('district', 'N/A')
        zip_code = data.get('zip', 'N/A')
        latitude = data.get('lat', 'N/A')
        longitude = data.get('lon', 'N/A')
        timezone = data.get('timezone', 'N/A')
        isp = data.get('isp', 'N/A')
        org = data.get('org', 'N/A')
        as_number = data.get('as', 'N/A')
        as_name = data.get('asname', 'N/A')
        reverse_dns = data.get('reverse', 'N/A')
        mobile = data.get('mobile', 'N/A')
        proxy = data.get('proxy', 'N/A')
        hosting = data.get('hosting', 'N/A')

        # Format and send the response with detailed information
        response_msg = (
            f'## IP Information for {ip_address}:\n'
            f'**Country:** {country}\n'
            f'**City:** {city}\n'
            f'**Region:** {region}\n'
            f'**District:** {district}\n'
            f'**Zip Code:** {zip_code}\n'
            f'**Latitude:** {latitude}\n'
            f'**Longitude:** {longitude}\n'
            f'**Timezone:** {timezone}\n'
            f'**Currency:** {currency}\n'
            f'**ISP:** {isp}\n'
            f'**Organization:** {org}\n'
            f'**AS Number:** {as_number}\n'
            f'**AS Name:** {as_name}\n'
            f'**Reverse DNS:** {reverse_dns}\n'
            f'**Mobile:** {mobile}\n'
            f'**Proxy:** {proxy}\n'
            f'**Hosting:** {hosting}'
        )

        # Log the response
        logging.info(response_msg)

        # Send the response to the user
        await interaction.response.send_message(response_msg)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='reversedns', description="Perform reverse DNS lookup")
async def reversedns_lookup(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(API_BASE_URL + f'reversedns/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='dnslookup', description="Perform DNS lookup")
async def dns_lookup(interaction: discord.Interaction, input_domain: str):
    try:
        response = requests.get(API_BASE_URL + f'dnslookup/?q={input_domain}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='hostsearch', description="Search for hosts sharing the same DNS")
async def host_search(interaction: discord.Interaction, input_domain: str):
    try:
        response = requests.get(API_BASE_URL + f'hostsearch/?q={input_domain}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='shareddns', description="Find shared DNS entries")
async def shared_dns(interaction: discord.Interaction, input_dns: str):
    try:
        response = requests.get(API_BASE_URL + f'findshareddns/?q={input_dns}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='whois', description="Perform WHOIS lookup")
async def whois_lookup(interaction: discord.Interaction, input_domain_or_ip: str):
    try:
        whois_info = whois.whois(input_domain_or_ip)
        whois_output = ''
        for key, value in whois_info.items():
            whois_output += f'{key}: {value}\n'
        output = f'```\n{whois_output}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='reverseip', description="Perform reverse IP lookup")
async def reverse_ip_lookup(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(API_BASE_URL + f'reverseiplookup/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='aslookup', description="Perform AS lookup")
async def as_lookup(interaction: discord.Interaction, input_ip_or_as: str):
    try:
        response = requests.get(API_BASE_URL + f'aslookup/?q={input_ip_or_as}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)


@bot.tree.command(name='ipgeo', description="Get IP geolocation information")
async def ip_geolocation(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(API_BASE_URL + f'ipgeo/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        error_msg = f'Error: {e}'
        logging.error(error_msg)
        await interaction.response.send_message(error_msg)

# Run the bot with the token
bot.run(TOKEN)
