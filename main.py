import streamlit as st
import requests
import os

st.set_page_config(page_title="Zero Click Chatbot", layout="centered")

st.title("🚀 Zero-Click Groq Chatbot Deployment")

st.markdown("Spin up your own LLaMA-based chatbot hosted on Vultr.")

# Input form
bot_name = st.text_input("🤖 Enter Bot Name", placeholder="e.g., Python Tutor")

if st.button("🚀 Deploy Bot"):
    if not bot_name.strip():
        st.warning("Please enter a bot name.")
    else:
        with st.spinner("Deploying bot... Please wait a second"):
            try:
                response = requests.post(
                    "http://45.77.65.122:8000/deploy",  # Replace with backend deployment API
                    json={"bot_name": bot_name}
                )
                if response.status_code == 200:
                    bot_url = response.json().get("url")
                    st.success(f"Bot deployed successfully! [Chat now]({bot_url})")
                else:
                    st.error(f"Deployment failed: {response.text}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
