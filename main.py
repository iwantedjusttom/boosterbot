# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import discord
from playwright.async_api import async_playwright

TOKEN = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def get_mmr(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3000)  # Wait for MMR content to load

        try:
            cards = await page.query_selector_all("div.trn-card--dark")
            results = []

            for card in cards:
                header = await card.query_selector("div.trn-card__header")
                if not header:
                    continue
                mode = await header.inner_text()

                mmr_el = await card.query_selector("div.trn-defstat__value")
                if mmr_el:
                    mmr = await mmr_el.inner_text()
                    results.append(f"{mode.strip()}: {mmr.strip()}")

            return "\n".join(results) if results else "Couldn't find MMRs."

        except Exception as e:
            return f"Error while fetching MMR: {e}"
        finally:
            await browser.close()

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!mmr'):
        parts = message.content.split(' ')
        if len(parts) < 2:
            await message.channel.send("Please provide a valid Rocket League Tracker URL.")
            return

        url = parts[1]
        await message.channel.send("Fetching MMR, please wait...")
        mmr = await get_mmr(url)
        await message.channel.send(f"MMR results:\n{mmr}")

client.run(TOKEN)
