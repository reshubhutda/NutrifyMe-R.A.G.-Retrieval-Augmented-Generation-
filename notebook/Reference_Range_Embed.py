# EXECUTION CODE BY reference_range_embed.py


from reference_embed_utils import embed_reference_csv

if __name__ == "__main__":
    embed_reference_csv(
        csv_path="data/Processed_Reference_Range.csv",
        save_emb_path="data/reference_embeddings.npy",
        save_ids_path="data/reference_row_ids.npy",
        batch_size=64
    )
