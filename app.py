import streamlit as st
from rag_logic import ask_resume

# --- PAGE SETUP ---
st.set_page_config(page_title="Sania's AI Resume", page_icon="🤖", layout="centered")

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background styling */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Profile Header Section with Glassmorphism */
    .profile-container {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 2rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    .profile-info h1 {
        margin: 0;
        font-size: 2.4rem;
        color: #0f172a;
        font-weight: 600;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .profile-info p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        color: #475569;
        font-weight: 400;
        line-height: 1.5;
    }
    
    /* Input area styling */
    .stChatInput {
        border-radius: 15px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05) !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {
        .profile-container {
            flex-direction: column;
            text-align: center;
            padding: 1.5rem;
        }
        .profile-info h1 {
            font-size: 1.8rem;
        }
    }
</style>

<div class="profile-container">
    <div class="profile-info">
        <h1>🤖 Chat with Sania's Resume</h1>
        <p>Welcome! I am an AI assistant trained exclusively on Sania's resume. Ask me anything about her skills, experience, or projects!</p>
    </div>
</div>
""", unsafe_allow_html=True)

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
