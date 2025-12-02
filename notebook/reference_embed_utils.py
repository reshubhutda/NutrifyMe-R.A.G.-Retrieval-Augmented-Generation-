# TESTING CODE EXECUTE BY reference_emebed_utils.py


import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def embed_reference_csv(
        csv_path: str,
        save_emb_path: str,
        save_ids_path: str,
        batch_size: int = 64,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
    print(f"Starting Reference Range embedding for {csv_path}")

    # Load CSV
    df = pd.read_csv(csv_path, dtype=str).fillna("Not Available")

    # Load embedding model
    model = SentenceTransformer(model_name)

    # Storage
    all_embeddings = []
    all_ids = []
    batch_texts = []
    batch_ids = []

    # Build text specifically for reference range dataset
    def build_text(row):
        return (
            f"{row['TEST']} "
            f"{row['Adult Range']} "
            f"{row['UNITS']} "
            f"{row['Child Range']} "
            f"{row['Adult Min']} "
            f"{row['Adult Max']} "
            f"{row['Child Min']} "
            f"{row['Child Max']}"
        )

    # Batch encode
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

    # Last incomplete batch
    if batch_texts:
        embs = model.encode(batch_texts, batch_size=batch_size, show_progress_bar=False)
        all_embeddings.append(embs)
        all_ids.extend(batch_ids)

    # Stack to arrays
    final_embeddings = np.vstack(all_embeddings)
    final_ids = np.array(all_ids)

    # Save
    np.save(save_emb_path, final_embeddings)
    np.save(save_ids_path, final_ids)

    print("Reference Range embedding completed.")
    print(f"Saved embeddings to {save_emb_path}")
    print(f"Saved row IDs to {save_ids_path}")
