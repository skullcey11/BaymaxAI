from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader


def load_documents():

    loader = DirectoryLoader(
        path="docs",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    for doc in docs:
        print("\n===================")
        print(doc.metadata["source"])
        print(doc.page_content[:100])