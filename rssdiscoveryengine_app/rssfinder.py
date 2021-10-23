from time import sleep

import feedparser
import requests
from bs4 import BeautifulSoup

from rssfinderasync.rssfinderhelpers import build_possible_rss_url

# Autoreload imported scripts without restarting the repl:
# https://ipython.org/ipython-doc/3/config/extensions/autoreload.html

ignore = [
	'https://amzn.to',
	'https://amazon.com',
	'https://twitter.com',
	'https://t.co',
	'https://www.instagram.com'
]
agent = 'RSS Discovery Engine 0.1'
request_headers = {
	'User-Agent': agent
}


def find_links(url):
	feeds = []
	discarded = []
	result = feedparser.parse(url)

	if result.bozo > 0:
		# there were errors parsing the feed
		print("error parsing the feed.")
		return feeds

	print(f'found {len(result.entries)} entries')

	for entry in result.entries:
		anchors = find_anchors(entry)
		print(f'found {len(anchors)} anchors')

		for anchor in anchors:
			link = anchor.get('href')
			print(link)

			if is_ignored(ignore, link):
				print(f'Ignored (default): {link}')
				continue

			if is_ignored(discarded, link):
				print(f'Ignored (discarded): {link}')
				continue

			if is_ignored([o.link for o in feeds], link):
				continue

			if link.startswith(result.feed.link):
				print(f'Url skipped: {link} is in {result.feed.link}')
				continue

			rss_url = find_rss_url(link)
			print(f"rss: {rss_url}")
			sleep(0.2)

			if not rss_url:
				discarded.append(link)
				continue

			found_rss_result = feedparser.parse(rss_url)
			if found_rss_result.bozo > 0:
				discarded.append(link)
				continue
			
			if not found_rss_result.feed.has_key('link'):
				discarded.append(link)
			else:
				feeds.append(found_rss_result.feed)
				print(link)

	return feeds

def find_rss_url(original_url):
	url = original_url
	if not original_url.startswith('http'):
		url = f"https://{original_url}"

	is_valid_response = False
	response = None
	try:
		response = get_request(url)
		is_valid_response = True
	except:
		print(f"Error when finding RSS for {url}")

	if not is_valid_response:
		if not original_url.startswith('http'):
			url = f'http://{original_url}'
			try:
				response = get_request(url)
				is_valid_response = True
			except:
				print(f"Error when finding RSS for {url}")
				return

	if not response or not response.ok:
		print(f"Response was not ok {url}")
		return
	
	soup = BeautifulSoup(response.content, "html.parser")
	link_tag = soup.find('link', {'type':'application/rss+xml'})

	rss_link = None
	if link_tag is None:
		link_tag = soup.find('link', {'type':'application/atom+xml'})
	
	if link_tag is None:
		response = None
		possible_feed_url = build_possible_rss_url(url)
		try:
			response = get_request(possible_feed_url)
		except:
			pass

		if response.ok:
			rss_link = possible_feed_url

	if link_tag is None and rss_link is None:
		return

	if rss_link is None:
		rss_link = link_tag.get('href')

	if rss_link.startswith('//'):
		rss_link = url.split('//')[0] + rss_link
	
	elif rss_link.startswith('/'):
		url_split = url.split('/')
		rss_link = url_split[0] + '//' + url_split[2] + rss_link

	try:
		rss_response = get_request(rss_link)
	except:
		print(f"Error when validating RSS link {rss_link}")
		return

	if rss_response.status_code != 200:
		print("rss response was not 200")
		return

	return rss_link

def get_request(url):
	return requests.get(url, headers=request_headers)

def find_anchors(entry):
	soup = BeautifulSoup(entry.description, "html.parser")
	anchors = soup.find_all('a')

	if entry.has_key('content'):
		for content in entry.content:
			soup = BeautifulSoup(content.value, "html.parser")
			anchors += soup.find_all('a')
	return anchors

def is_ignored(ignoreThese, link):
	for ignore in ignoreThese:
		if link.startswith(ignore):
			return True
	return False
