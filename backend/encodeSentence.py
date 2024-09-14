from sentence_transformers import SentenceTransformer
import numpy as np
from scipy import stats
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
nltk.download("punkt_tab")
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update([",", ".", "!", "-", "—", "?", ";", "'", "\""])
model = SentenceTransformer("all-MiniLM-L6-v2")

def sentenceToEmbedding(sentence: str) -> list:
    return model.encode(sentence)

def findClosestCategory(sentences: list[str]) -> str:
    with open("./categories.txt") as f:
        CATEGORIES = set()
        for l in f:
            line = l.rstrip()
            if len(line) > 0 and line[0] != "#":
                CATEGORIES.add(line)
        if len(sentences) == 0:
            return "Empty category"
        sentencesJoined = " ".join(sentences)
        
        # In addition to default categories, add custom categories based on words in sentences
        tokenized_sentences = word_tokenize(sentencesJoined.upper())
        # Remove stopwords
        filtered_tokens = [w for w in tokenized_sentences if not w.lower() in STOPWORDS]
        CATEGORIES.update(filtered_tokens)

        categoriesList = list(CATEGORIES)
        categoryEmbeddings = model.encode(categoriesList)
        
        # Find most similar category
        sentenceEmbeddings = model.encode(sentences[0:10])
        similarities = model.similarity(sentenceEmbeddings, categoryEmbeddings)
        # Get sum of similarity numbers over sentences for each category
        similiaritySums = np.sum(similarities.numpy(), axis=0)
        mostCommonCategoryIdx = np.argmax(similiaritySums)
        # maxSimilarities = np.argmax(similarities, axis=1)
        # mostCommonCategoryIdx = stats.mode(maxSimilarities).mode
        return categoriesList[mostCommonCategoryIdx]

def main():
    while True:
        toEmbed = input("Enter a sentence to embed\n")
        print(sentenceToEmbedding(toEmbed))

if __name__ == "__main__":
    main()