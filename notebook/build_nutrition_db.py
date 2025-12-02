# build_nutrition_db.py

import chromadb
import pandas as pd
import numpy as np

CHROMA_PATH = "./chroma_data"


# TEXT BUILDER

def build_nutrition_text(row):
    return " ".join([
        row.get("FOOD_NAME", ""),
        row.get("ALTERNATE_NAMES", ""),
        row.get("LABELS", ""),
        row.get("INGREDIENTS", ""),
        row.get("INGREDIENT_ANALYSIS", ""),
        row.get("SERVING_VALUE", ""),
        row.get("SERVING_UNIT", ""),
        row.get("QUANTITY_VALUE", ""),
        row.get("QUANTITY_UNIT", ""),
        row.get("NUTRITION_SUMMARY", "")
    ])

# FUNCTION

def build_nutrition_collection():

    print("\n=== Building nutrition_db in chroma_data ===\n")

    # Load your processed nutrition dataset
    df = pd.read_csv("data/Processed_Nutrition.csv", dtype=str).fillna("Not Available")
    embeddings = np.load("data/nutrition_embeddings.npy")
    row_ids = np.load("data/nutrition_row_ids.npy").astype(int)

    print(f"Loaded {len(df)} rows")
    print(f"Loaded {len(embeddings)} embeddings")
    print(f"Loaded {len(row_ids)} row ids")

    # Connect to chroma_data
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Create or load nutrition_db
    collection = client.get_or_create_collection(
        name="nutrition_db",
        embedding_function=None  # using your precomputed embeddings
    )

    # Build texts + ids
    texts = []
    ids = []
    for rid in row_ids:
        row = df.iloc[rid]
        text = build_nutrition_text(row)
        texts.append(text)
        ids.append(str(rid))

    print(f"Built {len(texts)} nutrition text documents")


    batch_size = 5000
    total = len(texts)
    print("Storing in batches...")

    # for i in range(0, total, batch_size):
    #     end = min(i + batch_size, total)
    #     batch_docs = texts[i:end]
    #     batch_emb = embeddings[i:end].tolist()
    #     batch_ids = ids[i:end]

    #     try:
    #         collection.add(
    #             embeddings=batch_emb,
    #             documents=batch_docs,
    #             ids=batch_ids
    #         )
    #         print(f" Added batch {i} → {end} to nutrition_db")
    #     except Exception as e:
    #         print(f" ERROR batch {i}-{end}: {e}")
    #         break
    for i in range(0, total, batch_size):
        end = min(i + batch_size, total)
        batch_docs = texts[i:end]
        batch_emb = embeddings[i:end].tolist()
        batch_ids = ids[i:end]

        # metadata for this batch
        batch_meta = df.iloc[i:end].to_dict(orient="records")

        try:
            collection.add(
                embeddings=batch_emb,
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_meta
            )
            print(f" Added batch {i} → {end} to nutrition_db")
        except Exception as e:
            print(f" ERROR batch {i}-{end}: {e}")
            break

    print("\n=== nutrition_db successfully stored in chroma_data ===\n")
