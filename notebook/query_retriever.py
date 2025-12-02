## TESTING CODE ##

# retrievers.py
import chromadb
from user_query import embed_query

# Setup Chroma client & collections (EDIT for your setup)
client = chromadb.PersistentClient(path="./chroma_data")

# Ensure collections are created (or fetched if they already exist)
collections = {}

# Try fetching each collection, create if not found
try:
    collections["profile_db"] = client.get_collection("profile_db")
except Exception as e:  # Use a generic exception handler
    print(f"[INFO] Collection 'profile_db' not found. Creating a new collection. Error: {e}")
    collections["profile_db"] = client.create_collection("profile_db")
    print("[INFO] Created 'profile_db' collection.")

try:
    collections["ref_range_db"] = client.get_collection("ref_range_db")
except Exception as e:
    print(f"[INFO] Collection 'ref_range_db' not found. Creating a new collection. Error: {e}")
    collections["ref_range_db"] = client.create_collection("ref_range_db")
    print("[INFO] Created 'ref_range_db' collection.")

try:
    collections["nutrition_db"] = client.get_collection("nutrition_db")
except Exception as e:
    print(f"[INFO] Collection 'nutrition_db' not found. Creating a new collection. Error: {e}")
    collections["nutrition_db"] = client.create_collection("nutrition_db")
    print("[INFO] Created 'nutrition_db' collection.")

try:
    collections["nhanes_db"] = client.get_collection("nhanes_db")
except Exception as e:
    print(f"[INFO] Collection 'nhanes_db' not found. Creating a new collection. Error: {e}")
    collections["nhanes_db"] = client.create_collection("nhanes_db")    
    print("[INFO] Created 'nhanes_db' collection.")

# Now collections are guaranteed to exist, you can proceed with querying

def query_single_db(db_name: str, query_text: str, user_id: int, top_k: int = 5):
    """
    Query a single collection in the Chroma DB for relevant documents.
    Returns the top-k most relevant documents, filtered by user_id for profile_db.
    """
    collection = collections.get(db_name)
    
    if not collection:
        raise ValueError(f"Collection '{db_name}' not found in the Chroma client.")

    if db_name == "profile_db":
        print("[DEBUG] profile_db: returning EXACT user_id document")

        results = collection.get(
            where={"user_id": user_id},     # filter by metadata
            include=["documents", "metadatas"]
        )

        # Ensure always 1 doc or empty
        results = {
            "documents": [results.get("documents", [])],
            "metadatas": [results.get("metadatas", [])]
        }
        return results

    query_embedding = embed_query(query_text)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

    

def query_multiple_dbs(user_query: str, user_id: int, top_k: int = 3):
    """
    Query multiple databases (profile_db, nutrition_db, etc.) and return results.
    """
    query_results = {}

    for db_name in collections:
        print(f"[INFO] Querying {db_name}...")
        results = query_single_db(db_name, user_query, user_id, top_k)
        query_results[db_name] = results

    return query_results

