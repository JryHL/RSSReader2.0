import math
import encodeSentence
from models.feed import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

INERTIA_CHANGE_THRESHOLD = 0.95
INERTIA_FAILURE_TOLERANCE = 2

def generateCategoryName(stories: list[Story]):
    sentences = []
    for s in stories:
        sentences.append(f"{s.title} {s.summary}")
    return encodeSentence.findClosestCategory(sentences, stories)

def classifyStories(stories: list[Story]):
    if len(stories) == 0:
        return [(-1, [])]
    embeddings = []
    for s in stories:
        embedding = encodeSentence.sentenceToEmbedding(f"{s.title} {s.summary}")
        embeddings.append(embedding)
    
    pca = PCA(n_components=8)
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
