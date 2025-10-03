import streamlit as st
import requests
import uuid


# --- Configuration ---
WEBHOOK_URL =   st.secrets["url"]
# WEBHOOK_URL ="http://localhost:5678/webhook-test/invoke_agent"
BEARER_TOKEN = st.secrets["token"]
LOGO_PATH = "logo.jpg"  # local file or URL


# --- Session state ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Page setup ---
st.set_page_config(page_title="n8n Agent Chat", page_icon="🤖")

# --- Sticky logo in sidebar ---
with st.sidebar:
    st.image(LOGO_PATH, width=120)
    

# --- Main Header ---
st.title("💬 Chat with my AI Bot ~MohsinF.")

# --- Display chat history ---
for role, text in st.session_state["messages"]:
    with st.chat_message(role):
        st.markdown(text)

# --- Chat input ---
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state["messages"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "sessionId": st.session_state["session_id"],
        "chatInput": prompt
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    # Loader while waiting
    with st.spinner("✨ Agent is preparing a response..."):
        try:
            response = requests.post(WEBHOOK_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            agent_reply = data.get("output", "⚠️ No response from agent.")
        except Exception as e:
            agent_reply = f"⚠️ Error: {e}"

    # Add agent reply
    st.session_state["messages"].append(("agent", agent_reply))
    with st.chat_message("agent"):
        st.markdown(agent_reply)
