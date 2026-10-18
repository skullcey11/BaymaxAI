from langchain_ollama import ChatOllama
from query.prompt_builder import build_prompt

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

while True:

    query = input("\nAsk a question: ")

    if query.lower().strip() == "exit":
        print("Goodbye!")
        break

    prompt = build_prompt(query)

    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)