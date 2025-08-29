import streamlit as st
from openai import OpenAI
import re

# Hugging Face OpenAI API Setup
with open("mykey.txt") as f:
    HF_API_KEY = f.read().strip()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

# Validation Functions
def is_valid_name(name):
    parts = name.strip().split()
    return len(parts) >= 2 and all(part.isalpha() for part in parts)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_alpha(value):
    return value.isalpha()

def is_yes_no(value):
    return value.lower() in ["yes", "no"]

def is_valid_score(value):
    try:
        float(value)
        return True
    except:
        return value.upper() == "NA"

# LLM-based polite language check
def is_message_polite(message):
    prompt = (
        "Does the following user message contain swear words or inappropriate language? "
        "Please answer 'yes' or 'no' only.\n\n"
        f"Message: \"{message}\""
    )
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = completion.choices[0].message.content.strip().lower()
    return answer == "no"

# Streamlit Setup
st.set_page_config(page_title="JobSage Chatbot", layout="wide")
st.markdown("""
    <style>
    .exit-button {position: fixed; top: 10px; right: 20px; background-color: #FF4B4B; color: white;
    padding: 5px 15px; border-radius: 5px; border: none; font-weight: bold; z-index:999;}
    </style>
    """, unsafe_allow_html=True)

# Exit button resets state to show intro again
if st.button("Exit", key="exit_button"):
    st.session_state.started = False
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.tech_questions = []
    st.session_state.tech_answers = []
    st.session_state.tech_index = 0
    st.session_state.confirm_stage = False
    st.session_state.correction_stage = False
    st.session_state.swear_count = 0
    st.session_state.ended_due_to_inappropriate_language = False
    st.rerun()

# Session State Initialization
if "started" not in st.session_state:
    st.session_state.started = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "tech_answers" not in st.session_state:
    st.session_state.tech_answers = []
if "tech_index" not in st.session_state:
    st.session_state.tech_index = 0
if "confirm_stage" not in st.session_state:
    st.session_state.confirm_stage = False
if "correction_stage" not in st.session_state:
    st.session_state.correction_stage = False
if "swear_count" not in st.session_state:
    st.session_state.swear_count = 0
if "ended_due_to_inappropriate_language" not in st.session_state:
    st.session_state.ended_due_to_inappropriate_language = False

personal_questions = [
    ("Full Name (First and Last name)", is_valid_name),
    ("Phone Number (10 digits)", is_valid_phone),
    ("Email Address", is_valid_email),
    ("Location (city/state)", is_valid_alpha),
    ("Highest Education", is_valid_alpha),
    ("Graduated? (yes/no)", is_yes_no),
    ("Score/Percentage (only if graduated, else type NA)", is_valid_score),
    ("Current Position (optional, type NA if none)", lambda x: True),
    ("Total Experience in years", lambda x: x.isdigit()),
    ("Desired Position", lambda x: True),
    ("Skills (comma-separated)", lambda x: True)
]

def generate_skill_question(position, skills, experience):
    difficulty = "moderate" if int(experience) < 2 else "advanced"
    prompt = f"Ask one concise {difficulty} technical interview question for a {position} role with these skills: {skills}. Keep it short (max 2 sentences)."
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content.strip()

def process_user_input(user_input):
    polite = is_message_polite(user_input)
    if not polite:
        st.session_state.swear_count += 1
        if st.session_state.swear_count == 1:
            with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                st.markdown("🛑 Please be polite during this conversation. Let's continue.")
            return False
        else:
            st.session_state.ended_due_to_inappropriate_language = True
            return False
    return True

if not st.session_state.started:
    with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
        st.markdown("Hi I am **JobSage**, a hiring assistant chatbot for TalentScout. I'll be taking your initial screen processing today. Type **hi** to continue.")
    user_input = st.chat_input("Type hi to continue...")
    if user_input is not None:
        if process_user_input(user_input):
            if user_input.strip().lower() == "hi":
                st.session_state.started = True
                st.rerun()
else:
    if st.session_state.ended_due_to_inappropriate_language:
        with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
            st.error("🚫 You have used inappropriate language multiple times. We will not move ahead. Goodbye!")
    else:
        if st.session_state.correction_stage:
            with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                st.markdown("Current details (copy the exact field name to correct):")
                for q, a in st.session_state.answers.items():
                    st.markdown(f"**{q}:**")
                    st.markdown(f"😊 {a}")
                st.markdown(
                    "Please enter the correction in this format: \n"
                    "`Field Name: new value`\n\n"
                    "For example: `Phone Number (10 digits): 9876543210`"
                )
            user_input = st.chat_input("Type correction (e.g., Phone Number (10 digits): 9876543210)...")
            if user_input is not None:
                if not process_user_input(user_input):
                    st.rerun()
                if ":" not in user_input:
                    st.warning("Please use the format: Field Name: new value")
                else:
                    field_candidate, new_value = user_input.split(":", 1)
                    field_candidate = field_candidate.strip()
                    new_value = new_value.strip()
                    valid_fields = [q for q, _ in personal_questions]
                    if field_candidate not in valid_fields:
                        st.warning("Invalid field name. Please copy and paste the field name exactly. Try again.")
                    else:
                        validator = dict(personal_questions)[field_candidate]
                        if not validator(new_value):
                            st.warning("Invalid value for this field. Please check the format and try again.")
                        else:
                            st.session_state.answers[field_candidate] = new_value
                            st.session_state.correction_stage = False
                            st.session_state.confirm_stage = True
                            st.rerun()

        elif st.session_state.confirm_stage:
            with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                st.markdown("Here are the details you entered. Are all of these correct? Type **yes** to confirm, or **no** to make a correction.")
                for q, a in st.session_state.answers.items():
                    st.markdown(f"**{q}:**")
                    st.markdown(f"😊 {a}")
            user_input = st.chat_input("Are all details correct? (yes/no)")
            if user_input is not None:
                if not process_user_input(user_input):
                    st.rerun()
                if user_input.strip().lower() == "yes":
                    st.session_state.confirm_stage = False
                    st.rerun()
                elif user_input.strip().lower() == "no":
                    st.session_state.correction_stage = True
                    st.rerun()
                else:
                    st.warning("Please type **yes** or **no**.")

        elif st.session_state.step < len(personal_questions):
            question, validator = personal_questions[st.session_state.step]
            for q, a in st.session_state.answers.items():
                with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                    st.markdown(f"**{q}:**")
                with st.chat_message("user", avatar="😊"):
                    st.markdown(a)
            with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                st.markdown(question)
            user_input = st.chat_input("Your answer...")
            if user_input is not None:
                if not process_user_input(user_input):
                    st.rerun()
                if not validator(user_input):
                    st.warning("Invalid input, please try again.")
                else:
                    st.session_state.answers[question] = user_input
                    st.session_state.step += 1
                    if st.session_state.step == len(personal_questions):
                        st.session_state.confirm_stage = True
                    st.rerun()

        elif st.session_state.tech_index < 5:
            if not st.session_state.tech_questions:
                experience = st.session_state.answers["Total Experience in years"]
                position = st.session_state.answers["Desired Position"]
                skills = st.session_state.answers["Skills (comma-separated)"]
                with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                    st.markdown("Generating technical questions... ⏳")
                for _ in range(5):
                    q = generate_skill_question(position, skills, experience)
                    st.session_state.tech_questions.append(q)
            for i in range(st.session_state.tech_index):
                with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                    st.markdown(f"**Q{i+1}:** {st.session_state.tech_questions[i]}")
                with st.chat_message("user", avatar="😊"):
                    st.markdown(st.session_state.tech_answers[i])
            curr_q = st.session_state.tech_questions[st.session_state.tech_index]
            with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
                st.markdown(curr_q + " ⏳")
            user_input = st.chat_input("Your answer...")
            if user_input is not None:
                if not process_user_input(user_input):
                    st.rerun()
                st.session_state.tech_answers.append(user_input)
                st.session_state.tech_index += 1
                st.rerun()

        else:
            st.success("✅ You have completed the interview! 🎉")
            st.subheader("📝 Your Personal Details")
            for q, a in st.session_state.answers.items():
                st.markdown(f"**{q}:**")
                st.markdown(f"😊 {a}")
            st.subheader("⚡ Skill-based Questions and Your Answers")
            for i, q in enumerate(st.session_state.tech_questions):
                st.markdown(f"**Q{i+1}: {q}**")
                st.markdown(f"😊 {st.session_state.tech_answers[i]}")
            st.info("Our team will review your responses and get back to you soon!")
