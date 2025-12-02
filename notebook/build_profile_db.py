# build_profile_db.py

import chromadb
from chromadb.utils import embedding_functions

from profile_summary import build_user_summary_embedding, build_user_summary_text
from user_db import get_user_profile, get_user_conditions, get_user_medications

# Path to your Chroma DB folder
CHROMA_PATH = "./chroma_data"

def build_profile_collection(user_id: int):
    # 1) Create persistent Chroma client
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # 2) Create or load collection
    try:
        collection = client.get_collection("profile_db")
    except:
        collection = client.create_collection("profile_db")

    # 3) Build summary & embedding
    prof = get_user_profile(user_id)
    conds = get_user_conditions(user_id)
    meds = get_user_medications(user_id)


    metadata = {
    "user_id": int(user_id),
    "name": str(prof.get("name")),
    "age": int(prof.get("age")) if prof.get("age") else None,
    "gender": str(prof.get("gender")),
    "ethnicity": str(prof.get("ethnicity")),
    "marital_status": str(prof.get("marital_status")),
    "height_cm": float(prof.get("height_cm")) if prof.get("height_cm") else None,
    "weight_kg": float(prof.get("weight_kg")) if prof.get("weight_kg") else None,
    "bmi": float(prof.get("bmi")) if prof.get("bmi") else None,
    "conditions": ", ".join(conds) if conds else "none",
    "medications": ", ".join(meds) if meds else "none"
    }


    summary_text, embedding = build_user_summary_embedding(user_id)

    # 4) Insert into collection
    collection.add(
        ids=[str(user_id)],        # ID must be string
        documents=[summary_text],  
        embeddings=[embedding.tolist()],
        metadatas=[metadata]
    )

    print(f"\nUser {user_id} summary stored in profile_db")
    return metadata
