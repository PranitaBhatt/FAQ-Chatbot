import streamlit as st
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found! Please set GROQ_API_KEY in your .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

#load faq
try:
    with open("faq.json", "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except Exception as e:
    st.error(f"❌ Could not load faq.json: {e}")
    st.stop()

def get_answer(user_input):
    """Search FAQ JSON for an answer (simple match)."""
    q = user_input.lower()
    for item in faq_data:
        if item["question"].lower() in q:
            return item["answer"]
    return None
#ai use
def ai_fallback(user_input):
    """Call Groq AI if FAQ not found."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"(AI Error: {e})"

#streamlit setup
st.set_page_config(page_title="Iron Lady Chatbot", page_icon="🤖")
st.title("🤖 Iron Lady FAQ Chatbot")

user_input = st.text_input("Ask me about Iron Lady programs:")

if user_input:
    answer = get_answer(user_input)
    if answer:
        st.success(f"**Bot:** {answer}")
    else:
        st.info("Hmm, I don’t know that. Let me check with AI 🤔")
        ai_resp = ai_fallback(user_input)
        st.write(f"**AI Bot:** {ai_resp}")
