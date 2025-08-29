import streamlit as st
import re

def is_valid_email(email):
    return "@" in email and "." in email

def is_valid_phone(phone):
    return phone.isdigit() and (10 <= len(phone) <= 13)

questions = [
    {"label": "Full Name", "key": "full_name", "validate": lambda x: len(x.strip().split()) >= 2, "error": "Please enter your full name (first and last)."},
    {"label": "Email Address", "key": "email", "validate": is_valid_email, "error": "Please enter a valid email address."},
    {"label": "Phone Number", "key": "phone", "validate": is_valid_phone, "error": "Please enter a valid phone number (10-13 digits)."},
    {"label": "Years of Experience", "key": "experience", "validate": lambda x: x.isdigit() and int(x)>=0, "error": "Please enter number of years as a non-negative integer."},
    {"label": "Desired Position", "key": "position", "validate": lambda x: x.strip() != "", "error": "Please specify the desired position."},
    {"label": "Current Location", "key": "location", "validate": lambda x: x.strip() != "", "error": "Please enter your current location."},
    {"label": "Tech Stack (skills, tools, languages)", "key": "tech_stack", "validate": lambda x: x.strip() != "", "error": "Please describe your main tech stack."}
]

if "step" not in st.session_state:
    st.session_state.step = -1
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("JobSage - Conversational Hiring Assistant")

# Exit detection
exit_keywords = {"exit", "quit", "stop", "goodbye", "bye"}
def check_exit(user_input):
    return user_input and user_input.strip().lower() in exit_keywords

# Greeting and start
if st.session_state.step == -1:
    st.markdown("👋 Welcome to **JobSage**!\n\nI'm here to assist you with the initial candidate screening for tech roles. Please answer a few short questions so we can understand your background and interests.\n\n*Type 'exit' to quit at any time.*")
    user_input = st.text_input("Type 'yes' to begin:", key='start_input')
    if check_exit(user_input):
        st.markdown("👋 Thanks for stopping by! Have a great day.")
        st.stop()
    if user_input and user_input.strip().lower() == "yes":
        st.session_state.step = 0
        st.rerun()

# Sequential Q&A
elif st.session_state.step < len(questions):
    question = questions[st.session_state.step]
    st.markdown(f"**{question['label']}**")
    user_input = st.text_input("Your answer:", key=f"input_{st.session_state.step}")
    if check_exit(user_input):
        st.markdown("👋 Interview exited. Thank you and best wishes!")
        st.stop()
    if user_input:
        if question["validate"](user_input):
            st.session_state.answers[question["key"]] = user_input.strip()
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning(question["error"])

# Completion and summary
else:
    st.success("Thank you! Here is the information you provided:")
    for q in questions:
        st.write(f"**{q['label']}**: {st.session_state.answers.get(q['key'], '')}")
    st.markdown("✅ Your details have been recorded. JobSage will be in touch with next steps!")
