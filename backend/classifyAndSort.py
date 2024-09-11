import math
import encodeSentence
from models.feed import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def generateCategoryName(stories: list[Story]):
    sentences = []
    for s in stories:
        sentences.append(f"{s.title} {s.summary}")
    return encodeSentence.findClosestCategory(sentences)

def classifyStories(stories: list[Story]):
    if len(stories) == 0:
        return [(-1, [])]
    embeddings = []
    for s in stories:
        embedding = encodeSentence.sentenceToEmbedding(f"{s.title} {s.summary}")
        embeddings.append(embedding)
    
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)
    kmeans = None
    
    # Approximation of elbow method
    # Detect when change from last inertia is below certain threshold
    lastInertia = -1
    for i in range(1, len(reduced_embeddings)): 
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(reduced_embeddings)
        print(kmeans.inertia_)
        if i > 1:
            if kmeans.inertia_ > lastInertia * 0.95:
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
    
    # Rank stories
    for c in categories.values():
        c.sort(key=(lambda x: x.rank), reverse=True)
    
    return categories.items()