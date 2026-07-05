"""
app.py  -  Step 3 of 3

A simple chatbot that answers questions using only YOUR documents.
It loads course_data.txt (created by prep_data.py) and sends it to the model
together with each question.

HOW TO RUN
  streamlit run app.py

You also need an API key in .streamlit/secrets.toml (see README).
"""

import streamlit as st
import google.generativeai as genai

# --- Page setup ---
st.set_page_config(page_title="AI Assistant", page_icon=":robot_face:")

# --- API key ---
# Read from .streamlit/secrets.toml when running locally, or from the app's
# Secrets settings when deployed online.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API key not found. Add GEMINI_API_KEY to your secrets file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


# --- Load your documents (read once, then reused) ---
@st.cache_data
def load_context():
    try:
        with open("course_data.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


context = load_context()

# --- Page content ---
st.title("AI Assistant")
st.markdown("Ask a question about the documents.")

# Change this text to set the assistant's personality and rules.
SYSTEM_INSTRUCTIONS = (
    "You are a helpful assistant. Answer the question using only the "
    "CONTEXT below. If the answer is not in the context, say you don't "
    "know instead of guessing."
)

# Keep the on-screen conversation in memory for this session.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show the conversation so far.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle a new question.
if question := st.chat_input("Type your question here"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not context:
        st.error("course_data.txt not found. Run prep_data.py first.")
    else:
        prompt = f"""{SYSTEM_INSTRUCTIONS}

CONTEXT:
{context}

QUESTION:
{question}
"""
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)

        answer = response.text
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
