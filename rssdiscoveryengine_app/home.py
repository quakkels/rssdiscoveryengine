from flask import (
	Blueprint, 
	render_template, 
	abort, 
	request, 
	flash
	)
from jinja2 import TemplateNotFound
from rssfinderasync import rfasync

bp = Blueprint('home', __name__,
	template_folder='templates')

@bp.route('/', methods=(['GET']))
def index():
	results = None
	blog_url = request.args.get('blog_url')
	print(f'blog_url: {blog_url}')
	if blog_url is None:
		blog_url = ''
	elif is_blog_url_valid(blog_url):
		results = rfasync.initiate_finder(blog_url)
		print("finished getting results")

	return render_template('home.html', blog_url = blog_url,
		results = results)

def is_blog_url_valid(blog_url):
	has_http = blog_url.lower().startswith("http")
	has_slashes = "://" in blog_url
	return has_http and has_slashes