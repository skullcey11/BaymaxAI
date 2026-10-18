from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

response = llm.invoke("What is PESO?")
print(response.content)