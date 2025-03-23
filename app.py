import streamlit as st
import os
from Farsi_audio_to_English_transcript import (
    download_youtube_audio,
    transcribe_farsi,
    translate_farsi_to_english,
    generate_english_audio_gpt4o,
    extract_video_id
)
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Set page config
st.set_page_config(
    page_title="Farsi Whisperer",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS for dark brown background and button styling
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #3c2a21 !important;
        color: white !important;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        margin: 5px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2a1c16 !important;
    }
    .stButton>button:disabled {
        background-color: #cccccc;
    }
    .stTextInput>div>div>input {
        background-color: white;
        color: black;
        font-size: 16px;
    }
    .stTextArea>div>div>textarea {
        background-color: white;
        color: black;
        font-size: 16px;
    }
    .stMarkdown {
        color: white;
        font-size: 16px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stSuccess {
        color: white;
        font-size: 16px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stError {
        color: white;
        font-size: 16px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stWarning {
        color: white;
        font-size: 16px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stInfo {
        color: white;
        font-size: 16px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stExpander {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stSpinner {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .stColumns {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    h1 {
        font-size: 2.5em !important;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    h2 {
        font-size: 2em !important;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    h3 {
        font-size: 1.5em !important;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .persian-text {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }
    .english-text {
        direction: ltr;
        text-align: left;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }
    .output-section {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .title-section {
        background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid #333;
    }
    .title-text {
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 10px 0;
    }
    .feature-list {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None
if 'farsi_text' not in st.session_state:
    st.session_state.farsi_text = None
if 'english_text' not in st.session_state:
    st.session_state.english_text = None
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'summary_text' not in st.session_state:
    st.session_state.summary_text = None

# Title and description
st.markdown("""
    <div class='title-section'>
        <p class='title-text' style='font-size: 32px; font-weight: bold; text-align: center;'>🤖 Ali AI Agent</p>
        <p class='title-text' style='font-size: 24px; text-align: center;'>Advanced AI-Powered Persian-English Processing System</p>
        <div class='feature-list'>
            <p style='font-size: 20px; margin: 10px 0;'>✨ Advanced Features:</p>
            <ul style='font-size: 18px; margin: 10px 0;'>
                <li>🎵 High-Quality Audio Processing & Enhancement</li>
                <li>🗣️ Advanced Persian Speech Recognition with Quality Checks</li>
                <li>🌍 Context-Aware Persian to English Translation</li>
                <li>🔊 Natural English Audio Generation</li>
                <li>📝 Intelligent Content Summarization</li>
                <li>⚡ Real-time Processing with Quality Control</li>
                <li>🎯 Customizable Processing Options</li>
            </ul>
        </div>
        <p class='title-text' style='font-size: 20px; text-align: center; margin-top: 20px;'>Made with ❤️ by Ali</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### Your AI Conversation Assistant that:
- 🎵 Records and downloads Persian conversations from YouTube
- 🗣️ Transcribes Persian speech to text with high accuracy
- 🌍 Translates Persian to English with natural flow
- 🔊 Creates clear English audio of the translation
- 📝 Generates concise English summaries of key points
""")

# URL input with default value
default_url = "https://www.youtube.com/watch?v=56WsSzrx98A"
url = st.text_input("Enter YouTube URL:", value=default_url, placeholder="https://www.youtube.com/watch?v=...")

# Quality check toggle
quality_check = st.checkbox("Enable Quality Checks", value=True, help="Enable this to perform quality checks and improvements on transcription and translation. Disable for faster processing.")

# Process button
if st.button("🚀 Process Everything!", disabled=not url):
    try:
        with st.spinner("🎵 Downloading audio..."):
            video_id = extract_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL")
            else:
                st.session_state.video_id = str(video_id)
                audio_file = f"{str(video_id)}.mp3"
                download_youtube_audio(url, audio_file)
                st.session_state.audio_file = audio_file
                st.success("✅ Audio downloaded!")
        
        with st.spinner("🗣️ Transcribing to Farsi..."):
            farsi_text = transcribe_farsi(st.session_state.audio_file, quality_check=quality_check)
            st.session_state.farsi_text = farsi_text
            st.success("✅ Transcription completed!")
        
        with st.spinner("🌍 Translating to English..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator specializing in Persian to English translation. Your goal is to produce natural, fluent English that maintains the original meaning while being easy to read and understand. Follow these guidelines:\n1. Use natural English expressions and idioms where appropriate\n2. Maintain the original tone and style\n3. Ensure the translation flows smoothly\n4. Break long sentences into shorter, clearer ones if needed\n5. Preserve any cultural references or specific terminology"
                    },
                    {
                        "role": "user",
                        "content": farsi_text
                    }
                ]
            )
            english_text = response.choices[0].message.content
            st.session_state.english_text = english_text
            st.success("✅ Translation completed!")
        
        with st.spinner("🔊 Generating English audio..."):
            english_audio_file = f"{str(video_id)}_english.wav"
            generate_english_audio_gpt4o(st.session_state.english_text, english_audio_file)
            st.success("✅ English audio generated!")
        
        with st.spinner("📝 Creating summary..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Create a clear, concise summary of the following text. Format your response exactly as follows, with each bullet point on its own line using markdown formatting:\n\n**Key Points:**\n\n* First main point\n\n* Second main point\n\n* Third main point\n\n**Key Takeaways:**\n\n* First takeaway\n\n* Second takeaway\n\n* Third takeaway\n\nMake sure each point is specific, actionable, and clearly stated. Each bullet point must be on its own line with a blank line before and after it."
                    },
                    {
                        "role": "user",
                        "content": st.session_state.english_text
                    }
                ]
            )
            summary_text = response.choices[0].message.content
            st.session_state.summary_text = summary_text
            st.success("✅ Summary generated!")
            
            # Save summary to file
            summary_file = f"{str(video_id)}_summary.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary_text)
            
            # Generate summary audio
            summary_audio_file = f"{str(video_id)}_summary.wav"
            generate_english_audio_gpt4o(summary_text, summary_audio_file)
            st.success("✅ Summary audio generated!")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display results in organized sections
st.markdown("## 📝 Results")

# Audio Section
st.markdown("### 🎵 Audio")
col1, col2 = st.columns(2)
with col1:
    if st.session_state.audio_file:
        st.audio(st.session_state.audio_file, format='audio/mp3')
        st.markdown("**Original Farsi Audio**")
with col2:
    if st.session_state.video_id:
        english_audio_file = f"{st.session_state.video_id}_english.wav"
        if os.path.exists(english_audio_file):
            st.audio(english_audio_file, format='audio/wav')
            st.markdown("**English Translation Audio**")

# Farsi Transcription Section
st.markdown("### 🗣️ Farsi Transcription")
if st.session_state.farsi_text:
    st.text_area("Farsi Text", st.session_state.farsi_text, height=200, disabled=True)
else:
    st.info("Farsi transcription will appear here after processing")

# English Translation Section
st.markdown("### 🌍 English Translation")
if st.session_state.english_text:
    st.text_area("English Text", st.session_state.english_text, height=200, disabled=True)
else:
    st.info("English translation will appear here after processing")

# Summary Section
st.markdown("### 📝 Summary")
if st.session_state.summary_text:
    st.markdown(st.session_state.summary_text)
else:
    st.info("Summary will appear here after processing")

# Add a clear button to reset the session
if st.button("🗑️ Clear All"):
    st.session_state.audio_file = None
    st.session_state.farsi_text = None
    st.session_state.english_text = None
    st.session_state.video_id = None
    st.session_state.summary_text = None
    st.experimental_rerun()

# Footer
st.markdown("""
    <div style='text-align: center; background-color: white; padding: 20px; border-radius: 10px; margin: 10px 0;'>
        <p style='color: black; font-size: 16px; margin: 5px 0;'>Made with ❤️ by Ali</p>
        <p style='color: black; font-size: 14px; margin: 5px 0;'>Powered by OpenAI GPT-4 and Whisper</p>
    </div>
""", unsafe_allow_html=True)