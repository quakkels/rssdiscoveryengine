from setuptools import find_packages, setup

setup(
	name='tiaamd',
	version='0.1.2',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'flask',
		'beautifulsoup4',
		'feedparser',
		'requests',
		'aiohttp',
		'asyncio',
		'gunicorn'
	],
	python_requires='>=3.7'
)
