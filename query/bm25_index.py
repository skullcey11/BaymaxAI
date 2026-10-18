import sys
import os
import re

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from rank_bm25 import BM25Okapi
from indexing.load_doc import load_documents


documents = load_documents()

# Extract text only
corpus = [doc.page_content for doc in documents]

# Tokenize
tokenized_corpus = [
    tokenize(doc)
    for doc in corpus
]

bm25 = BM25Okapi(tokenized_corpus)


def bm25_search(query, top_k=3):

    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    ranked_docs = sorted(
        zip(corpus, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_docs[:top_k]


if __name__ == "__main__":

    results = bm25_search(
        "What is SETT?"
    )

    for i, (doc, score) in enumerate(results, start=1):

        print("=" * 50)
        print(f"Result {i}")
        print(f"Score: {score:.2f}")
        print(doc)