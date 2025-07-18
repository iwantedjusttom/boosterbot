import discord
import asyncio
from discord.ext import commands
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

import os

# Replace with your bot token
TOKEN = os.getenv("DISCORD_BOT_TOKEN") or "YOUR_DISCORD_BOT_TOKEN"
TARGET_URL = "https://example.com"  # Replace this with the real MMR page

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_mmr(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print("Navigating to URL...")
            await page.goto(url, timeout=15000)  # 15s timeout

            print("Waiting for MMR element...")
            await page.wait_for_selector("span.value", timeout=10000)

            element = await page.query_selector("span.value")
            mmr_text = await element.text_content() if element else None

            await browser.close()

            if mmr_text:
                return mmr_text.strip()
            else:
                return "Couldn't find MMR value on the page."

    except PlaywrightTimeout:
        return "Timeout while loading the page or selector."
    except Exception as e:
        return f"Unexpected error: {e}"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def mmr(ctx):
    await ctx.send("Fetching MMR, please wait...")
    mmr_result = await fetch_mmr(TARGET_URL)
    await ctx.send(f"MMR results:\n{mmr_result}")

if __name__ == "__main__":
    bot.run(TOKEN)
