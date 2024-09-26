import math
import encodeSentence
from models.feed import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np
from scipy import stats

INERTIA_CHANGE_THRESHOLD = 0.90
INERTIA_FAILURE_TOLERANCE = 2
PREEXISTING_CATEGORY_PREFERENCE = 1.7
SIMILARITY_RANKING_EFFECT = 50

nltk.download("stopwords")
nltk.download("punkt_tab")
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update([",", ".", "!", "-", "—", "?", ";", "'", "\""])

def findClosestCategory(stories: list[Story]) -> str:
    model = encodeSentence.model
    with open("./categories.txt") as f:
        
        STORIES_TO_CONSIDER = 5
        PREEXISTING_CATEGORIES = set()
        DYNAMIC_CATEGORIES = set()
        for l in f:
            line = l.rstrip()
            if len(line) > 0 and line[0] != "#":
                PREEXISTING_CATEGORIES.add(line)

        if len(stories) == 0:
            return "Empty category"
        sentences = []
        for s in stories:
            sentences.append(s.title)
        sentencesJoined = " ".join(sentences)
        
        # In addition to default categories, add custom categories based on words in sentences
        # Tokenize
        tokenized_sentences = word_tokenize(sentencesJoined.upper())
        # Remove stopwords
        filtered_tokens = [w for w in tokenized_sentences if not w.lower() in STOPWORDS]
        # Find most common words as potential categories
        frequent_words = Counter(filtered_tokens).most_common(10)
        for w in frequent_words:
            DYNAMIC_CATEGORIES.add(w[0])


        # Turn categories into encodings
        preexistingCategoryList = list(PREEXISTING_CATEGORIES)
        dynamicCategoryList = list(DYNAMIC_CATEGORIES)
        preexistingCategoriesEmbeddings = model.encode(preexistingCategoryList)
        dynamicCategoriesEmbeddings = model.encode(dynamicCategoryList)
        
        
        # Get category similarities for sentence, category combinations among first few sentences
        # sentenceEmbeddings = model.encode(sentences[0:STORIES_TO_CONSIDER])
        sentenceEmbeddings = []
        for s in stories[0:STORIES_TO_CONSIDER]:
            sentenceEmbeddings.append(s.embedding)
        # Find best preexisting and dynamic categories
        preexistingCategorySimilarities = model.similarity(sentenceEmbeddings, preexistingCategoriesEmbeddings).numpy()
        preexistingSimilaritySums = np.sum(preexistingCategorySimilarities, axis=0)
        mostCommonPreexistingCategoryIdx = np.argmax(preexistingSimilaritySums)

        dynamicCategorySimilarities = model.similarity(sentenceEmbeddings, dynamicCategoriesEmbeddings).numpy()
        dynamicSimilaritySums = np.sum(dynamicCategorySimilarities, axis=0)
        mostCommonDynamicCategoryIdx = np.argmax(dynamicSimilaritySums)

        pCatMax = preexistingSimilaritySums[mostCommonPreexistingCategoryIdx]
        dCatMax = dynamicSimilaritySums[mostCommonDynamicCategoryIdx]

        
        similaritiesToUse = None
        category_label = ""
        catMaxIdx = -1
        if pCatMax * PREEXISTING_CATEGORY_PREFERENCE > dCatMax:
            category_label = preexistingCategoryList[mostCommonPreexistingCategoryIdx]
            similaritiesToUse = preexistingCategorySimilarities
            catMaxIdx = mostCommonPreexistingCategoryIdx
        else:
            category_label = dynamicCategoryList[mostCommonDynamicCategoryIdx]
            similaritiesToUse = dynamicCategorySimilarities
            catMaxIdx = mostCommonDynamicCategoryIdx
        
        # Promote stories that are more related to the category
        for idx, s in enumerate(stories[0:STORIES_TO_CONSIDER]):
            s.rank = s.rank + (similaritiesToUse[idx][catMaxIdx] * SIMILARITY_RANKING_EFFECT)
        return category_label


def generateCategoryName(stories: list[Story]):
    return findClosestCategory(stories)

def classifyStories(stories: list[Story]):
    if len(stories) == 0:
        return []
    embeddings = []
    for s in stories:
        embeddings.append(s.embedding)
    
    pca = PCA(n_components=min(8, len(stories)))
    reduced_embeddings = pca.fit_transform(embeddings)
    # reduced_embeddings = embeddings
    kmeans = None
    
    # Approximation of elbow method
    # Detect when change from last inertia is below certain threshold
    lastInertia = -1
    numFails = 0
    for i in range(1, max(math.ceil(len(reduced_embeddings)/2), 2)): 
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(reduced_embeddings)
        print(kmeans.inertia_)
        if i > 1:
            if kmeans.inertia_ > lastInertia * INERTIA_CHANGE_THRESHOLD:
                numFails += 1
                print(f"Failure to reduce inertia below threshold #{numFails}")
            else:
                if numFails > 0:
                    numFails = 0
                    print(f"Number of failure to reduce inertia reset")
            # Exit on repeat failure to decrease inertia
            if numFails >= INERTIA_FAILURE_TOLERANCE:
                break
            
        lastInertia = kmeans.inertia_
    #kmeans = KMeans(n_clusters=max(math.floor(len(reduced_embeddings)/10), 1), init="k-means++", algorithm="elkan", n_init=2)
    labels = kmeans.labels_

    categories = {}
    for story, label in zip(stories, labels):
        if label in categories:
            categories[label].append(story)
        else:
            categories[label] = [story]

    
    return categories.items()
