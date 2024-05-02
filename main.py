import discord
from discord.ext import commands
import requests
import json
import logging
import whois
from dotenv import dotenv_values

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Configure logging
logging.basicConfig(filename='logger.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Read config from .env
config = dotenv_values(".env")

# Access token and guild ID
TOKEN = config.get('TOKEN')
GUILD_ID = int(config.get('GUILDID'))
bot = commands.Bot(command_prefix='/', intents=intents)

API_BASE_URL = 'https://api.hackertarget.com/'


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="networks"))

    # Sync the slash commands with Discord
    await bot.tree.sync()


async def print_error(e: Exception, interaction: discord.Interaction):
    error_msg = f'Error: {e}'
    logging.error(error_msg)
    await interaction.response.send_message(error_msg)


@bot.tree.command(name='check', description="Check any IP")
async def check_ip_info(interaction: discord.Interaction, ip_address: str):
    try:
        # Log user information
        user_info = f'User: {interaction.user.name} (ID: {interaction.user.id})'
        logging.info(user_info)

        # Make a request to ip-api.com
        response = requests.get(
            f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,isp,org,as,asname,reverse,mobile,proxy,hosting,query')
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
        await print_error(e, interaction)


@bot.tree.command(name='request', description="Make a request to any API or webpage")
async def make_request(interaction: discord.Interaction, url: str):
    try:
        # Log user information
        user_info = f'User: {interaction.user.name} (ID: {interaction.user.id})'
        logging.info(user_info)

        # Make the request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # If the response is JSON, format it nicely
            try:
                response_data = response.json()
                output = f'```json\n{json.dumps(response_data, indent=4)}\n```'
            except json.JSONDecodeError:
                # If not JSON, display the raw response
                output = f'```\n{response.text}\n```'
        else:
            output = f'Error: {response.status_code} - {response.reason}'

        # Log the response
        logging.info(output)

        # Send the response to the user
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='reversedns', description="Perform reverse DNS lookup")
async def reversedns_lookup(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(API_BASE_URL + f'reversedns/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='dnslookup', description="Perform DNS lookup")
async def dns_lookup(interaction: discord.Interaction, input_domain: str):
    try:
        response = requests.get(API_BASE_URL + f'dnslookup/?q={input_domain}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='hostsearch', description="Search for hosts sharing the same DNS")
async def host_search(interaction: discord.Interaction, input_domain: str):
    try:
        response = requests.get(API_BASE_URL + f'hostsearch/?q={input_domain}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='shareddns', description="Find shared DNS entries")
async def shared_dns(interaction: discord.Interaction, input_dns: str):
    try:
        response = requests.get(API_BASE_URL + f'findshareddns/?q={input_dns}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='whois', description="Perform WHOIS lookup")
async def whois_lookup(interaction: discord.Interaction, input_domain_or_ip: str):
    try:
        whois_info = dict(whois.whois(input_domain_or_ip))
        whois_output = ''
        for key, value in whois_info.items():
            whois_output += f'{key.replace("_", " ").title()}: {value}\n'
        output = f"```{whois_output}```"
        await interaction.response.send_message(output.replace("[", "").replace("]", "").replace("'", ""))
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='reverseip', description="Perform reverse IP lookup")
async def reverse_ip_lookup(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(
            API_BASE_URL + f'reverseiplookup/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='aslookup', description="Perform AS lookup")
async def as_lookup(interaction: discord.Interaction, input_ip_or_as: str):
    try:
        response = requests.get(API_BASE_URL + f'aslookup/?q={input_ip_or_as}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='ipgeo', description="Get IP geolocation information")
async def ip_geolocation(interaction: discord.Interaction, input_ip: str):
    try:
        response = requests.get(API_BASE_URL + f'ipgeo/?q={input_ip}')
        output = f'```\n{response.text}\n```'
        await interaction.response.send_message(output)
    except Exception as e:
        await print_error(e, interaction)


@bot.tree.command(name='checkinvite', description="Check Discord invite")
async def check_invite(interaction: discord.Interaction, invite_link: str):
    try:
        # Extract invite code from the link
        invite_code = invite_link.split('/')[-1]

        # Make a request to Discord API to get invite information
        response = requests.get(f'https://discord.com/api/v9/invites/{invite_code}')
        data = response.json()

        # Check if the request was successful
        if 'guild' in data:
            # Extract guild information
            guild_info = data['guild']
            guild_name = guild_info.get('name', 'Not found')
            guild_id = guild_info.get('id', 'Not found')
            guild_splash = guild_info.get('splash', 'Not found')
            guild_banner = guild_info.get('banner', 'Not found')
            guild_description = guild_info.get('description', 'Not found')
            guild_icon = guild_info.get('icon', 'Not found')
            guild_features = ', '.join(guild_info.get('features', ['Not found']))
            guild_verification_level = guild_info.get('verification_level', 'Not found')
            guild_vanity_url_code = guild_info.get('vanity_url_code', 'Not found')
            guild_nsfw_level = guild_info.get('nsfw_level', 'Not found')
            guild_nsfw = guild_info.get('nsfw', 'Not found')
            guild_premium_subscription_count = guild_info.get('premium_subscription_count', 'Not found')

            # Extract channel information
            channel_info = data['channel']
            channel_id = channel_info.get('id', 'Not found')
            channel_type = channel_info.get('type', 'Not found')
            channel_name = channel_info.get('name', 'Not found')

            # Format and send the response with invite information
            invite_info_msg = (
                f'**Guild Name:** {guild_name}\n'
                f'**Guild ID:** {guild_id}\n'
                f'**Guild Splash:** {guild_splash}\n'
                f'**Guild Banner:** {guild_banner}\n'
                f'**Guild Description:** {guild_description}\n'
                f'**Guild Icon:** {guild_icon}\n'
                f'**Guild Features:** {guild_features}\n'
                f'**Guild Verification Level:** {guild_verification_level}\n'
                f'**Guild Vanity URL Code:** {guild_vanity_url_code}\n'
                f'**Guild NSFW Level:** {guild_nsfw_level}\n'
                f'**Guild NSFW:** {guild_nsfw}\n'
                f'**Guild Premium Subscription Count:** {guild_premium_subscription_count}\n'
                f'**Channel ID:** {channel_id}\n'
                f'**Channel Type:** {channel_type}\n'
                f'**Channel Name:** {channel_name}\n'
                f'**Invite URL:** `{invite_link}`'
            )

            # Log the response
            logging.info(invite_info_msg)

            # Send the response to the user
            await interaction.response.send_message(invite_info_msg)
        else:
            # If the request was not successful, send an error message
            error_msg = "Error retrieving invite info. Please check the invite link and try again."
            logging.error(error_msg)
            await interaction.response.send_message(error_msg)
    except Exception as e:
        await print_error(e, interaction)


# Run the bot with the token
bot.run(TOKEN)