import streamlit as st
import google.generativeai as genai
import base64
from typing import List

# Configure Google Generative AI API
genai.configure(api_key="YOUR_GOOGLE_API_KEY")  # Replace with your actual API key

def extract_text_from_image(image_content: bytes) -> str:
    """Extracts text from an image using Gemini Pro Vision."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    img_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(image_content).decode()}]
    prompt_parts = [
        img_parts[0],
        "\n\nExtract all the text from this image and return it as plain text."
    ]

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        st.error(f"Error during image text extraction: {e} 😢")
        return None

def general_image_query(image_contents: List[bytes], query: str) -> str:
    """Handles general queries about the images."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_parts = []
    for image_content in image_contents:
        img_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(image_content).decode()}]
        prompt_parts.append(img_parts[0])
    prompt_parts.append(f"\n\n{query}")

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        st.error(f"Error processing query: {e} 😞")
        return "An error occurred while processing your query. 🤖"

def main():
    st.set_page_config(page_title="Image Chatbot 🖼️", layout="wide")
    st.title("Image Chatbot 🤖🖼️")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "image_contents" not in st.session_state:
        st.session_state.image_contents = []

    uploaded_files = st.file_uploader("Upload images 📸", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            image_content = uploaded_file.read()
            st.session_state.image_contents.append(image_content)
            st.image(image_content, caption=uploaded_file.name, use_column_width=True)

    query = st.text_input("Ask a question about the images: 💬")

    if query:
        response_text = general_image_query(st.session_state.image_contents, query)
        st.session_state.chat_history.append({"user": query, "bot": response_text})

    # Display chat history
    st.subheader("Chat History 📜")
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['user']} 🧑‍💻")
        st.markdown(f"**Bot:** {chat['bot']} 🤖")
        st.markdown("---")  # Separator

if __name__ == "__main__":
    main()