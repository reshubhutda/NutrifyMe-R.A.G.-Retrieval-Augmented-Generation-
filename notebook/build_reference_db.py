# build_reference_db.py

import chromadb
import pandas as pd
import numpy as np

CHROMA_PATH = "./chroma_data"  


# TEXT BUILDER

def build_reference_text(row):
    return (
        f"{row.get('TEST','')} {row.get('UNITS','')} "
        f"Adult Range: {row.get('Adult Range','')} "
        f"Adult Min: {row.get('Adult Min','')} Adult Max: {row.get('Adult Max','')} "
        f"Child Range: {row.get('Child Range','')} "
        f"Child Min: {row.get('Child Min','')} Child Max: {row.get('Child Max','')}"
    )

# MAIN FUNCTION

def build_reference_collection():

    print("\n=== Building ref_range_db in chroma_data ===\n")

    # Load processed reference range dataset
    df = pd.read_csv("data/Processed_Reference_Range.csv", dtype=str).fillna("Not Available")
    embeddings = np.load("data/reference_embeddings.npy")
    row_ids = np.load("data/reference_row_ids.npy").astype(int)

    print(f"Loaded {len(df)} rows")
    print(f"Loaded {len(embeddings)} embeddings")
    print(f"Loaded {len(row_ids)} row ids")

    # Connect to chroma_data
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Use retriever-compatible name
    collection = client.get_or_create_collection(
        name="ref_range_db",
        embedding_function=None  # precomputed embeddings
    )

    # Build texts + ids
    texts = []
    ids = []
    metadata_list = []
    # for rid in row_ids:
    #     row = df.iloc[rid]
    #     text = build_reference_text(row)
    #     texts.append(text)
    #     ids.append(str(rid))

    # print(f"Built {len(texts)} reference documents")

    # # Batch insertion
    # batch_size = 5000
    # total = len(texts)
    # print("Storing in batches...")

    # for i in range(0, total, batch_size):
    #     end = min(i + batch_size, total)

    #     try:
    #         collection.add(
    #             embeddings=embeddings[i:end].tolist(),
    #             documents=texts[i:end],
    #             ids=ids[i:end]
    #         )
    #         print(f"Added batch {i} → {end} to ref_range_db")
    #     except Exception as e:
    #         print(f"ERROR batch {i}-{end}: {e}")
    #         break

    # print("\n=== ref_range_db successfully stored in chroma_data ===\n")
    for rid in row_ids:
        row = df.iloc[rid]

        texts.append(build_reference_text(row))
        ids.append(str(rid))

        metadata = {
            "TEST": row["TEST"],
            "UNITS": row["UNITS"],
            "Adult Range": row["Adult Range"],
            "Child Range": row["Child Range"],
            "Adult Min": row["Adult Min"],
            "Adult Max": row["Adult Max"],
            "Child Min": row["Child Min"],
            "Child Max": row["Child Max"]
        }

        metadata_list.append(metadata)

    # batch insert
    batch_size = 5000
    total = len(texts)

    for i in range(0, total, batch_size):
        end = min(i + batch_size, total)

        collection.add(
            embeddings=embeddings[i:end].tolist(),
            documents=texts[i:end],
            ids=ids[i:end],
            metadatas=metadata_list[i:end]
        )

    print("\n=== ref_range_db updated with full metadata ===\n")