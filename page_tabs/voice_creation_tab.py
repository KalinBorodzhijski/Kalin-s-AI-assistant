import streamlit as st
import openai
from pathlib import Path
import tempfile
import numpy as np
import io

def show_voice_creation_sidebar():
    st.sidebar.title("Voice Creation Settings")
    
    # Model selection
    model_options = {'standard': 'tts-1', 'hd': 'tts-1-hd'}
    model_choice = st.sidebar.radio("#### Choose Model Quality", options=list(model_options.keys()))
    
    # Voice selection
    voice_options = ['Alloy', 'Echo', 'Fable', 'Onyx', 'Nova', 'Shimmer']
    voice_choice = st.sidebar.selectbox("#### Select Voice", options=voice_options)
    
    # Speed selection
    speed = st.sidebar.slider("#### Select Speed", min_value=0.25, max_value=4.0, value=1.0, step=0.1)
    
    return model_options[model_choice], voice_choice.lower(), speed

def show_voice_creation_tab():
    model, voice, speed = show_voice_creation_sidebar()
    st.title("Voice Creation")
    st.markdown("Enter text below to synthesize it into speech. Customize the voice and playback speed using the sidebar settings.")

    user_text = st.text_area("test", value="", height=150, max_chars=500, placeholder="Enter text here...", label_visibility='collapsed')
    if st.button("Generate Voice"):
        if user_text:
            audio_file_path = synthesize_speech(user_text, model, voice, speed)
            with open(audio_file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/ogg')
        else:
            st.warning("Please enter some text to synthesize.")

    with st.expander("VOICE DEMOS"):
        col1, col2, col3 = st.columns(3)
        with col1:
            for voice in ['Alloy', 'Echo']:
                st.markdown(f"**{voice}**")
                with open(f"./resources/voice_creation/demo_voices/{voice}_demo.mp3", "rb") as demo_file:
                    demo_audio = demo_file.read()
                st.audio(demo_audio, format="audio/mp3")
        with col2:
            for voice in ['Fable', 'Onyx']:
                st.markdown(f"**{voice}**")
                with open(f"./resources/voice_creation/demo_voices/{voice}_demo.mp3", "rb") as demo_file:
                    demo_audio = demo_file.read()
                st.audio(demo_audio, format="audio/mp3")
        with col3:
            for voice in ['Nova', 'Shimmer']:
                st.markdown(f"**{voice}**")
                with open(f"./resources/voice_creation/demo_voices/{voice}_demo.mp3", "rb") as demo_file:
                    demo_audio = demo_file.read()
                st.audio(demo_audio, format="audio/mp3")


def synthesize_speech(text, model, voice, speed):
    """
    Calls the OpenAI API to generate speech from text.
    :param text: Text to synthesize.
    :param model: TTS model to use ('tts-1' or 'tts-1-hd').
    :param voice: Voice to use for speech synthesis.
    :param speed: Speed of the generated audio.
    :return: Path to the generated MP3 file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        speech_file_path = Path(tmpfile.name)

    with openai.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text,
        speed=speed
    ) as response:
        response.stream_to_file(str(speech_file_path))

    return speech_file_path
