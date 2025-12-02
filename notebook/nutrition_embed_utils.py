# TESTING CODE EXECUTE BY Nutrtion_Embed.py


import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

print("Script started")

def embed_csv(
    csv_path,
    save_emb_path,
    save_ids_path,
    batch_size=64,
    model_name="sentence-transformers/all-MiniLM-L6-v2",
):
    df = pd.read_csv(csv_path, dtype=str).fillna("Not Available")
    model = SentenceTransformer(model_name)

    all_embeddings = []
    all_ids = []
    batch_texts = []
    batch_ids = []

    def build_text(row):
        return (
            f"{row['FOOD_NAME']} "
            f"{row['ALTERNATE_NAMES']} "
            f"{row['LABELS']} "
            f"{row['INGREDIENTS']} "
            f"{row['INGREDIENT_ANALYSIS']} "
            f"{row['SERVING_VALUE']} "
            f"{row['SERVING_UNIT']} "
            f"{row['QUANTITY_VALUE']} "
            f"{row['QUANTITY_UNIT']} "
            f"{row['NUTRITION_SUMMARY']}"
        )

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        text = build_text(row)
        batch_texts.append(text)
        batch_ids.append(idx)

        if len(batch_texts) == batch_size:
            embs = model.encode(batch_texts, batch_size=batch_size, show_progress_bar=False)
            all_embeddings.append(embs)
            all_ids.extend(batch_ids)
            batch_texts = []
            batch_ids = []

    if batch_texts:
        embs = model.encode(batch_texts, batch_size=batch_size, show_progress_bar=False)
        all_embeddings.append(embs)
        all_ids.extend(batch_ids)

    all_embeddings = np.vstack(all_embeddings)
    all_ids = np.array(all_ids)

    np.save(save_emb_path, all_embeddings)
    np.save(save_ids_path, all_ids)

    print(f"Embedding completed for: {csv_path}")
    print(f"Saved embeddings: {save_emb_path}")
    print(f"Saved IDs: {save_ids_path}")