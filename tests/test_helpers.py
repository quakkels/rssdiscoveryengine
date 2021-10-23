import pytest

import rssfinderasync.rssfinderhelpers as helpers


def test_build_possible_rss_url():
    assert helpers.build_possible_rss_url('mailto:rdengine@example.invalid') is None
    assert helpers.build_possible_rss_url('https://example.invalid/') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/subpath/') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/?q=5') == 'https://example.invalid/feed'
    assert helpers.build_possible_rss_url('https://example.invalid/#fragment') == 'https://example.invalid/feed'



@pytest.mark.parametrize('content_type, expected', [
    ('application/rss', True),
    ('application/rss; charset=UTF-8', True),
    ('application/atom', True),
    ('application/xml', True),
    ('text/html', False),
])
def test_is_feed_content_type(content_type, expected):
    assert helpers.is_feed_content_type(content_type) is expected
