from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def sentenceToEmbedding(sentence: str) -> list:
    return model.encode(sentence)


def main():
    while True:
        toEmbed = input("Enter a sentence to embed\n")
        print(sentenceToEmbedding(toEmbed))

if __name__ == "__main__":
    main()