import streamlit as st
from user_db import create_user, add_conditions, add_medications
from main import start_agent_once
from user_db import get_user_name
import time

st.set_page_config(page_title="NutrifyMe", layout="wide")

# SESSION STATE INITIALIZE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = None


# TITLE
st.markdown("""
<style>

    /* ===== Background color (dark blue) ===== */
    .stApp {
        background-color: #0F1C2E; /* Darker professional blue */
    }

    /* ===== Make all text white by default ===== */
    html, body, [class*="css"] {
        color: white !important;
    }

    /* ===== Page Title Styling ===== */
    .main-title {
        font-size: 58px;
        font-weight: 900;
        text-align: center;
        color: white;
        margin-top: -20px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #D0D8E3;
        font-size: 20px;
        margin-bottom: 40px;
    }

    /* ===== Chat input styling ===== */
    .stChatInputContainer {
        background-color: #1A2A40 !important;
        border-radius: 12px !important;
        border: 1px solid #30455F !important;
    }

    input, textarea {
        color: white !important;
    }

</style>
""", unsafe_allow_html=True)


# TITLE 
st.markdown("<h1 class='main-title'>NutrifyMe 🩺</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personalized Nutrition Health Assistant</p>", unsafe_allow_html=True)
# ------------------------------------------------------



# 1. UI

if st.session_state.user_id is None:

    with st.container():
        st.subheader("Login / Create Profile")

        choice = st.radio("Do you already have a User ID?", ["Yes", "No"])

        if choice == "Yes":
            entered_id = st.text_input("Enter your User ID")

            if st.button("Continue"):
                st.session_state.user_id = int(entered_id)
                st.session_state.username = get_user_name(st.session_state.user_id)
                st.rerun()

        else:
            st.markdown("### Create New Profile")

            name = st.text_input("Name")
            age = st.number_input("Age", 1, 120)
            gender = st.text_input("Gender")
            ethnicity = st.text_input("Ethnicity")
            marital = st.text_input("Marital Status")
            height = st.number_input("Height (cm)")
            weight = st.number_input("Weight (kg)")

            conditions = st.text_input("Medical Conditions (comma separated)")
            medications = st.text_input("Medications (comma separated)")

            if st.button("Create Profile"):
                bmi = weight / ((height / 100) ** 2)

                user_id = create_user(
                    name, age, gender, ethnicity, marital, height, weight, bmi
                )

                if conditions.strip():
                    add_conditions(user_id, conditions.split(","))

                if medications.strip():
                    add_medications(user_id, medications.split(","))

                st.success(f"Profile Created! Your User ID = {user_id}")
                time.sleep(0.4)
                st.session_state.user_id = user_id

                # fetch username safely
                username = get_user_name(user_id)
                if username is None:
                    time.sleep(0.2)
                    username = get_user_name(user_id)

                st.session_state.username = username

                st.rerun()
    st.stop()



# 2. CHAT INTERFACE

st.markdown(f"### 👋 Welcome to the chat, {st.session_state.username}")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input box at bottom
user_input = st.chat_input("Ask something about your food or health...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Run agent
    reply = start_agent_once(st.session_state.user_id, user_input)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
