import google.generativeai as genai
import os
import json

# Set your Gemini API key
genai.configure(api_key="AIzaSyDw9BGDOjDOOO9SXoJuYERe0P6nsjWUQ-0")

def ask_gemini(user_question, final_context):
    """
    final_context schema (Option C):

    {
      "profile": {
        "summary": str,
        "personal_info": {...},
        "medical": {...}
      },
      "reference_ranges": {
        "TEST_NAME": { "units": ..., "adult_min": ..., ... },
        ...
      },
      "nhanes_matches": [
        {
          "demographics": str,
          "biomarkers": {...}
        },
        ...
      },
      "nutrition": [
        {
          "food_name": str,
          "nutrients": {...},
          "labels": [...],
          "ingredients": [...],
          "raw_document": str
        },
        ...
      ],
      "question": str
    }
    """

    ctx_json = json.dumps(final_context, indent=2)
    print(ctx_json)
    prompt = f"""
You are a careful health assistant.

You will receive a JSON object with these keys:

- "profile": user summary, demographics, conditions, and medications.
- "reference_ranges": reference ranges for lab tests (min/max, units) which will help you in comparison.
- "nhanes_matches": similar people like the profile but with biomarkers from the NHANES dataset with their biomarker values.
- "nutrition": nutrition facts, labels, and ingredients for foods relevant to the question which will tell you nutrtients.
- "question": the user's original question.

JSON_CONTEXT:
{ctx_json}

RULES:
1. If the user's question does NOT mention a food, beverage, nutrient, diet, or health-related concern, DO NOT generate any medical or nutritional analysis.
   Instead answer them based on the question asked from your own knowledge in concise way and then politely ask the user what food or nutrition-related question they
   would like help with.
2. Your PRIMARY reasoning source is JSON_CONTEXT.
3. You MAY use general medical/nutritional knowledge from outside sources
   ONLY for explanations (e.g., what sugar does, what cholesterol means).
   NEVER invent biomarker values, nutrition values, or foods.
4. ALL biomarkers MUST come from NHANES proxy entries in JSON_CONTEXT.
5. ALWAYS compare proxy biomarker values to reference_ranges to decide
   whether a value is low/normal/high.
6.  When analyzing any food, ALWAYS start from the nutrition object provided (nutrients, ingredients, labels, serving info).
7. If information you need is missing, say:
   "This information is not available in the provided context."
8. No hallucinated numbers. General explanations are allowed.

TASK:
1. If the question is general (e.g., “hi”, “hello”, “I have a question”, "Hey NutrifyMe, how are you doing?", "Hey, wassup", "Thank you" or anything similar), respond
   with a short greeting and answer them with your general knowledge and your own database and ask them politely what food or nutrition topic the user wants
   help with. Do NOT analyze the profile, NHANES, or nutrition data yet.
2. First understand the user's health context from "profile", "reference_ranges", and "nhanes_matches".
3. Identify which foods in the "nutrition" section relate to the question.
4. Use NHANES proxy biomarkers to infer the user’s likely biomarker pattern.
5. Extract all nutrient values (carbs, sugars, sodium, fats, protein, vitamins, etc.) and assess their health impact based on the user profile.
6. Use NHANES proxy biomarkers to infer the user's likely risk pattern (e.g., cholesterol tendency, glucose tendency, inflammatory tendency).
7. Analyze the food(s) in the question using the nutrition section.
8. Provide a personalized, safety-first assessment of the food(s):
      - beneficial
      - neutral
      - caution
      - avoid / limit
   with clear reasoning.
9. If some information you would normally need is missing, say that you cannot fully answer with the current data.
10. Combine all reasoning into a clear, safe, personalized answer.

Now answer the user's question.
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text