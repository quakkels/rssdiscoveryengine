import requests
from bs4 import BeautifulSoup
import feedparser

def get_response_content(url):
    response = None
    try:
        response = requests.get(url)
    except requests.exceptions.SSLError:
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
    url_split = url.split('/')
    possible_url = url_split[0]+url_split[1]+'//'+url_split[2]+'/feed'
    return possible_url

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
    return url and not url.startswith("#") and not url.startswith("javascript:")

def is_rss_content_type(content_type):
    if content_type.startswith("application/rss") \
    or content_type.startswith("application/atom") \
    or content_type.startswith("application/xml"):
        return True
    return False