import math
import encodeSentence
from models.feed import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def generateCategoryName(stories: list[Story]):
    sentences = []
    for s in stories:
        sentences.append(s.title)
    return encodeSentence.findClosestCategory(sentences)

def classifyStories(stories: list[Story]):
    if len(stories) == 0:
        return [(-1, [])]
    embeddings = []
    for s in stories:
        embedding = encodeSentence.sentenceToEmbedding(f"{s.title} {s.summary}")
        embeddings.append(embedding)
    
    pca = PCA(n_components=5)
    reduced_embeddings = pca.fit_transform(embeddings)
    kmeans = KMeans(n_clusters=max(math.floor(len(reduced_embeddings)/5), 1))
    labels = kmeans.fit(reduced_embeddings).labels_

    categories = {}
    for story, label in zip(stories, labels):
        if label in categories:
            categories[label].append(story)
        else:
            categories[label] = [story]
    return categories.items()