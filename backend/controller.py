import persistence
import time
import classifyAndSort
import threading
from models.feed import Source, Story

allStories = []

def addSource(url, name):
    s = Source(-1, url, name)
    persistence.addSource(s)
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
    allStories = []
    threadsUsed = []
    for idx, s in enumerate(persistence.sourceList):
        t = threading.Thread(target=fetchStories, args=[s])
        t.start()
        threadsUsed.append(t)
    threadsLeft = len(threadsUsed)
    for t in threadsUsed:
        t.join()
        threadsLeft -= 1
        print(f"{threadsLeft} threads left")

def fetchStories(s: Source):
    print(f"Fetching {s.name} in thread {threading.get_ident()}")
    stories = s.fetch()
    allStories.extend(stories)

def categoryRank(category):
    totalRank = 0
    for s in category[1]:
        totalRank += s.rank
    return totalRank


def getCategorizedStories():
    categories = list(classifyAndSort.classifyStories(allStories))
    # Sort by total story rank to capture number of stories, recency, and coherence of category
    categories.sort(key=categoryRank, reverse=True)
    return categories

def getCategoryLabels(categories: list):
    labels = []
    for c in categories:
        labels.append(classifyAndSort.generateCategoryName(c[1]))
    return labels