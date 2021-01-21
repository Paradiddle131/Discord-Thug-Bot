import os
import re

import bs4
import discord
import requests
from dotenv import load_dotenv
from keep_alive import keep_alive

client = discord.Client()


def thug_out(input_text):
    params = {"translatetext": input_text}
    target_url = "http://www.gizoogle.net/textilizer.php"
    resp = requests.post(target_url, data=params)
    soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
    soup = bs4.BeautifulSoup(soup_input, "html")
    giz = soup.find_all(text=True)
    return giz[38].strip("\r\n")


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$thugout"):
        await message.channel.send(thug_out(' '.join(message.content.split(" ")[1:])))
    print('Message from {0.author}: {0.content}'.format(message))


load_dotenv("config.env")
# keep_alive()
client.run(os.getenv("token"))
