from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from query.query_processor import preprocess_query

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Chroma DB
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# Ollama
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

query = "Hey!! Can you tell me what SETT is???"

processed_query = preprocess_query(query)

print("Processed Query:")
print(processed_query)

# Retrieve relevant docs
docs = db.similarity_search(processed_query, k=3)

# Build context
context = "\n\n".join(
    [doc.page_content for doc in docs]
)

# Prompt
prompt = f"""
You are a helpful assistant for the Petroleum and Explosives Safety Organisation (PESO).

Use the provided context to answer the user's question.

If the answer is present in the context, provide a complete explanation.

If the answer is not present in the context, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

response = llm.invoke(prompt)

print("\nQUESTION:")
print(query)

print("\nANSWER:")
print(response.content)