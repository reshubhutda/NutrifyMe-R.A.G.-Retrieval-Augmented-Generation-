# nutrition_retriever.py

import chromadb
from user_query import embed_query 

CHROMA_PATH = "./chroma_data"
client = chromadb.PersistentClient(path=CHROMA_PATH)

def query_nutrition(query_embedding, top_k: int = 5):
    """
    Clean retriever ONLY for nutrition_db.
    Assumes 'food_name' is already a clean string like 'coca cola', 'banana', etc.
    """

    try:
        col = client.get_collection("nutrition_db")
    except:
        print("[ERROR] nutrition_db not found in Chroma.")
        return {"documents": [], "metadata": [], "embeddings": []}

    # 1. Embed the food name
    #query_embedding = embed_query(food_name)

    # 2. Query the nutrition collection
    results = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "embeddings"]
    )

    # Guarantee a stable dictionary structure
    return {
        "documents": results.get("documents", [[]])[0],
        "metadata":  results.get("metadatas", [[]])[0],
      #  "embeddings": results.get("embeddings", [[]])[0]
    }

# Invidividual File Testing code.

# if __name__ == "__main__":
#     # quick test
#     q = input("Enter food name: ")
#     out = query_nutrition(q, top_k=3)

#     print("\nTOP RESULTS:")
#     for i, doc in enumerate(out["documents"][0], start=1):
#         print(f"\n[{i}] {doc}")
#         print(out["metadatas"][0][i-1])
