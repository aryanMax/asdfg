from .__init__ import *


async def fetch_coomer_pages(post_url, message):
    i = 0
    total_img_urls = []
    total_vid_urls = []
    while True:
        url = post_url + f"?o={i}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("h2.post-card__heading")
            if len(posts) != 0:
                img_urls, vid_urls = await loop.run_in_executor(executor, lambda: fetch_posts(posts))
                total_img_urls += img_urls
                total_vid_urls += vid_urls
                await message.edit(f"<code>Fetched {len(total_img_urls)} Images and {len(total_vid_urls)} Videos. Fetching...</code>")
                i += 25
            else:
                break
        else:
            break
    return total_img_urls, total_vid_urls


def fetch_posts(posts):
    img_urls = []
    vid_urls = []
    for post in posts:
        try:
            post_url = "https://coomer.party" + post.find("a").get("href")
            each_post_img_urls, each_post_vid_urls = fetch_img_urls(post_url)
            img_urls = img_urls + each_post_img_urls
            vid_urls = vid_urls + each_post_vid_urls
        except Exception as e:
            continue

    return img_urls, vid_urls


def fetch_img_urls(post_url):
    response = requests.get(post_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        vid_urls = []
        img_urls = []
        posts = soup.select("a.fileThumb")
        vid_posts = soup.select("a.post__attachment-link")
        for post in posts:
            try:
                img_url = "https://coomer.party" + post.get("href")
                img_urls.append(img_url)
            except:
                continue

        for vid_post in vid_posts:
            try:
                vid_url = "https://coomer.party" + vid_post.get("href")
                vid_urls.append(vid_url)
            except:
                continue

        return img_urls, vid_urls
    else:
        return [], []
