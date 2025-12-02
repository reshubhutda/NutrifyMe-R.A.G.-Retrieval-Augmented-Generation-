# # main.py

# from user_db import get_or_create_user, get_user_profile, get_user_conditions

# def main():
#     user_id = get_or_create_user()

#     profile = get_user_profile(user_id)
#     conditions = get_user_conditions(user_id)

#     print("\nUser Loaded:")
#     print(profile)
#     print("Conditions:", conditions)

# if __name__ == "__main__":
#     main()
# main.py

# main.py

from user_db import get_or_create_user, get_user_profile
from build_profile_db import build_profile_collection
from build_nutrition_db import build_nutrition_collection
from build_reference_db import build_reference_collection
from build_health_db import build_health_collection
from profile_summary import build_user_summary_text, build_user_summary_embedding
from query_retriever import query_multiple_dbs   # your retriever
from user_query import embed_query               # question embedder
from reference_loader import load_reference_ranges
from context_builder import build_context, clean_nutrition_entry
from profile_matcher_file import get_similar_nhanes_users
from nutrition_retriever import query_nutrition
import json
from Groq_LLM import ask_gemini
import google.generativeai as genai
import os


print("executed")

def pretty(obj):
    print(json.dumps(obj, indent=2))

def format_context(ctx):
    return json.dumps(ctx, indent=2, ensure_ascii=False)

def run_health_agent(user_question, user_id):
    """
    This function runs the ENTIRE health agent pipeline ONCE.
    It includes:
    - user_id creation
    - profile building
    - summary building
    - reference loading
    - NHANES matching
    - food extraction
    - query embedding
    - nutrition vector search
    - cleaning nutrition results
    - context building
    - LLM answering

    It is EXACTLY one iteration of your original while-loop,
    plus all the setup code before the loop.
    """

    # --------------------------------------------------
    # 1. SAME AS TOP OF main(), before your while-loop
    # --------------------------------------------------
    #user_id = get_or_create_user()

    profile_metadata = build_profile_collection(user_id)

    user_summary_text, user_summary_embedding = build_user_summary_embedding(user_id)

    reference_metadata, reference_embeddings = load_reference_ranges()

    nhanes_matches = get_similar_nhanes_users(user_id, top_k=5)

    # same gemini model
    model = genai.GenerativeModel("gemini-2.0-flash")

    # --------------------------------------------------
    # 2. SAME AS INSIDE your while-loop (ONE ITERATION)
    # --------------------------------------------------
    def extract_food(question):
        response = model.generate_content(f"""
            Extract ONLY the food or beverage name from this question.
            Return JUST the name, no explanation.

            Question: {question}
        """)
        return response.text.strip()

    food = extract_food(user_question)

    # embed food
    q_embedding = embed_query(food)

    # nutrition retrieval
    nutrition_matches = query_nutrition(q_embedding, top_k=5)

    raw_nutrition_list = nutrition_matches.get("metadata", [])

    # clean nutrition results
    clean_nutrition_list = [
        clean_nutrition_entry(entry) for entry in raw_nutrition_list
    ]

    # --------------------------------------------------
    # 3. Build final context (same as loop)
    # --------------------------------------------------
    final_context = build_context(
        profile_summary=user_summary_text,
        profile_metadata=profile_metadata,
        reference_metadata=reference_metadata,
        nhanes_matches=nhanes_matches,
        nutrition_list=clean_nutrition_list,
        user_question=user_question
    )

    # --------------------------------------------------
    # 4. Ask Gemini (same as loop)
    # --------------------------------------------------
    answer = ask_gemini(user_question, final_context)

    return answer

def main():

    # --------------------------------------------------
    # STEP 1 — Get or create user
    # --------------------------------------------------
    user_id = get_or_create_user()

    # --------------------------------------------------
    # STEP 2 — Rebuild profile_db entry for this user
    # --------------------------------------------------
    #print("\n[INFO] Updating profile_db with latest user profile...")
    profile_metadata = build_profile_collection(user_id)
    print("[INFO] profile_db updated successfully.")

    # --------------------------------------------------
    # STEP 3 — Print user’s profile summary (optional)
    # --------------------------------------------------
    #user_summary = build_user_summary_text(user_id)
    user_summary_text, user_summary_embedding = build_user_summary_embedding(user_id)
    #print("\n=== USER PROFILE SUMMARY ===")
    #print(user_summary_text)
    #print("============================\n")

    # --------------------------------------------------
    # STEP 4 — Get Reference Data
    # --------------------------------------------------
    reference_metadata, reference_embeddings = load_reference_ranges()

    # --------------------------------------------------
    # STEP 5 — Get Health Data
    # --------------------------------------------------
    nhanes_matches = get_similar_nhanes_users(user_id, top_k=5)

    # --------------------------------------------------
    # STEP 5.1 - Sending the above data to building context
    # --------------------------------------------------
    # base_context = build_context(
    #     user_id=user_id,
    #     profile_summary=user_summary_text,
    #     profile_embedding=user_summary_embedding,
    #     profile_metadata=profile_metadata,
    #     reference_metadata=reference_metadata,
    #     reference_embeddings=reference_embeddings,
    #     nhanes_matches=nhanes_matches
    # )
    # base_context = build_context(
    #     user_id=user_id,
    #     profile_summary=user_summary_text,
    #    # profile_embedding=user_summary_embedding,
    #     profile_metadata=profile_metadata,
    #     reference_metadata=reference_metadata,
    #     #reference_embeddings=reference_embeddings,
    #     nhanes_matches=nhanes_matches
    # )


    # ---------------------------------------------------------
    # STEP 7 — QUESTION LOOP
    # ---------------------------------------------------------
    model = genai.GenerativeModel("gemini-2.0-flash")
    while True:
        user_question = input("\nWhat is your question today? (type 'exit' to stop)\n> ")
        
        if user_question.lower() in ["exit", "quit", "stop"]:
            print("\n[INFO] Session ended.")
            break

        def extract_food(question):
            response = model.generate_content(f"""
        Extract ONLY the food or beverage name from this question. 
        Return JUST the name, no explanation.

        Question: {question}
        """)
            return response.text.strip()
        
        food = extract_food(user_question)

        # (A) Embed the question
        q_embedding = embed_query(food)

        nutrition_matches = query_nutrition(q_embedding, top_k=5)

        raw_nutrition_list = nutrition_matches.get("metadata", [])

        clean_nutrition_list = [
            clean_nutrition_entry(entry) for entry in raw_nutrition_list
        ]

        # final_context = {
        # **base_context,
        # "nutrition": clean_nutrition_list,
        # "question": user_question
        # }
        final_context = build_context(
        profile_summary=user_summary_text,
        profile_metadata=profile_metadata,
        reference_metadata=reference_metadata,
        nhanes_matches=nhanes_matches,
        nutrition_list=clean_nutrition_list,
        user_question=user_question
    )

        #print(final_context)
        #final_context = pretty(final_context)
        #json.dumps(final_context, indent=2)

        answer = ask_gemini(user_question, final_context)
        print(answer)


## code from the bottom is comemnted but I will keep it for now
    # # --------------------------------------------------
    # # STEP 4 — Ask the user’s question
    # # --------------------------------------------------
    # user_question = input("What is your question today?\n> ")

    # # embed question if needed
    # user_question_embedding = embed_query(user_question)

    # # --------------------------------------------------
    # # STEP 5 — Query all vector DBs (nutrition, reference, nhanes, profile)
    # # --------------------------------------------------
    # print("\n[INFO] Querying vector databases...")
    # results = query_multiple_dbs(user_question, user_id, top_k=3)

    # # STEP 6 — Display retrieved documents
    # # --------------------------------------------------
    # print("\n=========== RETRIEVAL RESULTS ===========")
    # for db_name, res in results.items():
    #     print(f"\n--- Results from: {db_name} ---")

    #     docs_lists = res.get("documents", [])
        
    #     if not docs_lists:
    #         print("No documents found.")
    #         continue

    #     docs = docs_lists[0]
    #     for i, doc in enumerate(docs, start=1):
    #         doc_preview = str(doc)[:].replace("\n", " ")
    #         print(f"\n[{db_name} result #{i}] {doc_preview}...")

    # print("\n==========================================\n")

    # # STEP 6 — Load reference ranges
    # reference_ranges = load_reference_ranges()
    # print(f"[INFO] Loaded {len(reference_ranges)} reference range entries.")

    # print("\n==========================================\n")

    
    # # --------------------------------------------------
    # # STEP 7 — (Later) merge retrieved docs + LLM reasoning
    # # --------------------------------------------------
    # print("[INFO] Retrieval stage complete. LLM reasoning comes next.")



if __name__ == "__main__":
    main()



