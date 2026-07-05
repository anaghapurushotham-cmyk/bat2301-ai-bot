import streamlit as st
from google import genai

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

@st.cache_data
def load_context():
    try:
        with open("course_data.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

context = load_context()

st.title("AI Assistant")
st.markdown("Ask a question about the documents.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Type your question here"):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    if not context:
        st.error("course_data.txt not found.")
    else:
        prompt = f"""
You are a helpful assistant. Answer using only the CONTEXT below.
If the answer is not in the context, say you don't know.

CONTEXT:
{context}

QUESTION:
{question}
"""

        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        answer = response.text
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)
