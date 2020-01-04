import asyncio
from aiohttp import ClientSession
import feedparser
from . import rssfinderhelpers as helpers

async def fetch(blog_url, session):
    rss_url = None
    async with session.get(blog_url) as response:
        result = await response.read()
    
    rss_url = helpers.find_rss_url_in_html(result)

    if not rss_url:
        rss_url = helpers.build_possible_rss_url(blog_url)
    
    rss_url = helpers.add_protocol_urlprefix(blog_url, rss_url)

    print(f"LOOKING {rss_url} from {blog_url}")
    async with session.get(rss_url) as response:
        if response.status != 200 \
        or not helpers.is_rss_content_type(response.headers["Content-Type"]):
            print(f"NOTFOUND: rss found {rss_url}")
            return

        feed = feedparser.parse(await response.read())
        if feed.bozo > 0:
            print(f"BOZO FOUND: {rss_url}")
        print(f"FOUND: end fetch {blog_url}")
        return feed.feed

async def fetch_bound_async(sem, url, session):
    async with sem:
        result = await fetch(url, session)
        return result

async def run(urls):
    print("start run()")
    sem = asyncio.Semaphore(500)
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(
                fetch_bound_async(sem, url, session)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print("end run()")
        return responses

def initiate_finder(blog_url):
    html = helpers.get_response_content(blog_url)
    if not html:
        return

    rss_url = helpers.find_rss_url_in_html(html)
    if not rss_url:
        rss_url = helpers.build_possible_rss_url(blog_url)

    rss_url = helpers.add_protocol_urlprefix(blog_url, rss_url)

    urls = helpers.get_urls_from_rss_feed(rss_url)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(run(urls))
    result = loop.run_until_complete(future)

    result = [x for x in result if x is not None]
    return result