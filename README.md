🧙🏻‍♂️ JobSage – AI Hiring Assistant Chatbot
Project Overview
JobSage is an interactive, multi-step interview chatbot built with Streamlit and the Hugging Face OpenAI API. Designed for TalentScout, JobSage collects candidate information, validates responses, and generates skill-based technical questions in a friendly conversational UI. It streamlines the initial candidate screening with live validation, technical question generation, and a chat UX that feels modern and intuitive.

Features
Conversational Flow: Collects personal and professional details in a friendly, chat-style interface.

Live Validation: Ensures all inputs (name, phone, email, education, etc.) are correctly formatted as the interview progresses.

Custom LLM Questions: Generates technical interview questions tailored to the job role and the candidate’s skills.

Session State: Allows reruns/corrections without losing progress.

Chat UI: Uses Streamlit's st.chat_message for assistant and user, complete with emoji avatars.

Wizard Emoji Avatars: Assistant messages show 🧙🏻‍♂️; user messages use 😊.

Exit Button: Users can restart and clear the session at any time.

Data Privacy Notice: Candidates are informed at startup that their data will be saved for job purposes.

Demo
Installation Instructions
Clone the repository:

bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:

bash
pip install streamlit openai
Configure your Hugging Face API token:

Save your token in a file (such as mykey.txt) and load it in code, or

Set it as an environment variable (OPENAI_API_KEY), or

Use a .env file with python-dotenv.

Run the chatbot:

bash
streamlit run app.py
Usage Guide
On launch, the bot (🧙🏻‍♂️) introduces itself and displays a clear privacy message.

The user (😊) is guided step by step through essential personal and professional questions, which are live-validated.

After info collection, five technical questions are generated and presented.

At the end, a summary table is shown with all details and answers.

Use the Exit button to restart at any time.

Technical Details
Libraries Used:

Streamlit for UI and chat flow

OpenAI Python client (for Hugging Face router endpoint)

re for regex-based validation

Model:

Hugging Face OpenAI GPT LLM via their router API

Model used for generation: openai/gpt-oss-120b:cerebras

Architecture:

Stateless front-end driven by st.session_state for each user

Modular validation for each question

Technical questions generated on-the-fly from position/skills

Privacy message and emoji avatars enhance UX and compliance awareness

Prompt Design
Personal Questions:

Validated live using custom Python functions.

Question order, acceptable answers, and instructions clearly defined in personal_questions.

Technical Question Generation:

The chatbot crafts prompts like:
"Ask one concise moderate/advanced technical interview question for a {position} role focusing on these skills: {skills}. Keep it short (max 2 sentences)."

This ensures each technical question is targeted and brief.

Politeness/Content Checking:

When configured, the bot checks for inappropriate language using a simple LLM prompt:
"Does the following user message contain swear words or inappropriate language?..."

Data Privacy
Users are notified at startup, in small font, that their data is saved for job purposes.

No data is logged to disk unless you modify the code.

If using in production, add a privacy policy, consent screen, and GDPR compliance tools as required.

Challenges & Solutions
Challenge: Ensuring reliable input validation for various fields, including non-standard responses (like "NA").
Solution: Wrote robust validation functions and allowed bypasses when appropriate (e.g., score question).

Challenge: Preventing the exposure of API tokens in source code.
Solution: Supports reading from environment variables or a local ignored file.

Challenge: UX clarity for corrections and technical questions.
Solution: Used session state, chat history display, and markdown formatting for clear guidance and editing.

Challenge: Data privacy and transparency.
Solution: Added a privacy notice directly on the chat screen, following responsible data-handling guidelines.

Challenge: Handling impolite language.
Solution: Added LLM-driven check with polite warnings and automatic exit after repeated offenses.

Customization
Edit Questions: Change the personal_questions list to fit your use case.

Tweak Validation: Modify or expand the validation Python functions as needed.

Change Prompting or Policies: Update the startup privacy notice or add location-specific GDPR screens as required.
