import asyncio

import aiohttp
import feedparser

from rssdiscoveryengine_app.headers import HTTP_HEADERS
from rssfinderasync import rssfinderhelpers as helpers


async def fetch(blog_url, session):
    rss_url = None
    result = None
    try:
        async with session.get(blog_url, timeout=4) as response:
            result = await response.read()
    except Exception as e:
        print(f"<Exception>{e}</Exception><blog_url>{blog_url}</blog_url>")

    if result:
        rss_url = helpers.find_rss_url_in_html(result)

    if not rss_url:
        rss_url = helpers.build_possible_rss_url(blog_url)

    rss_url = helpers.add_protocol_urlprefix(blog_url, rss_url)

    try:
        async with session.get(rss_url) as response:
            if response.status != 200 \
            or not helpers.is_rss_content_type(response.headers["Content-Type"]):
                return

            feed = feedparser.parse(await response.read())
            if feed.bozo > 0:
                print(f"BOZO FOUND: {rss_url}")
                return
            return feed.feed
    except Exception as e:
        print(f"<Exception>{e}</Exception><blog_url>{blog_url}</blog_url>")

async def fetch_bound_async(sem, url, session):
    async with sem:
        result = await fetch(url, session)
        return result

async def run(urls):
    sem = asyncio.Semaphore(1000)
    tasks = []
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout, headers=HTTP_HEADERS) as session:
        for url in urls:
            task = asyncio.ensure_future(
                fetch_bound_async(sem, url, session)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

def initiate_finder(blog_url):
    blog_url = blog_url.strip()
    html = helpers.get_response_content(blog_url)
    if not html:
        return

    rss_url = helpers.find_rss_url_in_html(html)
    if not rss_url:
        rss_url = helpers.build_possible_rss_url(blog_url)

    rss_url = helpers.add_protocol_urlprefix(blog_url, rss_url)

    urls = helpers.get_urls_from_rss_feed(rss_url)
    if not urls:
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(run(urls))
    result = loop.run_until_complete(future)

    result = helpers.find_unique_results(result)
    return result
