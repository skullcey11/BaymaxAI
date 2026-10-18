from query.reranker import rerank


def build_prompt(query):

    results = rerank(query)

    context = "\n\n".join(
        [doc for doc, score in results]
    )

    prompt = f"""
You are an expert and helpful assistant for the Petroleum and Explosives Safety Organisation (PESO).

You also know a lot about SETT and ANRS rules.

You are tasked with answering questions based on the provided context.

Answer ONLY using the provided context.

If the answer cannot be found in the context, say:

"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt


if __name__ == "__main__":

    prompt = build_prompt(
        "What is SETT?"
    )

    print(prompt)