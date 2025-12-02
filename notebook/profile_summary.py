from user_db import get_user_profile, get_user_conditions, get_user_medications
from user_query import embed_query  # your existing embed function

def build_user_summary_text(user_id: int) -> str:
    profile = get_user_profile(user_id)
    conditions = get_user_conditions(user_id)
    meds = get_user_medications(user_id)

    if not profile:
        raise ValueError(f"No profile found for user_id={user_id}")

    name = profile.get("name") or "The user"
    age = profile.get("age")
    gender = profile.get("gender") or ""
    ethnicity = profile.get("ethnicity") or ""
    marital = profile.get("marital_status") or ""
    height_cm = profile.get("height_cm")
    weight_kg = profile.get("weight_kg")
    bmi = profile.get("bmi")

    cond_text = ", ".join(conditions) if conditions else "none reported"
    meds_text = ", ".join(meds) if meds else "none reported"

    summary = (
        f"{name} is a {age}-year-old {gender} with BMI {bmi:.1f}, "
        f"height {height_cm:.1f} cm and weight {weight_kg:.1f} kg. "
        f"Ethnicity: {ethnicity}. Marital status: {marital}. "
        f"Reported medical conditions: {cond_text}. "
        f"Current medications: {meds_text}."
    )

    return summary


def build_user_summary_embedding(user_id: int):
    """
    Returns (summary_text, embedding_vector) for this user.
    """
    summary = build_user_summary_text(user_id)
    embedding = embed_query(summary)
    return summary, embedding
