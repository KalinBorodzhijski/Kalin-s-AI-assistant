import streamlit as st
import openai
import config

models_info = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo is a AI model provided by OpenAI. This model strikes a balance between affordability and performance, capable of generating coherent and contextually relevant text based on the input.",
    "gpt-4": "The Standard GPT-4 model. This is the base model of GPT-4, known for its ability to generate detailed and coherent text.",
    #"LLAMA2": "Locally trained advanced AI model for generating high-quality text."
}

def show_chatbot_sidebar():
    st.sidebar.title("Chat Bot Settings")
    # Dropdown for selecting the model
    selected_model = st.sidebar.selectbox("#### Select Model", list(models_info.keys()))

    st.sidebar.markdown(f"**Model Description:** {models_info[selected_model]}")

    st.sidebar.markdown("#### Temperature")
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    st.sidebar.markdown("Set the 'temperature' of the model responses. Higher values will produce more creative and unpredictable responses, whereas lower values will produce more conservative and predictable responses.")

    return selected_model, temperature

def show_chatbot_tab():
    selected_model, temperature = show_chatbot_sidebar()
    
    st.title("Chat Bot")

    st.session_state["openai_model"] = selected_model

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = openai.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                max_tokens=config.MAX_TOKENS,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})