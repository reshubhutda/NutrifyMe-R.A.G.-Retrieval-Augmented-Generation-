## TESTING CODE ##

import chromadb
import pandas as pd

# 1. Load Chroma Client

client = chromadb.PersistentClient(path="chroma_db")

# 2. Select HEALTH collection

collection = client.get_collection("health")

# 3. Load CSV for numeric lookup

df = pd.read_csv("data/Processed_Health.csv", dtype=str).fillna("Not Available")

print("\nLoaded health CSV with", len(df), "rows.")


# 4. Ask user for a health-related query

query = input("\nEnter your health search query: ").strip()


#  5. Query Chroma (no embedding needed, text search)

results = collection.query(
    query_texts=[query],
    n_results=5
)

docs = results["documents"][0]
ids = results["ids"][0]
distances = results["distances"][0]

print("\n==============================")
print("HEALTH QUERY RESULTS")
print("================================")

numeric_columns = [col for col in df.columns if df[col].dtype != object]


# 6. Print results + numeric health values

for i, (doc, doc_id, dist) in enumerate(zip(docs, ids, distances)):
    
    print(f"\n------------------------------")
    print(f"Result {i+1}")
    print(f"Row ID: {doc_id}")
    print(f"Distance: {dist:.4f}")
    print("\nText Match:")
    print(doc[:300], "...")

    
    # Fetch CSV row
    try:
        row_index = int(doc_id)
    except ValueError:
        print("Invalid row ID, skipping...")
        continue
    
    row = df.iloc[row_index]

    
    # Print all numeric attributes for this user

    print("\nStructured Health Values:")
    for col in df.columns:
        try:
            val = float(row[col])
            print(f"{col}: {val}")
        except:
            pass

print("\n Health query completed successfully.")
