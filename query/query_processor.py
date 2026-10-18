import re


def preprocess_query(query: str) -> str:

    query = query.lower()

    # Remove extra spaces
    query = re.sub(r"\s+", " ", query)

    # Remove punctuation
    query = re.sub(r"[^\w\s]", "", query)

    return query.strip()


if __name__ == "__main__":

    test_query = "Hey!! Can you tell me What is SETT???"
    processed = preprocess_query(test_query)

    print("Original Query:")
    print(test_query)

    print("\nProcessed Query:")
    print(processed)