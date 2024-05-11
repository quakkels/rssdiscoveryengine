import pytest

import rssfinderasync.rssfinderhelpers as helpers


def test_build_possible_rss_url():
    assert helpers.build_possible_rss_url('mailto:rdengine@example.invalid') is None
    assert helpers.build_possible_rss_url('https://example.invalid/') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/subpath/') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/?q=5') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/#fragment') == 'https://example.invalid/feed'

def test_add_protocol_urlprefix():
    assert helpers.add_protocol_urlprefix('https://blog.example.com', '//blog.example.com/path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/', '//blog.example.com/path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/index.xyz', '//blog.example.com/path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com', '/path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/index.xyz', '/path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com', 'path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/slug/#asdf', 'path/feed') == 'https://blog.example.com/slug/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com?dsa=asd', 'path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/index.xyz', 'path/feed') == 'https://blog.example.com/path/feed'
    assert helpers.add_protocol_urlprefix('https://blog.example.com/index.xyz?sdf=dsa', 'path/feed') == 'https://blog.example.com/path/feed'

@pytest.mark.parametrize('content_type, expected', [
    ('application/rss', True),
    ('application/rss; charset=UTF-8', True),
    ('application/atom', True),
    ('application/xml', True),
    ('text/html', False),
])
def test_is_feed_content_type(content_type, expected):
    assert helpers.is_feed_content_type(content_type) is expected
