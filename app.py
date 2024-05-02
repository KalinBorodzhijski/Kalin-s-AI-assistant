import streamlit as st

from page_tabs.chatbot_tab import show_chatbot_tab
from page_tabs.image_creation_tab import show_image_creation_tab
from page_tabs.video_generator_tab import show_video_generator_tab
from page_tabs.voice_creation_tab import show_voice_creation_tab
from page_tabs.voice_translation_tab import show_voice_translator_tab

import streamlit.config as _config

st.set_page_config(page_title="Kalin's GPT", layout="wide")
_config.set_option('server.maxUploadSize', 25)

def show_home_page():
    # Use columns to center content. Adjust '1' values to control spacing further if needed.
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        cola, colb, colc = st.columns([0.75, 2.5, 1.25])
        with colb:
            st.image("resources/logo.png", width=600)
        # Center-aligned title
        st.markdown("<h1 style='text-align: center;'>Welcome to Kalin's GPT 🚀</h1>", unsafe_allow_html=True)
        
        # Center-aligned markdown text
        st.markdown("""
            <div style="text-align: center;">
                ✨ Kalin's GPT is your go-to suite for cutting-edge AI features, designed to empower your creative and analytical endeavors. Dive into our offerings:
            </div>
            """, unsafe_allow_html=True)
        
        # Features list
        st.markdown("""
            - **Chat Bot** 🤖: Engage with our AI conversational agent.
            - **Image Creation** 🎨: Bring your ideas to life with AI-generated images.
            - **Voice Creation** 🎙️: Create realistic voices from text.
            - **Voice Translation** 🌍: Break language barriers in real-time. Transcribe and translate audio files effortlessly.
            - **Video Generator** 📹: Generate videos from simple descriptions.
            """)


# Sidebar setup with navigation info
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the selector below to navigate through the features of Kalin's GPT.")

# Sidebar for navigation
page = st.sidebar.selectbox("test", ["Home", "Chat Bot", "Image Creation", "Voice Creation", "Voice Translation", "Video Generator"], label_visibility="collapsed")
st.sidebar.markdown("---")

if page == "Home":
    show_home_page()
elif page == "Chat Bot":
    show_chatbot_tab()
elif page == "Image Creation":
    show_image_creation_tab()
elif page == "Voice Creation":
    show_voice_creation_tab()
elif page == "Voice Translation":
    show_voice_translator_tab()
elif page == "Video Generator":
    show_video_generator_tab()