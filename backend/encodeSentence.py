from sentence_transformers import SentenceTransformer
import numpy as np
from scipy import stats
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from models.feed import *

nltk.download("stopwords")
nltk.download("punkt_tab")
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update([",", ".", "!", "-", "—", "?", ";", "'", "\""])
model = SentenceTransformer("all-MiniLM-L6-v2")
PREEXISTING_CATEGORY_PREFERENCE = 1.7
SIMILARITY_RANKING_EFFECT = 50

def sentenceToEmbedding(sentence: str) -> list:
    return model.encode(sentence)

def findClosestCategory(sentences: list[str], stories: list[Story]) -> str:
    with open("./categories.txt") as f:
        
        STORIES_TO_CONSIDER = 5
        PREEXISTING_CATEGORIES = set()
        DYNAMIC_CATEGORIES = set()
        for l in f:
            line = l.rstrip()
            if len(line) > 0 and line[0] != "#":
                PREEXISTING_CATEGORIES.add(line)
        if len(sentences) == 0:
            return "Empty category"
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
        sentenceEmbeddings = model.encode(sentences[0:STORIES_TO_CONSIDER])

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

def main():
    while True:
        toEmbed = input("Enter a sentence to embed\n")
        print(sentenceToEmbedding(toEmbed))

if __name__ == "__main__":
    main()