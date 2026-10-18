from sentence_transformers import CrossEncoder
from query.hybrid_search import hybrid_search

# Load reranker model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, top_k=3):

    docs = hybrid_search(query)

    pairs = [
        (query, doc)
        for doc in docs
    ]

    scores = reranker.predict(pairs)

    ranked_results = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_results[:top_k]


if __name__ == "__main__":

    query = "What is SETT?"

    results = rerank(query)

    for i, (doc, score) in enumerate(results, start=1):

        print("\n" + "="*50)

        print(f"Rank {i}")

        print(f"Score : {score:.4f}")

        print(doc)