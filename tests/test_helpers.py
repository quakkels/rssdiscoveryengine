from rssfinderasync.rssfinderhelpers import build_possible_rss_url


def test_build_possible_rss_url():
    assert build_possible_rss_url('mailto:rdengine@example.invalid') is None
    assert build_possible_rss_url('https://example.invalid/') == 'https://example.invalid/feed'
    assert build_possible_rss_url('https://example.invalid/subpath/') == 'https://example.invalid/feed'
    assert build_possible_rss_url('https://example.invalid/?q=5') == 'https://example.invalid/feed'
    assert build_possible_rss_url('https://example.invalid/#fragment') == 'https://example.invalid/feed'
