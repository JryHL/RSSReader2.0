import feedparser
from bs4 import BeautifulSoup
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
    def fetch(self):
        global lastStoryID
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
                