import feedparser
from bs4 import BeautifulSoup
import datetime
import time

FETCH_INTERVAL_MINUTES = 10
RECENCY_WEIGHT = 1
MAX_ENTRIES_PER_SOURCE = 10
lastStoryID = 0

class Story:
    
    @staticmethod
    def selfRank(timetuple):
        rank = 0
        
        # Get number of seconds since publishing
        pubTime = time.mktime(timetuple)
        currTime = time.time()
        timeDiff = max(currTime - pubTime, 0)
        # Convert to number of hours
        hoursDiff = timeDiff / 3600
        rank -= hoursDiff * RECENCY_WEIGHT
        
        return rank
    
    def __init__(self, id, url, title, timetuple, summary, source):
        self.id = id
        self.url = url
        self.title = title
        self.summary = summary
       
        self.timetuple = timetuple
        self.date = time.strftime("%a. %b. %-d, %Y at %I:%M %p", timetuple)
        self.rank = self.selfRank(timetuple)
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
            print(f"{self.name} was not fetched because it was last fetched {(currTime - self.lastFetchTime) / 60} minutes ago")
            return self.stories
        
        
        self.stories = []
        feed = feedparser.parse(self.url)
        self.lastFetchTime = currTime
        if hasattr(feed, "entries"):
            for e in feed.entries[0:MAX_ENTRIES_PER_SOURCE]:
                lastStoryID += 1
                id = lastStoryID
                title = getattr(e, "title", "")
                url = getattr(e, "link", "")
                summaryHTML = getattr(e, "description", "")
                soup = BeautifulSoup(summaryHTML, "html.parser")
                summary = soup.text
                timetuple = getattr(e, "published_parsed", datetime.datetime.today().timetuple())
                s = Story(id, url, title, timetuple, summary, self)
                self.stories.append(s)
        if len(self.stories) == 0:
            print(f"No stories found for {self.name}!")
        return self.stories
                