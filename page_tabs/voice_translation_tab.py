import streamlit as st
import openai
import io
from st_audiorec import st_audiorec
import tempfile


def show_voice_translation_sidebar():
    st.sidebar.title("Voice Translation Settings")
    translate_to_english = st.sidebar.checkbox("Translate to English", help="Translate the audio to English instead of transcribing it.")
    
    languages = {
        "Afrikaans": "af", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az", "Belarusian": "be",
        "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca", "Chinese": "zh", "Croatian": "hr",
        "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en", "Estonian": "et",
        "Finnish": "fi", "French": "fr", "Galician": "gl", "German": "de", "Greek": "el",
        "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
        "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Kazakh": "kk", "Korean": "ko",
        "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms", "Marathi": "mr",
        "Maori": "mi", "Nepali": "ne", "Norwegian": "no", "Persian": "fa", "Polish": "pl",
        "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Serbian": "sr", "Slovak": "sk",
        "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl",
        "Tamil": "ta", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
        "Vietnamese": "vi", "Welsh": "cy"
    }

    if not translate_to_english:
        selected_language_name = st.sidebar.selectbox("#### Select Language for Transcription", options=list(languages.keys()), index=list(languages.keys()).index('English'))
        language = languages[selected_language_name]
    else:
        language = None
    return translate_to_english, language

def process_audio(audio_data, translate_to_english, language=None):
    """
    Processes the audio data by either transcribing or translating it.
    
    :param audio_data: The audio data to process.
    :param translate_to_english: Determines whether to translate to English or transcribe.
    :param language: The language for transcription (ISO-639-1 format).
    :return: The processed text.
    """
    if translate_to_english:
        response = openai.audio.translations.create(
            model="whisper-1",
            file=audio_data
        )
    else:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_data,
            language=language
        )
    
    return response.text

def show_voice_translator_tab():
    translate_to_english, language = show_voice_translation_sidebar()
    st.title("Voice Translator")
    st.markdown("In this page you can either record audio or upload audio files. After processing, the AI model will provide the transcribed text of the audio file or translate the audio to English, based on your selected option.")


    st.markdown("## Upload or Record Your Audio")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Record Audio")
        st.info("Click the button to start recording")
        wav_audio_data = st_audiorec()
    
    with col2:
        st.markdown("#### Upload Audio File")
        
        st.info("Drag and drop or browse files to select the audio file for Transcription/Translation")
        uploaded_audio = st.file_uploader("hidden", type=['mp3', 'wav', 'mpeg'], key="file_uploader", label_visibility='collapsed')

    process_button = st.button("Process Audio")

    
    if process_button:
        if uploaded_audio is not None or wav_audio_data is not None:
            if uploaded_audio:
                audio_file = uploaded_audio
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                    tmpfile.write(wav_audio_data)
                    tmpfile_path = tmpfile.name
                audio_file = open(tmpfile_path, "rb")

            result_text = process_audio(audio_file, translate_to_english, language)
            
            st.markdown("## Transcription/Translation Result")
            st.text_area("hidden", value=result_text, height=150, help="The transcribed or translated text will appear here.", key="result_textarea", label_visibility='collapsed')

            if not uploaded_audio:
                audio_file.close()
        else:
            st.warning("Please upload or record an audio file before processing.")