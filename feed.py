import feedparser
import delorean
from dateutil import parser
from datetime import datetime, timezone


class FeedItem():
    def __init__(self, author, rss_item):
        self.author = author
        self.rss_item = rss_item
        self.title = rss_item['title']
        self.link = rss_item['link']

class InvalidRSSError(Exception):
    pass 


class Feed():
    def __init__(self, link):
        try:
            """Creates feed object with all of the latest things."""
            self.updated_feed = []
            feed = feedparser.parse(link)
            self.author = feed['feed']['title']
            for item in feed['items']:
                date_of = parser.parse(item['published'])
                time_difference = datetime.now(timezone.utc) - date_of
                time_difference_hours = (
                    time_difference.days * 24) + time_difference.seconds//3600
                if time_difference_hours < 48:
                    self.updated_feed.append(FeedItem(self.author, item))
        except:
            raise InvalidRSSError()
