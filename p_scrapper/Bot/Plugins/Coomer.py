from .__init__ import *


@bot.on_message(filters.command(['coomer']) & filters.private)
async def coomer(_, message):
    args = message.text.split(" ")
    if len(args) <= 1:
        try:
            await message.delete()
        except:
            pass
        return
    link = args[-1].strip()

    if not re.search(r"https://.*?/onlyfans/user/.*?", link):
        return await message.reply_text("<code>This type of link is not supported</code>")

    link = clean_url(link)
    reply = await message.reply_text("<code>Starting to Scrape Coomer.party. Keep Patience this will take few minutes</code>")
    try:
        img_urls, vid_urls = await fetch_coomer_pages(link, reply)
        await reply.edit(f"<code>Fetched {len(img_urls)} Images. Now Sending...</code>")
        for i in range(len(img_urls)):
            _, ext = os.path.splitext(img_urls[i])
            try:
                await loop.run_in_executor(executor, lambda: dl_coomer_image(img_urls[i], i, ext))
                await bot.send_document(
                    document=f"coomer_image_{i+1}{ext}",
                    chat_id=message.chat.id,
                    disable_notification=True,
                    caption=f"<code>coomer_image_{i+1}</code>"
                )
                os.remove(f"coomer_image_{i+1}{ext}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                pass

        await reply.edit(f"<code>Sent {len(img_urls)} Images</code>")

        if len(vid_urls) != 0:
            vid_reply = await message.reply_text(f"<code>Fetched {len(vid_urls)} Videos. Now Sending...</code>")
            for i in range(len(vid_urls)):
                _, ext = os.path.splitext(vid_urls[i])
                try:
                    await loop.run_in_executor(executor, lambda: dl_coomer_video(vid_urls[i], i, ext))
                    await bot.send_document(
                        document=f"coomer_video_{i+1}{ext}",
                        chat_id=message.chat.id,
                        disable_notification=True,
                        caption=f"<code>coomer_video_{i+1}</code>"
                    )
                    os.remove(f"coomer_video_{i+1}{ext}")
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except:
                    pass
            await vid_reply.edit(f"<code>Sent {len(vid_urls)} Videos</code>")

    except:
        await reply.edit(f"<code>Failed to fetch from : {link}</code>")


def clean_url(url):
    if url.endswith("/"):
        return url.rstrip("/")
    elif re.search(r'\?o=', url):
        index = url.find("?o=")
        return url[slice(index)].rstrip("/")
    else:
        return url


def dl_coomer_video(link, index, ext):
    response = requests.get(link)
    if response.status_code == 200:
        with open(f"coomer_video_{index+1}{ext}", "wb") as video:
            video.write(response.content)


def dl_coomer_image(link, index, ext):
    response = requests.get(link)
    if response.status_code == 200:
        with open(f"coomer_image_{index+1}{ext}", "wb") as image:
            image.write(response.content)
