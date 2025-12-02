# TESTING CODE FOR ALL THE DBS AT THE SAME TIME

import chromadb
import pandas as pd
import numpy as np

print("\n=== Starting Chroma Store for ALL datasets ===\n")

# TEXT BUILDERS (exactly matching your embedding logic)


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

def build_reference_text(row):
    return (
        f"{row.get('TEST','')} {row.get('UNITS','')} "
        f"Adult Range: {row.get('Adult Range','')} "
        f"Adult Min: {row.get('Adult Min','')} Adult Max: {row.get('Adult Max','')} "
        f"Child Range: {row.get('Child Range','')} "
        f"Child Min: {row.get('Child Min','')} Child Max: {row.get('Child Max','')}"
    )

def build_health_text(row):
    return (
        f"Gender {row.get('GENDER','')}, "
        f"Age {row.get('AGE','')}, "
        f"Race {row.get('RACE','')}, "
        f"Birth Country {row.get('BIRTH_COUNTRY','')}, "
        f"Marital Status {row.get('Marital_Status','')}, "
        f"BMI Category {row.get('BMI_Category','')}"
    )


# DATASET CONFIG

datasets = {
    "nutrition": {
        "csv": "data/Processed_Nutrition.csv",
        "emb": "data/nutrition_embeddings.npy",
        "row": "data/nutrition_row_ids.npy",
        "builder": build_nutrition_text
    },
    "health": {
        "csv": "data/Processed_Health.csv",
        "emb": "data/health_embeddings.npy",
        "row": "data/health_row_ids.npy",
        "builder": build_health_text
    },
    "reference": {
        "csv": "data/Processed_Reference_Range.csv",
        "emb": "data/reference_embeddings.npy",
        "row": "data/reference_row_ids.npy",
        "builder": build_reference_text
    }
}


# INITIALIZE CHROMA

client = chromadb.PersistentClient(path="chroma_db")


# MAIN LOOP

for name, cfg in datasets.items():

    print(f"\n=== Processing dataset: {name.upper()} ===")

    # Load data
    df = pd.read_csv(cfg["csv"], dtype=str).fillna("Not Available")
    embeddings = np.load(cfg["emb"])
    row_ids = np.load(cfg["row"]).astype(int)
    builder = cfg["builder"]

    print(f"Loaded {len(df)} rows from CSV")
    print(f"Loaded {len(embeddings)} embeddings")
    print(f"Loaded {len(row_ids)} row indices")

    # Create or get collection
    collection = client.get_or_create_collection(
        name=name,
        embedding_function=None  # embeddings already computed
    )

    # Build texts + IDs
    texts = []
    ids = []
    for rid in row_ids:
        row = df.iloc[rid]
        text = builder(row)
        texts.append(text)
        ids.append(str(rid))

    print(f"Built {len(texts)} text chunks for storage")

    
    batch_size = 5000
    total = len(texts)

    print(f"Storing in batches of {batch_size}...")

    for i in range(0, total, batch_size):
        end = min(i + batch_size, total)
        try:
            collection.add(
                embeddings=embeddings[i:end].tolist(),
                documents=texts[i:end],
                ids=ids[i:end]
            )
            print(f"✅ Added batch {i} → {end} for collection '{name}'")
        except Exception as e:
            print(f"❌ ERROR in batch {i} → {end}: {e}")
            break

    print(f"COMPLETED storing dataset: {name}")

print("\nALL datasets successfully stored into ChromaDB\n")
