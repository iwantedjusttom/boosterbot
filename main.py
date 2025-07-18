import discord
import asyncio
from discord.ext import commands
from playwright.async_api import async_playwright

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
TARGET_URL = "https://example.com"  # Replace with the actual URL to scrape

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_mmr(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_selector("span.value")

            mmr_element = await page.query_selector("span.value")
            mmr = await mmr_element.text_content()
            await browser.close()

            return mmr.strip()
    except Exception as e:
        return f"Error fetching MMR: {e}"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def mmr(ctx):
    await ctx.send("Fetching MMR, please wait...")
    mmr_value = await fetch_mmr(TARGET_URL)
    await ctx.send(f"MMR results:\n{mmr_value}")

if __name__ == "__main__":
    bot.run(TOKEN)
