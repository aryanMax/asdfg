from .__init__ import *


@bot.on_message(filters.command(['start']) & filters.private)
async def start(_, message):
    await message.reply_text("<code>I am Alive :)</code>")
