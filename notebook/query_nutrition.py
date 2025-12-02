## TESTING CODE ##


# import chromadb
# from sentence_transformers import SentenceTransformer
# import sys

# # Get user query
# if len(sys.argv) < 2:
#     print("Usage: python query_chroma.py \"your query here\"")
#     sys.exit()

# query_text = sys.argv[1]
# print(f"\n=== Querying nutrition ===")
# print(f"Query: {query_text}\n")

# # Load Chroma client
# client = chromadb.PersistentClient(path="chroma_db")

# # Always use nutrition
# collection = client.get_collection("nutrition")

# # Load embedding model ONLY to embed user's query
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# # Encode user query
# query_embedding = model.encode([query_text])[0].tolist()

# # Search top 5 results
# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=5
# )

# # Print results
# docs = results.get("documents", [[]])[0]
# ids = results.get("ids", [[]])[0]

# for i, (doc, doc_id) in enumerate(zip(docs, ids)):
#     print(f"\nResult {i+1} (Row ID: {doc_id}):")
#     print(doc[:10000], "...")

# print("\n=== Done ===")


import chromadb
import pandas as pd
import numpy as np
import json


# 1. Load Chroma Client

client = chromadb.PersistentClient(path="chroma_db")


# 2. Select ONE collection for testing (Nutrition)

collection = client.get_collection("nutrition")


# 3. Load CSV for numeric lookup (structured values)

df = pd.read_csv("data/Processed_Nutrition.csv", dtype=str).fillna("Not Available")

print("\n Loaded nutrition CSV with", len(df), "rows.")


# 4. Ask user for a query

query = input("\nEnter your search query: ").strip()


# 5. Embed query using collection's embedding function

results = collection.query(
    query_texts=[query],
    n_results=5
)

docs = results["documents"][0]
ids = results["ids"][0]
distances = results["distances"][0]

print("\n==============================")
print("QUERY RESULTS")
print("================================")


# 6. Loop through results and print semantic + numeric data

for i, (doc, doc_id, dist) in enumerate(zip(docs, ids, distances)):

    print(f"\n------------------------------")
    print(f"Result {i+1}")
    print(f"Row ID: {doc_id}")
    print(f"Distance: {dist:.4f}")
    print("\nText Match:")
    print(doc[:300], "...")


    #  Fetch CSV row using row_id

    try:
        row_index = int(doc_id)
    except ValueError:
        print("Invalid row ID, skipping...")
        continue

    row = df.iloc[row_index]

    
    # Parse JSON nutrition values
    
    numeric_json = None

    # Check possible column names
    possible_json_columns = [
        "NUTRITION_100G"
    ]

    for col in possible_json_columns:
        if col in df.columns:
            try:
                numeric_json = json.loads(row[col])
            except:
                numeric_json = None
            break

    
    # Show numeric structured nutrition values

    print("\nStructured Numeric Values:")
    
    if numeric_json:
        for key, value in numeric_json.items():
            print(f"{key}: {value}")
    else:
        print("No structured JSON found in this row. Check CSV column name.")

print("\n Query completed successfully.")
