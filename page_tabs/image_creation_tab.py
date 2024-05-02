import streamlit as st
import openai
from PIL import Image
import io
import requests
from base64 import b64encode
import uuid

#----------------------------------------------------------------------------------------------------------------------------------
def show_image_creation_sidebar():
    st.sidebar.title("Image Creation Settings")
    creation_option = st.sidebar.radio("Choose an option:", ["Create New Image", "Create Image Variation"], captions=[ "Select this option to create a completely new image.","Select this option to create a variation of an existing image."])

    size = None

    if creation_option == "Create New Image":
        model = st.sidebar.selectbox("Select Model", ["dall-e-2", "dall-e-3"], index=1,
                                     format_func=lambda x: f"{x.upper()} - {'High quality and variations' if x == 'dall-e-2' else 'Latest with HD option'}")
        
        if model == "dall-e-3":
            size_options = ["1024x1024", "1024x1792", "1792x1024"]
            size = st.sidebar.selectbox("Select Image Size", size_options, index=0)
            quality = st.sidebar.radio("Select Image Quality", ["standard", "hd"], index=0)
        else:
            quality = "standard"
    else:
        model, quality = None, None  # These options are not applicable for image variations
        # Size options for image variation
        size_options = ['256x256', '512x512', '1024x1024']
        size = st.sidebar.selectbox("Select Image Size", size_options, index=0)

    return creation_option, size, model, quality

#----------------------------------------------------------------------------------------------------------------------------------
def fetch_and_save_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image = Image.open(response.raw)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Failed to fetch the image: {e}")
        return None
#----------------------------------------------------------------------------------------------------------------------------------
def display_and_download_image(image_url):
    # Use image URL as the key to store and check if it's already fetched
    if image_url not in st.session_state:
        # Fetch image data if not already in session state
        image_data = fetch_and_save_image(image_url)
        if image_data:
            st.session_state[image_url] = image_data
        else:
            st.error("Failed to load image.")
            return

    image_data = st.session_state[image_url]

    # Display the image
    display_image_preview(image_data, width=500, height=500)

    # Create a download button
    st.download_button(
        label="Download Image",
        data=image_data,
        file_name="generated_image.png",
        mime="image/png"
    )
#----------------------------------------------------------------------------------------------------------------------------------
def display_image_preview(image_data, width=100, height=100):
    
    # Convert image data to base64 to embed in HTML
    base64_image = b64encode(image_data).decode("utf-8")
    image_html = f"""
    <style>
        .image-preview-wrapper {{
            width: {width}px;
            height: {height}px;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .image-preview-wrapper img {{
            max-width: 100%;
            max-height: 100%;
        }}
    </style>
    <div class="image-preview-wrapper">
        <img src="data:image/png;base64,{base64_image}" alt="Generated Image">
    </div>
    """

    st.markdown(image_html, unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------------------
def show_image_creation_tab():
    creation_option, size, model, quality = show_image_creation_sidebar()
    st.title("Image Creation")

    if creation_option == "Create New Image":
        prompt = st.text_input("Enter a prompt for the image", "")
        if model == "dall-e-3" or model == "dall-e-2":  # Check for model selection
            action_button = st.button("Generate Image")

            if action_button and prompt:
                if model == "dall-e-3":
                    # Only pass size for DALL·E 3 as it's relevant
                    generate_and_display_image(model, prompt, size, quality)
                else:
                    # For DALL·E 2, size isn't used
                    generate_and_display_image(model, prompt, None, quality)

    elif creation_option == "Create Image Variation":
        uploaded_photo = st.file_uploader("Upload a photo for image variation", type=["png"], )
        if uploaded_photo is not None:
            action_button = st.button("Create Variation")

            if action_button:
                # Size is relevant for variations
                create_and_display_variation(uploaded_photo, size)
#----------------------------------------------------------------------------------------------------------------------------------
def generate_and_display_image(model, prompt, size, quality):
    try:
        # Generate image from prompt using the specified model, size, and quality
        if size:
            response = openai.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
        else:
            response = openai.images.generate(
                model=model,
                prompt=prompt,
                n=1,
            )
        # Check if images were returned in the response
        if response.data:
            for index, image_data in enumerate(response.data):
                session_key = f"image_{uuid.uuid4()}"
                # Function to display the image and provide a download link
                display_and_download_image(image_data.url)
        else:
            st.error("No images were returned.")
    except Exception as e:
        st.error(f"Failed to generate image: {str(e)}")
#----------------------------------------------------------------------------------------------------------------------------------
def create_and_display_variation(uploaded_photo, size):
    try:
        # Convert the uploaded file to bytes for the API call
        bytes_data = uploaded_photo.getvalue()
        # Create image variation using the specified model and size
        response = openai.images.create_variation(
            image=bytes_data,
            n=1,
            size=size
        )
        # Check if variations were returned in the response
        if response.data:
            for index, image_data in enumerate(response.data):
                session_key = f"variation_{uuid.uuid4()}"
                # Function to display the image variation and provide a download link
                display_and_download_image(image_data.url)
        else:
            st.error("No variations were generated.")
    except Exception as e:
        st.error(f"Failed to create image variation: {str(e)}")

