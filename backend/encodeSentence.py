from sentence_transformers import SentenceTransformer
import numpy as np
from scipy import stats

model = SentenceTransformer("all-MiniLM-L6-v2")

def sentenceToEmbedding(sentence: str) -> list:
    return model.encode(sentence)

def findClosestCategory(sentences: list[str]) -> str:
    with open("./categories.txt") as f:
        CATEGORIES = []
        for l in f:
            line = l.rstrip()
            if len(line) > 0 and line[0] != "#":
                CATEGORIES.append(line)
        if len(sentences) == 0:
            return "Empty category"
        categoryEmbeddings = model.encode(CATEGORIES)
        # Use only first few sentences to avoid excess strain
        sentenceEmbeddings = model.encode(sentences[0:5])
        similarities = model.similarity(sentenceEmbeddings, categoryEmbeddings)
        maxSimilarities = np.argmax(similarities, axis=1)
        mostCommonCategoryIdx = stats.mode(maxSimilarities).mode
        return CATEGORIES[mostCommonCategoryIdx]

def main():
    while True:
        toEmbed = input("Enter a sentence to embed\n")
        print(sentenceToEmbedding(toEmbed))

if __name__ == "__main__":
    main()