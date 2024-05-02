import streamlit as st

def show_video_generator_sidebar():
    st.sidebar.title("Video Generator Settings")


def show_video_generator_tab():
    show_video_generator_sidebar()
    st.title("Video Generation")
    st.warning(f"This page is under development !")