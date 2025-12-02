## TESTING CODE ##


import chromadb
import pandas as pd

# 1. Load Chroma Client

client = chromadb.PersistentClient(path="chroma_db")


# 2. Select REFERENCE collection

collection = client.get_collection("reference")

# 3. Load Reference Range CSV

df = pd.read_csv("data/Processed_Reference_Range.csv", dtype=str).fillna("Not Available")

print("\nLoaded reference range CSV with", len(df), "rows.")


# 4. Ask user for a lab test query

query = input("\nEnter your reference test search query: ").strip()

# 5. Query Chroma using text search
results = collection.query(
    query_texts=[query],
    n_results=5
)

docs = results["documents"][0]
ids = results["ids"][0]
distances = results["distances"][0]

print("\n==============================")
print("REFERENCE RANGE QUERY RESULTS")
print("==============================")


# 6. Identify numeric reference columns

numeric_cols = []

for col in ["Adult Min", "Adult Max", "Child Min", "Child Max"]:
    if col in df.columns:
        numeric_cols.append(col)

# 7. Loop through results and display structured ranges

for i, (doc, doc_id, dist) in enumerate(zip(docs, ids, distances)):

    print(f"\n------------------------------")
    print(f"Result {i+1}")
    print(f"Row ID: {doc_id}")
    print(f"Distance: {dist:.4f}")

    print("\nText Match:")
    print(doc[:500], "...")

    # Fetch CSV row using row index

    try:
        row_index = int(doc_id)
    except ValueError:
        print("Invalid row ID — skipping")
        continue

    row = df.iloc[row_index]


    # Print structured reference ranges

    print("\nStructured Reference Ranges:")

    test_name = row.get("TEST", "Not Available")
    print(f"TEST: {test_name}")

    units = row.get("UNITS", "Not Available")
    print(f"UNITS: {units}")

    # Adult values
    if "Adult Range" in df.columns:
        print(f"Adult Range: {row['Adult Range']}")

    for col in numeric_cols:
        val = row[col]
        print(f"{col}: {val}")

    print("\n--------------------------------")

print("\nReference range query completed.")
