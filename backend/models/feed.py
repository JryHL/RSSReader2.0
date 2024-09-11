import feedparser
from bs4 import BeautifulSoup
import time

FETCH_INTERVAL_MINUTES = 10
lastStoryID = 0

class Story:
    def __init__(self, id, url, title, date, summary, source):
        self.id = id
        self.url = url
        self.title = title
        self.summary = summary
        self.date = date
        self.rank = 0
        self.source = source


class Source:
    def __init__(self, id, url, name):
        self.id = id
        self.url = url
        self.name = name
        self.stories = []
        self.lastFetchTime = 0
    def fetch(self):
        global lastStoryID
        currTime = time.time()
        if (currTime - self.lastFetchTime < FETCH_INTERVAL_MINUTES * 60):
            print(f"{self.name} was not fetched because it last fetched {(currTime - self.lastFetchTime) / 60} minutes ago")
            return self.stories
        self.lastFetchTime = currTime
        
        self.stories = []
        feed = feedparser.parse(self.url)
        if hasattr(feed, "entries"):
            for e in feed.entries:
                lastStoryID += 1
                id = lastStoryID
                title = getattr(e, "title", "")
                url = getattr(e, "link", "")
                summaryHTML = getattr(e, "description", "")
                soup = BeautifulSoup(summaryHTML, "html.parser")
                summary = soup.text
                date = getattr(e, "published", "")
                s = Story(lastStoryID, url, title, date, summary, self)
                self.stories.append(s)
        return self.stories
                