from IPython.core.page import page
import streamlit as st
st.set_page_config(page_title="heloo",layout="centered")
st.title("sania here")
st.markdown("hi thanks for connecting to sania")
st.chat_input("how r u ?")
st.chat_message("user")
st.chat_message("AI")  #symbols
with st.chat_message("assistant"):
        with st.spinner("Searching resume..."):
            st.markdown("im final amswer")