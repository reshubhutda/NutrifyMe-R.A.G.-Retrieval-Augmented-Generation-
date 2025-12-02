# TESTING CODE EXECUTE BY Health_Embed.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

print("Script Started")

def embed_health_csv(
    csv_path,
    save_emb_path,
    save_ids_path,
    batch_size=64,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
):
    """
    Embeds contextual/descriptive fields from the Health dataset.

    Only non-numeric and categorical features are used for embedding.
    Numeric lab values are skipped because embeddings are not suitable
    for numerical reasoning.
    """

    print(f"\nLoading CSV: {csv_path}")
    df = pd.read_csv(csv_path, dtype=str).fillna("Not Available")

    print("Loading model...")
    model = SentenceTransformer(model_name)

    # Prepare storage
    all_embeddings = []
    all_ids = []
    batch_texts = []
    batch_ids = []

    # Define which columns to embed (ONLY semantic fields)
    embed_cols = [
        "GENDER",
        "AGE",
        "RACE",
        "BIRTH_COUNTRY",
        "Marital_Status",
        "BMI_Category"
    ]

    # Build text from selected columns
    def build_text(row):
        parts = []
        for col in embed_cols:
            if col in row:
                parts.append(f"{col}: {row[col]}")
        return " | ".join(parts)

    print("Starting embedding process...")
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

    # Process final incomplete batch
    if batch_texts:
        embs = model.encode(batch_texts, batch_size=batch_size, show_progress_bar=False)
        all_embeddings.append(embs)
        all_ids.extend(batch_ids)

    # Stack and save results
    all_embeddings = np.vstack(all_embeddings)
    all_ids = np.array(all_ids)

    np.save(save_emb_path, all_embeddings)
    np.save(save_ids_path, all_ids)

    print("\n Embedding completed successfully.")
    print(f" Saved embeddings to → {save_emb_path}")
    print(f" Saved row IDs to → {save_ids_path}")
