from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from query.bm25_index import bm25_search


# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Chroma DB
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)


def hybrid_search(query, k=3):

    # Vector search
    vector_docs = db.similarity_search(
        query,
        k=k
    )

    # BM25 search
    bm25_docs = bm25_search(
        query,
        top_k=k
    )

    # Combine and remove duplicates
    combined_docs = []

    seen = set()

    # Add vector results
    for doc in vector_docs:

        content = doc.page_content

        if content not in seen:

            combined_docs.append(content)

            seen.add(content)

    # Add BM25 results
    for doc, score in bm25_docs:

        if doc not in seen:

            combined_docs.append(doc)

            seen.add(doc)

    return combined_docs


if __name__ == "__main__":

    query = "What is SETT?"

    results = hybrid_search(query)

    print("\nQuery:", query)

    for i, doc in enumerate(results, 1):

        print("\n" + "="*50)

        print(f"Result {i}")

        print(doc)