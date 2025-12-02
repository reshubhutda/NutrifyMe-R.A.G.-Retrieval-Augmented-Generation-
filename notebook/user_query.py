from sentence_transformers import SentenceTransformer

# Load embedding model 
_embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_query(query: str):
    """
    Takes a user query and returns a vector embedding.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")

    embedding = _embedder.encode(query)
    return embedding


def process_user_query(user_input: str):
    """
    Wrapper function:
    - cleans input
    - embeds it
    - returns both raw text + embedding
    """
    cleaned = user_input.strip()
    embedding = embed_query(cleaned)

    return {
        "query": cleaned,
        "embedding": embedding
    }
