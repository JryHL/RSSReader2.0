import persistence
import time
import classifyAndSort
import threading
from models.feed import Source, Story
import random
import encodeSentence

# Number of stories per page
PAGE_SIZE = 50
SEARCH_QUERY_WEIGHT = 500
EXACT_WORDS_WEIGHT = 100000
SIMILARITY_THRESHOLD = 0.7
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
    allStories = [] # Note: Sources themselves keep cache of stories that is not cleared here
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
    # random.shuffle(allStories)
    
    # Sort stories by pre-categorization rank (time alone) 
    # So that latest stories are displayed first
    # When paging through stories
    # Stories are not resorted when their ranks are changed
    # later on based on their category label, so no effect on paging
    for s in allStories:
        s.rank = s.baseRank
    allStories.sort(key=lambda x: x.rank, reverse=True)

def fetchStories(s: Source):
    print(f"Fetching {s.name} in thread {threading.get_ident()}")
    stories = s.fetch()
    allStories.extend(stories)

def categoryRank(category):
    totalRank = 0
    for s in category[1]:
        totalRank += s.rank
    return totalRank

            
def getCategorizedStories(page, searchQuery):
    global allStories
    queryEmbed = None
    myStories = []
    if len(searchQuery):
        queryEmbed = encodeSentence.model.encode(searchQuery)
        if page == 0:
            for s in allStories:
                s.embedding = encodeSentence.sentenceToEmbedding(s.title)
                similarity = encodeSentence.model.similarity(s.embedding, queryEmbed).item()
                # Do not index 
                if similarity > SIMILARITY_THRESHOLD or (searchQuery in s.title) or (searchQuery in s.source.name) or (searchQuery in s.summary):
                    s.rank += similarity * SEARCH_QUERY_WEIGHT
                    if searchQuery in s.title:
                        s.rank += EXACT_WORDS_WEIGHT
                    myStories.append(s)
                else:
                    continue
            allStories = myStories
    storiesOnPage = allStories[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    # if no search query, embedding has already been obtained in previous stage
    if not len(searchQuery):
        for s in storiesOnPage:
            if type(s.embedding) == type(None):
                s.embedding = encodeSentence.sentenceToEmbedding(s.title)
    categories = list(classifyAndSort.classifyStories(storiesOnPage))
    # Sort by total story rank to capture number of stories, recency, and coherence of category
    categories.sort(key=categoryRank, reverse=True)
    return categories

def getCategoryLabels(categories: list):
    labels = []
    for c in categories:
        labels.append(classifyAndSort.generateCategoryName(c[1]))
    return labels