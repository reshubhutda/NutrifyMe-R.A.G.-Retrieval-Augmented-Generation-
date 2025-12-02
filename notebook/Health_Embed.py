# EXECUTION CODE FOR health_embed_utils.py

from health_embed_utils import embed_health_csv

if __name__ == "__main__":
    embed_health_csv(
        csv_path="data/Processed_Health.csv",
        save_emb_path="data/health_embeddings.npy",
        save_ids_path="data/health_row_ids.npy",
        batch_size=64
    )
