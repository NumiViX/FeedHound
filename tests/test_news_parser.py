import sys
import time
import xml.etree.ElementTree as ET
from types import SimpleNamespace


class Entry(SimpleNamespace):
    def __contains__(self, item):
        return hasattr(self, item)

import pytest
import asyncio

# Prepare a minimal stub for the `feedparser` module so that project modules can
# import it even if the real package is absent.
feedparser_stub = sys.modules.setdefault("feedparser", SimpleNamespace())

from app.parsers.news_parser import parse_news
from app.parsers.sync_news_parser import parse_news_sync
from app.schemas.news import NewsCreate

MOCK_RSS = """<?xml version='1.0' encoding='UTF-8'?>
<rss version='2.0'>
<channel>
    <title>Mock Feed</title>
    <item>
        <title>Item 1</title>
        <link>http://example.com/1</link>
        <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
    </item>
    <item>
        <title>Item 2</title>
        <link>http://example.com/2</link>
        <pubDate>Tue, 02 Jan 2024 00:00:00 GMT</pubDate>
    </item>
</channel>
</rss>"""


def _build_parsed(feed: str):
    root = ET.fromstring(feed)
    entries = []
    for item in root.findall(".//item"):
        entries.append(
            Entry(
                title=item.findtext("title"),
                link=item.findtext("link"),
                published_parsed=time.strptime(
                    item.findtext("pubDate"), "%a, %d %b %Y %H:%M:%S %Z"
                ),
            )
        )
    return SimpleNamespace(entries=entries)


mock_parsed_feed = _build_parsed(MOCK_RSS)


def test_parse_news(monkeypatch):
    monkeypatch.setattr(feedparser_stub, "parse", lambda url: mock_parsed_feed, raising=False)
    result = asyncio.run(parse_news(1, "dummy"))

    assert len(result) == 2
    assert all(isinstance(item, NewsCreate) for item in result)
    assert [n.title for n in result] == ["Item 1", "Item 2"]
    assert [n.url for n in result] == ["http://example.com/1", "http://example.com/2"]
    assert all(n.source_id == 1 for n in result)


def test_parse_news_sync(monkeypatch):
    monkeypatch.setattr(feedparser_stub, "parse", lambda url: mock_parsed_feed, raising=False)
    result = parse_news_sync(2, "dummy")

    assert len(result) == 2
    assert all(isinstance(item, NewsCreate) for item in result)
    assert [n.title for n in result] == ["Item 1", "Item 2"]
    assert [n.url for n in result] == ["http://example.com/1", "http://example.com/2"]
    assert all(n.source_id == 2 for n in result)
