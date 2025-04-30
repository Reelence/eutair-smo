# File: main.py

import streamlit as st
import datetime
import requests
import os

st.set_page_config(page_title="Eutair SMO Automation", layout="centered")

st.title("📣 Eutair Social Media Automation MVP")

# --- Load Hugging Face Token from Streamlit Secrets ---
hf_token = st.secrets["hf_token"]
headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# --- Input: Requirement ---
st.subheader("Step 1: Enter Your Requirement")
requirement = st.text_input("What do you want to post about?", placeholder="e.g. Promote Eutair’s energy-efficient compressor")

# --- Content Generation ---
st.subheader("Step 2: Generate AI Content")
if st.button("Generate AI Content"):
    if requirement:
        with st.spinner("Generating content using Mistral AI..."):
            try:
                payload = {
                    "inputs": f"You are a creative social media content writer for an industrial compressor company. Create a catchy LinkedIn/Instagram post about: {requirement}. Include a caption and relevant hashtags."
                }
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    ai_text = result[0]['generated_text'] if isinstance(result, list) else result.get("generated_text", "")
                    st.success("✅ AI Content Generated")
                    st.markdown(ai_text)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error generating content: {e}")
    else:
        st.warning("Please enter a requirement first.")

# --- Media Upload / Image Creation Placeholder ---
st.subheader("Step 3: Upload Product Image")
image_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if image_file:
    st.image(image_file, caption="Uploaded Image", use_column_width=True)

# --- Posting Placeholder ---
st.subheader("Step 4: Schedule or Post Manually")
schedule = st.checkbox("Schedule this post?")
if schedule:
    date = st.date_input("Pick a date", min_value=datetime.date.today())
    time = st.time_input("Pick a time", value=datetime.time(10, 0))
    st.success(f"Post scheduled for {date} at {time}")
else:
    st.button("Download Media for Manual Posting")

# --- Stats & Suggestions Placeholder ---
st.subheader("Step 5: Insights (Mock Data)")
st.metric(label="Post Likes", value="1,200")
st.metric(label="Shares", value="300")
st.metric(label="Comments", value="150")

st.markdown("**AI Recommendation:** Try using short videos showcasing real-time usage of compressors to increase engagement on Instagram.")

st.info("✅ This MVP now uses Mistral via Hugging Face to generate captions and hashtags. Posting and analytics integrations are coming next!")
