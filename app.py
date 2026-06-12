import streamlit as st
import json
import os
from groq import Groq
import chromadb

# 1. CONFIG & SETUP
st.set_page_config(page_title="Ask Osaka AI Concierge", page_icon="🏯")
st.title("🏯 Ask Osaka")
st.caption("Your AI local guide. Ask about food, events, transit, or hidden gems.")

# Get API Key safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Enter your Groq API Key", type="password", key="groq_key")
    if not GROQ_API_KEY:
        st.stop()

groq_client = Groq(api_key=GROQ_API_KEY)

# 2. LOAD DATA (Simple approach - no vector DB for MVP)
@st.cache_data
def load_osaka_data():
    try:
        with open("osaka_restaurants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

osaka_data = load_osaka_data()

if osaka_data:
    st.success(f"✅ Loaded {len(osaka_data)} Osaka items into knowledge base.")

# 3. SYSTEM PROMPT & RAG LOGIC
SYSTEM_PROMPT = """You are "Ask Osaka", a friendly, knowledgeable AI concierge for Osaka, Japan.
- Speak in the user's language. Keep answers concise, practical, and locally accurate.
- Emphasize Osaka's "kuidaore" (eat till you drop) culture. Recommend food often.
- Distinguish districts: Kita/Umeda (modern/shopping), Minami/Namba/Dotonbori (neon/street food/nightlife), Bay Area (theme parks/aquarium).
- Use Kansai-ben greetings sparingly (e.g., "Maido!" for hello, "Okini!" for thanks) to sound local.
- ONLY use the provided context. If the answer isn't in the context, say: "I don't have verified info on that yet, but I can help you explore similar spots!"
- Always include practical tips (hours, transit, booking, cost range) when available.
"""

def get_context_for_query(user_query):
    """Simple keyword matching to find relevant data"""
    query_lower = user_query.lower()
    relevant_items = []
    
    for item in osaka_data:
        # Check if query keywords match item properties
        text_to_search = f"{item.get('name', '')} {item.get('description', '')} {item.get('category', '')} {' '.join(item.get('tags', []))}".lower()
        if any(word in text_to_search for word in query_lower.split() if len(word) > 3):
            relevant_items.append(item)
    
    # If no matches, return all items as fallback
    return relevant_items if relevant_items else osaka_data[:3]

def get_response(user_query):
    context_items = get_context_for_query(user_query)
    
    # Format context for the LLM
    context = "\n\n".join([
        f"Name: {item['name']}\nCategory: {item['category']}\nLocation: {item['area']}\nDescription: {item['description']}\nTags: {', '.join(item['highlights'])}"
        for item in context_items
    ])
    
    prompt = f"""
[OSAKA KNOWLEDGE BASE]
{context}

[USER QUESTION]
{user_query}

[ANSWER]
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content

# 4. STREAMLIT CHAT UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Osaka restaurants, events, transit, or tips..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Checking local Osaka guide..."):
            reply = get_response(prompt)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})