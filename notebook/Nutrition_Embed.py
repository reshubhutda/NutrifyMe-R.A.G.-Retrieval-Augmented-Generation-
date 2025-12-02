# EXECUTe  nutrtion_embed_utils.py

from nutrition_embed_utils import embed_csv

if __name__ == "__main__":
    embed_csv(
        csv_path="data/Processed_Nutrition.csv",
        save_emb_path="data/nutrition_embeddings.npy",
        save_ids_path="data/nutrition_row_ids.npy",
        batch_size=64
    )
