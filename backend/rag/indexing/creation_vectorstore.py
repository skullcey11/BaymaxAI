from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from indexing.chunk_doc import chunk_documents 


def create_vector_store():

    chunks = chunk_documents()

    print("\nLoading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating ChromaDB...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    print("\nVector store created successfully!")

    return vectorstore


if __name__ == "__main__":
    create_vector_store()