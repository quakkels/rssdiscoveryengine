from flask import (
	Blueprint, 
	render_template, 
	abort, 
	request, 
	flash
	)
from jinja2 import TemplateNotFound
from . import rssfinder
from rssfinderasync import rfasync

bp = Blueprint('home', __name__,
	template_folder='templates')

@bp.route('/', methods=('GET', 'POST'))
def index():
	blog_url = ''
	results = None
	if request.method == 'POST':
		blog_url = request.form['blog_url']
		if blog_url is None:
			pass
		elif is_blog_url_valid(blog_url):
			# rss_feed_url = rssfinder.find_rss_url(blog_url)
			# results = rssfinder.find_links(rss_feed_url)
			results = rfasync.initiate_finder(blog_url)
			print("finished getting results")

	return render_template('home.html', blog_url = blog_url,
		results = results)

def is_blog_url_valid(blog_url):
	has_http = blog_url.lower().startswith("http")
	has_slashes = "://" in blog_url
	return has_http and has_slashes