from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)


query = "What is SETT?"

results = db.similarity_search(
    query,
    k=3
)

print(f"\nQuery: {query}\n")

for i, doc in enumerate(results, start=1):

    print("=" * 50)
    print(f"Result {i}")
    print(doc.page_content)