import persistence
import time
import classifyAndSort
from models.feed import Source, Story

allStories = []
lastFetchTime = 0
MINUTES_BETWEEN_FETCH = 10

def addSource(url, name):
    global lastFetchTime
    s = Source(-1, url, name)
    persistence.addSource(s)
    fetchStories(s)
    return s

def delSource(id):
    global allStories
    mySource = None
    for s in persistence.sourceList:
        if s.id == id:
            mySource = s
            break
    if mySource is not None:
        for st in allStories:
            if st.source == mySource:
                allStories.remove(st)
        persistence.delSource(mySource)

def getAllStories():
    global allStories
    global lastFetchTime
    currentTime = time.time()
    if currentTime - lastFetchTime < MINUTES_BETWEEN_FETCH * 60:
        print(f"Time difference {currentTime - lastFetchTime} seconds, did not refetch")
        return
    lastFetchTime = currentTime

    allStories = []
    for idx, s in enumerate(persistence.sourceList):
        print(f"Fetching {s.name} ({idx + 1}/{len(persistence.sourceList)})")
        fetchStories(s)

def fetchStories(s: Source):
    stories = s.fetch()
    allStories.extend(stories)

def getCategorizedStories():
    categories = classifyAndSort.classifyStories(allStories)
    return categories

def getCategoryLabels(categories: list):
    labels = []
    for c in categories:
        labels.append(classifyAndSort.generateCategoryName(c[1]))
    return labels