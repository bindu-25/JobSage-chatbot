🧙🏻‍♂️ JobSage – AI Hiring Assistant Chatbot
This is an interactive, multi-step interview chatbot built with Streamlit and the Hugging Face OpenAI API. JobSage acts as an AI assistant for TalentScout, collecting candidate information, validating responses, and administering skill-based technical questions in a conversational interface.

Features
Conversational Flow: Collects personal and professional details in a friendly, chat-style UI.

Live Validation: Ensures all inputs (name, phone, email, education, etc.) are correctly formatted as the interview progresses.

Custom LLM Questions: Generates technical interview questions tailored to the desired position and listed skills.

Chat UI: Uses Streamlit's st.chat_message for intuitive, real-time chatbot and user messaging.

Session State: Allows reruns and corrections without losing progress.

Wizard Emoji Avatars: Assistant avatar is 🧙🏻‍♂️; user avatar is 😊 for a friendly experience.

Exit Button: Let users reset the interview to the introduction at any time.

Demo
Usage
Clone the repository:

text
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install requirements:

text
pip install streamlit openai
Get your Hugging Face API token and paste it at the top of the script:

python
HF_API_KEY = "your-huggingface-token"
Run the chatbot:

text
streamlit run app.py
How it Works
On launch, the bot (🧙🏻‍♂️) introduces itself and collects user details step by step, validating each field.

After personal details, the bot generates five technical questions suited to the candidate's profile.

All input and answers are displayed with friendly emoji avatars.

At the end, a summary is shown with all personal details and Q&A.

Users can use the Exit button anytime to restart the interview.

Customization
Questions: Edit the personal_questions list to adjust what details are collected.

Technical Questions: The generate_skill_question() function generates custom questions using the LLM.

Validation: Modify the validation functions for stricter/looser input rules.
