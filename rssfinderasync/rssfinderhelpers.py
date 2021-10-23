from urllib.parse import urlparse

import feedparser
import requests
import html
from bs4 import BeautifulSoup

def get_response_content(url):
    response = None
    try:
        response = requests.get(url)
    except:
        return

    if not response.ok:
        return

    return response.content

def find_rss_url_in_html(html):

    soup = BeautifulSoup(html, "html.parser", from_encoding="iso-8859-1")
    link_tag = soup.find("link", {"type":"application/rss+xml"})

    if link_tag is None:
        link_tag = soup.find("link", {"type":"application/atom+xml"})
    
    if link_tag is None:
        return None
    
    rss_url = link_tag.get("href")
    return rss_url


def build_possible_rss_url(url):
    parsed = urlparse(url)
    if not parsed.scheme in ['http', 'https']:
        return None
    # Remove query string & fragment noise if present
    parsed = parsed._replace(path='/feed', query='', fragment='')
    return parsed.geturl()


def add_protocol_urlprefix(blog_url, rss_url):
    if rss_url.startswith('//'):
        rss_url = blog_url.split('//')[0] + rss_url
    elif rss_url.startswith('/'):
        url_split = blog_url.split('/')
        rss_url = url_split[0] + '//' + url_split[2] + rss_url

    return rss_url

def get_urls_from_rss_feed(rss_url):
    feed = feedparser.parse(rss_url)
    if feed.bozo > 0:
        return

    urls = []
    for entry in feed.entries:
        anchors = find_anchors(entry)
        for anchor in anchors:
            url = anchor.get("href")
            if is_valid_url(url):
                urls.append(url)

    return urls

def find_anchors(entry):
    soup = BeautifulSoup(entry.description, "html.parser")
    anchors = soup.find_all('a')

    if entry.has_key('content'):
        for content in entry.content:
            soup = BeautifulSoup(content.value, "html.parser")
            anchors += soup.find_all('a')
    return anchors

def is_valid_url(url):
    return url and url.startswith("http")

def is_rss_content_type(content_type):
    if content_type.startswith("application/rss") \
    or content_type.startswith("application/atom") \
    or content_type.startswith("application/xml"):
        return True
    return False

# mutates feedparser object
def unescape_feed(feed):
    if "title" in feed:
        feed["title"] = html.unescape(feed["title"])
    if "title_detail" in feed:
        title_detail = feed["title_detail"]
        if "value" in title_detail:
            title_detail["value"] = html.unescape(title_detail["value"])
    return feed

def find_unique_results(results):
    results = [x for x in results if x is not None]
    unique = {}
    for result in results:
        if not result.link in unique:
            unique[result.link] = result

    return unique.values()
