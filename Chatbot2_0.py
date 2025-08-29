import streamlit as st
from transformers import pipeline
import re

# -------------------- Hugging Face Pipeline Setup --------------------
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

# Function to generate one skill-related question
def generate_skill_question(desired_position, skills):
    prompt = f"Ask one interview question for a {desired_position} role focusing on these skills: {skills}."
    output = generator(prompt, max_length=150)[0]['generated_text']
    return output.strip()

# -------------------- Validation Helpers --------------------
def is_valid_name(name):
    parts = name.strip().split()
    return len(parts) >= 2 and all(part.isalpha() for part in parts)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_number(value):
    return value.isdigit()

# -------------------- Streamlit App --------------------
st.set_page_config(page_title="AI Interview Bot", layout="centered")
st.title("🤖 AI Interview Chatbot")

# Session state initialization
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.tech_questions_asked = False
    st.session_state.tech_questions = []
    st.session_state.tech_question_index = 0
    st.session_state.tech_answers = []

# Define the interview questions (personal details)
questions = [
    "Please enter your full name (First and Last name).",
    "Enter your 10-digit phone number.",
    "Enter your email address.",
    "Enter your highest qualification (e.g., B.Tech, MSc).",
    "Have you graduated? (yes/no)",
    "If graduated, enter your graduation score/percentage.",
    "Enter your total experience in years.",
    "Enter your current position (optional, press Enter to skip).",
    "Enter your desired position.",
    "Enter your skills (comma-separated)."
]

# -------------------- General Q&A --------------------
if st.session_state.step < len(questions):
    question = questions[st.session_state.step]
    with st.chat_message("assistant", avatar="🤖"):
        if st.session_state.step == 0:
            st.markdown("Hello! I am your AI interview assistant. I will be conducting your initial screening. Please be ready to answer some questions.")
        st.markdown(question)

    user_input = st.chat_input("Your answer:")
    if user_input:
        # Validation
        valid = True
        if st.session_state.step == 0 and not is_valid_name(user_input):
            st.warning("Please enter at least two names using letters only.")
            valid = False
        elif st.session_state.step == 1 and not is_valid_phone(user_input):
            st.warning("Invalid phone number. Enter exactly 10 digits.")
            valid = False
        elif st.session_state.step == 2 and not is_valid_email(user_input):
            st.warning("Invalid email address.")
            valid = False
        elif st.session_state.step in [5,6] and user_input and not is_valid_number(user_input):
            st.warning("Please enter a valid number.")
            valid = False

        if valid:
            st.session_state.answers.append(user_input)
            st.session_state.step += 1
            st.rerun()

# -------------------- Skill-based Question --------------------
elif not st.session_state.tech_questions_asked:
    desired_position = st.session_state.answers[8]
    skills = st.session_state.answers[9]
    with st.chat_message("assistant", avatar="⚛️"):
        st.markdown("Generating a skill-related technical question based on your desired position and skills...")

    # Generate **one** question
    qlist = [generate_skill_question(desired_position, skills)]
    st.session_state.tech_questions = qlist
    st.session_state.tech_questions_asked = True
    st.session_state.tech_question_index = 0
    st.rerun()

elif st.session_state.tech_question_index < len(st.session_state.tech_questions):
    # Show previous Q&A (if any)
    for idx in range(st.session_state.tech_question_index):
        with st.chat_message("assistant", avatar="⚛️"):
            st.markdown(f"Q{idx+1}: {st.session_state.tech_questions[idx]}")
        with st.chat_message("user", avatar="🙂"):
            st.markdown(st.session_state.tech_answers[idx])

    # Ask current question
    curr_q = st.session_state.tech_questions[st.session_state.tech_question_index]
    with st.chat_message("assistant", avatar="⚛️"):
        st.markdown(f"Q{st.session_state.tech_question_index+1}: {curr_q}")

    user_input = st.chat_input("Your answer:")
    if user_input:
        with st.chat_message("user", avatar="🙂"):
            st.markdown(user_input)
        st.session_state.tech_answers.append(user_input)
        st.session_state.tech_question_index += 1
        st.rerun()

# -------------------- End of Interview --------------------
else:
    st.success("✅ Thank you for completing the interview! 🎉 Here’s a summary:")
    st.subheader("📝 Personal Details")
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q}**")
        st.markdown(f"👉 {st.session_state.answers[i]}")

    st.subheader("⚡ Skill-based Question")
    for idx, tq in enumerate(st.session_state.tech_questions):
        st.markdown(f"**Q{idx+1}: {tq}**")
        st.markdown(f"👉 {st.session_state.tech_answers[idx]}")

    st.info("Our team will review your responses and get back to you soon!")
