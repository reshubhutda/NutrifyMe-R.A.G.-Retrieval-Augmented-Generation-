# build_health_db.py

import chromadb
import pandas as pd
import numpy as np

CHROMA_PATH = "./chroma_data"   

# TEXT BUILDER

def build_health_text(row):
    return (
        f"Gender {row.get('GENDER','')}, "
        f"Age {row.get('AGE','')}, "
        f"Race {row.get('RACE','')}, "
        f"Birth Country {row.get('BIRTH_COUNTRY','')}, "
        f"Marital Status {row.get('Marital Status','')}, "
        f"BMI Category {row.get('BMI Category','')}"
    )


# FUNCTION

def build_health_collection():

    print("\n=== Building nhanes_db in chroma_data ===\n")

    # Load NHANES-like processed health dataset
    df = pd.read_csv("data/Processed_Health.csv", dtype=str).fillna("Not Available")
    embeddings = np.load("data/health_embeddings.npy")
    row_ids = np.load("data/health_row_ids.npy").astype(int)

    print(f"Loaded {len(df)} rows")
    print(f"Loaded {len(embeddings)} embeddings")
    print(f"Loaded {len(row_ids)} row ids")

    # Connect to chroma_data
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Use retriever-compatible name
    collection = client.get_or_create_collection(
        name="nhanes_db",
        embedding_function=None
    )

    # Build text + ids + metadata
    texts = []
    ids = []
    metadata_list = []

    for rid in row_ids:
        row = df.iloc[rid]
        text = build_health_text(row)
        texts.append(text)
        ids.append(str(rid))
        metadata = {
            col: row[col]
            for col in df.columns  # everything goes in metadata
            if col not in ["GENDER", "AGE", "RACE", "BIRTH_COUNTRY", "Marital Status", "BMI Category"]
        }
        # Add semantic columns ALSO to metadata
        metadata["GENDER"] = row["GENDER"]
        metadata["AGE"] = row["AGE"]
        metadata["RACE"] = row["RACE"]
        metadata["BIRTH_COUNTRY"] = row["BIRTH_COUNTRY"]
        metadata["Marital_Status"] = row["Marital Status"]
        metadata["BMI_Category"] = row["BMI Category"]

        metadata_list.append(metadata)

    print(f"Built {len(texts)} health documents")


    batch_size = 5000  
    total = len(texts)
    print("Storing in batches...")

    for i in range(0, total, batch_size):
        end = min(i + batch_size, total)

        try:
            collection.add(
                embeddings=embeddings[i:end].tolist(),
                documents=texts[i:end],
                ids=ids[i:end],
                metadatas=metadata_list[i:end]
            )
            print(f"Added batch {i} → {end} to nhanes_db")
        except Exception as e:
            print(f"ERROR batch {i}-{end}: {e}")
            break

    print("\n=== nhanes_db successfully stored in chroma_data ===\n")
