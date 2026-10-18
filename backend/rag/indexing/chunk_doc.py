from langchain_text_splitters import RecursiveCharacterTextSplitter
from indexing.load_doc import load_documents


def chunk_documents():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"\nCreated {len(chunks)} chunks")

    return chunks


if __name__ == "__main__":

    chunks = chunk_documents()

    for i, chunk in enumerate(chunks):

        print("\n" + "=" * 50)
        print(f"Chunk {i+1}")
        print(f"Source: {chunk.metadata['source']}")
        print(chunk.page_content)