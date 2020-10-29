import feedparser
import delorean
from dateutil import parser 
from datetime import datetime, timezone 

class Feed():
    def __init__(self, link):
        """Creates feed object with all of the latest things."""
        self.updated_feed =[]
        feed = feedparser.parse(link)
        for item in feed['items']:
            date_of = parser.parse(item['published'])
            time_difference = datetime.now(timezone.utc) - date_of 
            time_difference_hours = (time_difference.days * 24) + time_difference.seconds//3600
            if time_difference_hours < 10:
                self.updated_feed.append(item)
        self.author = feed['feed']['title']

