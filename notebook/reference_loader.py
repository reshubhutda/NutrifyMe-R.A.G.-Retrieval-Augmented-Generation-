# reference_loader.py

import chromadb

CHROMA_PATH = "./chroma_data"
client = chromadb.PersistentClient(path=CHROMA_PATH)

def load_reference_ranges():
    """
    Loads ALL reference range metadata (around 35 rows).
    Used by LLM for lab test interpretation.
    """
    try:
        col = client.get_collection("ref_range_db")
    except:
        print("[ERROR] reference_db not found in Chroma.")
        return []

    res = col.get(include=["metadatas", "embeddings"])
    metadata = res.get("metadatas", [])
    embeddings = res.get("embeddings", [])
    
    return metadata, embeddings

# # STEP 6 — Load reference ranges
# if __name__ == "__main__":
#     reference_ranges = load_reference_ranges()
#     print(f"[INFO] Loaded {len(reference_ranges)} reference range entries.")
