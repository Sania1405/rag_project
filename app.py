import streamlit as st
from rag_logic import ask_resume

# --- PAGE SETUP ---
st.set_page_config(page_title="Sania's AI Resume", page_icon="🤖", layout="centered")

st.title("🤖 Chat with Sania's Resume")
st.markdown("Welcome! I am an AI assistant trained exclusively on Sania's resume. Ask me anything about her skills, experience, or projects!")

# --- INITIALIZE CHAT MEMORY ---
# Streamlit reruns the whole script every time a button is clicked.
# session_state allows us to keep data (like chat history) saved between reruns!
if "messages" not in st.session_state:  #comp checks memory as it is brand new session, finds nothing
    st.session_state.messages = []    #creates empty list

# --- DISPLAY CHAT HISTORY ---
# Draw all past messages to the screen
for message in st.session_state.messages: #loop thorugh older chats
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE NEW USER INPUT ---
user_question = st.chat_input("Ask about Python, projects, or education...")

if user_question:
    # 1. Display user's question on the screen
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # 2. Add user's question to our session state memory
    st.session_state.messages.append({"role": "user", "content": user_question})

    # 3. Build the chat_history string to send to Gemini
    # We convert our list of dictionaries into a single text string
    history_string = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_string += f"{role}: {msg['content']}\n"

    # 4. Get the AI's response using our backend logic
    with st.chat_message("assistant"):
        with st.spinner("Searching resume..."):
            ai_response = ask_resume(user_question, history_string)
            st.markdown(ai_response)
    
    # 5. Add AI's response to our session state memory
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
