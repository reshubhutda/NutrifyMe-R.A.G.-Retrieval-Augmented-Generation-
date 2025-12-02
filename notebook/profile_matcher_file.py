# matching.py

import chromadb
import numpy as np

CHROMA_PATH = "./chroma_data"
client = chromadb.PersistentClient(path=CHROMA_PATH)

# 1. LOAD USER PROFILE

def load_user_profile(user_id: int):
    col = client.get_collection("profile_db")

    res = col.get(
        where={"user_id": user_id},
        include=["metadatas", "documents", "embeddings"]
    )

    if not res["metadatas"]:
        return None, None, None

    metadata  = res["metadatas"][0]
    document  = res["documents"][0]
    embedding = res["embeddings"][0]

    return metadata, document, embedding


# 2. LOAD NHANES COLLECTION

def load_all_nhanes_entries():
    col = client.get_collection("nhanes_db")

    res = col.get(
        include=["metadatas", "documents", "embeddings"]
    )

    return res["metadatas"], res["documents"], res["embeddings"]


# 3. CATEGORY MAPPERS (CORRECTED)

def map_race(value):
    if not value:
        return "Other/Mixed"

    v = str(value).lower()

    # white-like inputs
    if "american" in v or "aussie" in v or "european" in v:
        return "Non-Hispanic White"

    # black-like inputs
    if "black" in v or "african" in v:
        return "Non-Hispanic Black"

    # asian-like inputs
    if "asian" in v or "korean" in v or "chinese" in v or "japanese" in v or "indian" in v:
        return "Other/Mixed"

    # hispanic-like inputs
    if "hispanic" in v or "latino" in v:
        return "Mexican American"

    return "Other/Mixed"

### Some More Matching Logic for Further Refining of Matches:###

# def map_marital(value):
#     if not value:
#         return "Not Available"

#     v = str(value).lower()

#     if "single" in v or "never" in v:
#         return "Never Married"

#     if "married" in v or "partner" in v:
#         return "Married/Partner"

#     if "widow" in v or "divorced" in v or "separated" in v:
#         return "Wid/Div/Sep"

#     return "Not Available"


# def map_country(value):
#     if not value:
#         return "Foreign"

#     v = str(value).lower()

#     if v in ["usa", "us", "united states", "america", "u.s.", "u.s.a"]:
#         return "USA"

#     return "Foreign"
###-------------------------------------###

# 4. BIOMARKER COLUMNS (ALL)

BIOMARKER_COLS = [
    "WBC_COUNT", "LYMPHOCYTE_PCT", "MONOCYTE_PCT", "NEUTROPHIL_PCT",
    "EOSINOPHIL_PCT", "BASOPHIL_PCT", "LYMPHOCYTE_NUM", "RBC_COUNT",
    "HEMOGLOBIN", "HEMATOCRIT", "PLATELET_COUNT", "HDL Cholesterol (mg/dL)",
    "TRIGLYCERIDES_MG_DL_X", "LDL Cholesterol (mg/dL)", "HBA1C_PERCENT",
    "Fasting Glucose (mg/dL)", "HS_CRP_MG_L", "HEPATITIS_A_RESULT",
    "HEPATITIS_B_SURFACE_ANTIBODY", "ALBUMIN_CREATININE_RATIO_MG_G",
    "ALT (Alanine Aminotransferase) (U/L)", "Albumin (g/dL)",
    "ALP (Alkaline Phosphatase) (U/L)", "AST (Aspartate Aminotransferase) (U/L)",
    "Bicarbonate (mmol/L)", "BUN (Blood Urea Nitrogen) (mg/dL)",
    "Chloride (mmol/L)", "CK (Creatine Kinase) (U/L)", "Creatinine (mg/dL)",
    "Globulin (g/dL)", "GGT (Gamma-Glutamyl Transferase) (U/L)",
    "Iron (µg/dL)", "LDH (Lactate Dehydrogenase) (U/L)", "Magnesium (mg/dL)",
    "Osmolality (mOsm/kg)", "Phosphorus (mg/dL)", "Potassium (mmol/L)",
    "Sodium (mmol/L)", "Total Bilirubin (mg/dL)", "Calcium (mg/dL)",
    "Total Cholesterol (mg/dL)", "Total Protein (g/dL)", "TRIGLYCERIDES_MG_DL_Y",
    "Uric Acid (mg/dL)", "Vitamin D 25-OH (nmol/L)"
]



# 5. DEMOGRAPHIC MATCH (NOW WITH RACE ONLY)

def demographic_match(user, nh):

    # 1. Gender must match
    try:
        if user["gender"].lower() != nh["GENDER"].lower():
            return False
    except:
        return False

    # 2. Age ±3
    try:
        if abs(int(user["age"]) - int(nh["AGE"])) > 3:
            return False
    except:
        return False

    # 3. BMI ±1.5
    try:
        if abs(float(user["bmi"]) - float(nh["BMI"])) > 1.5:
            return False
    except:
        pass

    # 4. Race match (NEW)
    try:
        if map_race(user["ethnicity"]) != map_race(nh["RACE"]):
            return False
    except:
        return False

    return True

# 6. EUCLIDEAN SIMILARITY

def biomarker_distance(nh_entry):
    values = []
    for col in BIOMARKER_COLS:
        v = nh_entry.get(col)
        try:
            values.append(float(v))
        except:
            values.append(np.nan)

    arr = np.array(values, dtype=float)
    arr = np.nan_to_num(arr, nan=0.0)

    return np.linalg.norm(arr)

# 7. MAIN MATCHING LOGIC

def get_similar_nhanes_users(user_id: int, top_k=15):
    user_meta, _, _ = load_user_profile(user_id)
    if not user_meta:
        return []

    nh_metas, nh_docs, nh_embeds = load_all_nhanes_entries()

    candidates = []

    for i, nh in enumerate(nh_metas):

        if demographic_match(user_meta, nh):
            score = biomarker_distance(nh)
            #candidates.append((score, nh, nh_docs[i], nh_embeds[i]))
            candidates.append({
                "score": score,
                "metadata": nh,
                "document": nh_docs[i],
                "embedding": nh_embeds[i]
            })

# candidates.sort(key=lambda x: x[0])

    return candidates[:top_k]



# # TESTING RUN

# if __name__ == "__main__":
#     uid = int(input("Enter user_id: "))

#     matches = get_similar_nhanes_users(uid, top_k=15)

#     print(f"\nFound {len(matches)} matches:\n")

#     for _, meta, doc, embed in matches:
#         print(meta)
#         print(doc)
#         print(embed)


# # import chromadb

# # CHROMA_PATH = "./chroma_data"
# # client = chromadb.PersistentClient(path=CHROMA_PATH)

# # def get_profile_by_id(user_id: int):
# #     col = client.get_collection("profile_db")

# #     # user_id stored as STRING in metadata → convert
# #     uid = user_id

# #     res = col.get(
# #         where={"user_id": uid},
# #         include=["metadatas", "documents", "embeddings"]
# #     )

# #     # nothing found
# #     if not res["metadatas"]:
# #         return None, None, None

# #     metadata  = res["metadatas"][0]
# #     document  = res["documents"][0] if res["documents"] else None
# #     embedding = res["embeddings"][0] if len(res["embeddings"]) > 0 else None

# #     return metadata, document, embedding


# # # -------------------------------------------------------
# # # Test
# # # -------------------------------------------------------
# # if __name__ == "__main__":
# #     uid = int(input("Enter user_id: "))

# #     metadata, document, embedding = get_profile_by_id(uid)

# #     print("\n--- METADATA ---")
# #     print(metadata)

# #     print("\n--- DOCUMENT ---")
# #     print(document)

# #     print("\n--- EMBEDDING SHAPE ---")
# #     print(len(embedding) if embedding is not None else "No embedding")
# import chromadb

# CHROMA_PATH = "./chroma_data"
# client = chromadb.PersistentClient(path=CHROMA_PATH)

# def get_any_nhanes_sample():
#     col = client.get_collection("nhanes_db")

#     # fetch 1 item only
#     res = col.get(
#         ids=None,
#         limit=1,
#         include=["metadatas", "documents", "embeddings"]
#     )

#     if not res["metadatas"]:
#         return None, None, None

#     metadata  = res["metadatas"][0]
#     document  = res["documents"][0] if len(res.get("documents", [])) > 0 else None
#     embedding = res["embeddings"][0] if len(res.get("embeddings", [])) > 0 else None

#     return metadata, document, embedding



# # -------- TEST --------
# if __name__ == "__main__":
#     print("Fetching ANY ONE NHANES ENTRY...\n")

#     metadata, document, embedding = get_any_nhanes_sample()

#     print("\n--- METADATA ---")
#     print(metadata)

#     print("\n--- DOCUMENT ---")
#     print(document)

#     print("\n--- EMBEDDING SHAPE ---")
#     print(len(embedding) if embedding is not None else "No embedding")

