import streamlit as st
from transformers import pipeline
import random

# Load Hugging Face text-generation model
generator = pipeline("text-generation", model="gpt2")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "tech_question_index" not in st.session_state:
    st.session_state.tech_question_index = 0

# Function to generate one unique, difficult skill-related question
def generate_skill_question(skill, qnum):
    prompt = (
        f"Generate a challenging and in-depth technical interview question #{qnum} "
        f"that evaluates advanced problem-solving ability in the skill: {skill}. "
        f"The question should be scenario-based or require deep explanation, not a simple definition."
    )
    output = generator(
        prompt,
        max_length=120,
        do_sample=True,
        top_k=40,
        top_p=0.9,
        temperature=0.9,
        repetition_penalty=2.5
    )[0]['generated_text']
    return output.strip()

# ---------------- UI Flow ---------------- #

st.title("💡 AI Mock Interviewer")

# Intro step
if st.session_state.step == "intro":
    st.write("👋 Hi there! I’ll be your friendly AI interviewer today. "
             "I’ll ask you a few details first, then confirm with you, "
             "and finally we’ll jump into 3 tough technical questions. 🚀")
    if st.button("Start"):
        st.session_state.step = "details"
        st.rerun()

# Collect details
elif st.session_state.step == "details":
    st.subheader("📋 Tell me about yourself")
    desired_position = st.text_input("Your desired job position")
    skills = st.text_input("Enter 5 skills (comma-separated)")
    
    if st.button("Submit Details"):
        if not desired_position or not skills:
            st.warning("Please fill out both fields!")
        else:
            st.session_state.answers["position"] = desired_position
            st.session_state.answers["skills"] = [s.strip() for s in skills.split(",") if s.strip()]
            st.session_state.step = "confirm"
            st.rerun()

# Confirm details
elif st.session_state.step == "confirm":
    st.subheader("✅ Please confirm your details before we continue")
    st.write(f"**Desired Position:** {st.session_state.answers['position']}")
    st.write("**Skills Provided:**")
    for skill in st.session_state.answers["skills"]:
        st.write(f"- {skill}")
    
    if st.button("Yes, looks good! Proceed"):
        st.session_state.step = "questions"
        st.rerun()
    if st.button("Edit Details"):
        st.session_state.step = "details"
        st.rerun()

# Interview questions
elif st.session_state.step == "questions":
    skills = st.session_state.answers["skills"]

    # pick exactly 3 random unique skills from provided list
    selected_skills = random.sample(skills, 3) if len(skills) > 3 else skills

    if not st.session_state.tech_questions:
        qlist = []
        used_questions = set()

        for i, skill in enumerate(selected_skills, start=1):
            while True:
                q = generate_skill_question(skill, i)
                if q not in used_questions:
                    used_questions.add(q)
                    qlist.append(q)
                    break
        st.session_state.tech_questions = qlist

    st.subheader("🎯 Interview Questions")
    idx = st.session_state.tech_question_index

    if idx < len(st.session_state.tech_questions):
        st.markdown(f"**Q{idx+1}:** {st.session_state.tech_questions[idx]}")
        if st.button("Next Question"):
            st.session_state.tech_question_index += 1
            st.rerun()
    else:
        st.success("🎉 That’s the end of your mock interview! Great job!")
