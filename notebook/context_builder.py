from user_db import get_or_create_user, get_user_profile
from build_profile_db import build_profile_collection
from build_nutrition_db import build_nutrition_collection
from build_reference_db import build_reference_collection
from build_health_db import build_health_collection
from profile_summary import build_user_summary_text
from query_retriever import query_multiple_dbs   
from user_query import embed_query               
from reference_loader import load_reference_ranges
from nutrition_retriever import query_nutrition
from reference_loader import load_reference_ranges
from profile_matcher_file import get_similar_nhanes_users, BIOMARKER_COLS
import json

def build_context(
    profile_summary,
    profile_metadata,
    reference_metadata,
    nhanes_matches,
    nutrition_list,
    user_question
):
    """
    Build a clean, LLM-friendly context structure.

    Output schema:
    {
      "profile": {...},
      "reference_ranges": {...},
      "nhanes_matches": [...]
    }
    """

    # 1. PROFILE
    def build_profile(summary, meta):
        personal_info = {
            "user_id": meta.get("user_id"),
            "name": meta.get("name"),
            "age": meta.get("age"),
            "gender": meta.get("gender"),
            "ethnicity": meta.get("ethnicity"),
            "height_cm": meta.get("height_cm"),
            "weight_kg": meta.get("weight_kg"),
            "bmi": meta.get("bmi"),
            "marital_status": meta.get("marital_status"),
        }

        medical_info = {
            "conditions": meta.get("conditions", []),
            "medications": meta.get("medications", []),
        }

        return {
            "summary": summary,
            "personal_info": personal_info,
            "medical": medical_info,
        }

    # 2. REFERENCE RANGES 
    def build_reference_ranges(ref_meta_list):
        """
        reference_metadata is a list of dicts with keys like:
          TEST, UNITS, Adult Min, Adult Max, ...
        We compress this into a dict keyed by TEST.
        """
        ranges = {}
        for row in ref_meta_list:
            test_name = row.get("TEST")
            if not test_name:
                continue

            ranges[test_name] = {
                "units": row.get("UNITS"),
                "adult_min": row.get("Adult Min"),
                "adult_max": row.get("Adult Max"),
                "child_min": row.get("Child Min"),
                "child_max": row.get("Child Max"),
                # keep anything else if you ever need it
            }
        return ranges

    # 3. NHANES MATCHES 
    # We have already defined BIOMARKER_COLS  
    def extract_biomarkers(nh_meta):
        biomarkers = {}
        for col in BIOMARKER_COLS:
            biomarkers[col] = nh_meta.get(col)
        return biomarkers

    def build_nhanes_section(matches):
        nh_list = []
        for m in matches:
            nh_meta = m.get("metadata", {})
            nh_doc = m.get("document", "")

            nh_list.append(
                {
                    "demographics": nh_doc,                # human readable text
                    "biomarkers": extract_biomarkers(nh_meta),  # compact lab dict
                }
            )
        return nh_list

    # 4. ASSEMBLING CONTEXT 
    def build_nutrition_section(n_list):
        """
        n_list = cleaned entries from nutrition retriever.
        """
        formatted = []
        for entry in n_list:
            formatted.append({
                "food_name": entry.get("food_name"),
                "nutrients": entry.get("nutrients", {}),
                "ingredients": entry.get("ingredients", []),
                "labels": entry.get("labels", []),
                "raw_document": entry.get("raw_document", "")
            })
        return formatted

    # 5. FINAL CLEAN CONTEXT 
    context = {
        "profile": build_profile(profile_summary, profile_metadata),
        "reference_ranges": build_reference_ranges(reference_metadata),
        "nhanes_matches": build_nhanes_section(nhanes_matches),
        "nutrition": build_nutrition_section(nutrition_list),
        "question": user_question
    }


    return context


def clean_nutrition_entry(meta: dict):
    """
    Converts raw Chroma metadata for a nutrition entry into a clean, simple format.
    Handles uppercase keys, missing keys, and fixes escaped JSON strings.
    """

    # Normalize keys to lowercase because Chroma uses uppercase keys
    normalized = {k.lower(): v for k, v in meta.items()}

    food_name = normalized.get("food_name", "Unknown Food")

    #  Parse nutrients from NUTRITION_100G 
    raw_nutrients = normalized.get("nutrition_100g", "{}")

    if isinstance(raw_nutrients, str):
        try:
            nutrients = json.loads(raw_nutrients)  # Fix escaped JSON
        except:
            nutrients = {}
    elif isinstance(raw_nutrients, dict):
        nutrients = raw_nutrients
    else:
        nutrients = {}

    # Parse labels, ingredients, alternate names 
    labels = normalized.get("labels", "Not Available")
    if isinstance(labels, str):
        labels = [labels]

    ingredients = normalized.get("ingredients", "Not Available")
    if isinstance(ingredients, str):
        ingredients = [ingredients]

    alt_names = normalized.get("alternate_names", "Not Available")
    if isinstance(alt_names, str):
        alt_names = [alt_names]

    return {
        "food_name": food_name,
        "nutrients": nutrients,
        "labels": labels,
        "ingredients": ingredients,
        "alternate_names": alt_names
    }
