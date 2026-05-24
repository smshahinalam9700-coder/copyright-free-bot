import os
from pyrogram import Client, filters

app = Client(
    "my_bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("বট সচল আছে!")

app.run()
