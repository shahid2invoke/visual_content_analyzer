import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
import base64

# Load Google AI Gemini API key
#GOOGLE_API_KEY = "AIzaSyDxF8JJJWGA-oml8qxdEhkvDRfQisNdsOs"  #AIzaSyDxF8JJJWGA-oml8qxdEhkvDRfQisNdsOs
#GOOGLE_API_KEY = 
with open('api_key.txt', 'r') as f:
      GOOGLE_API_KEY = f.read().strip()
if GOOGLE_API_KEY is None:
    st.error("Please set your GOOGLE_API_KEY environment variable")
    st.stop()
else:
    genai.configure(api_key=GOOGLE_API_KEY)


def analyze_image_or_video(uploaded_file, prompt):
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")#gemini-1.5-flash / gemini-pro-vision

        # Check file type
        if uploaded_file.type.startswith("image"):
            image_data = uploaded_file.read()
            image = Image.open(io.BytesIO(image_data))
            st.image(image)
            response = model.generate_content([prompt, image], stream=True)
        elif uploaded_file.type.startswith("video"):
            # Handle video (basic example; processing videos with Gemini is more involved)
            video_data = uploaded_file.read()
            st.video(video_data)
            # For simplicity, we're not processing the video frames, but just send the whole file to the AI. 
            # This may not work with all prompts, videos and API configurations
            response = model.generate_content([prompt, video_data], stream=True)
        else:
            return "Unsupported file type. Please upload a photo or a video."
        
        response.resolve()
        return response.text
    except Exception as e:
         return f"Error during analysis: {str(e)}"


def main():
    st.title("Visual advertisement analyzer")

    uploaded_file = st.file_uploader(
        "Upload an image or video", type=["png", "jpg", "jpeg", "mp4"]
    )
    #prompt = st.text_area("Enter your prompt for Google AI")
    prompt = "the good and bad of this image base on advertisement perspective in term of color, style, text and sentiment"

    if uploaded_file and prompt:
        if st.button("Analyze"):
            st.spinner("Analyzing with Google AI ...")
            response = analyze_image_or_video(uploaded_file, prompt)
            st.subheader("Analysis Results:")
            st.write(response)


if __name__ == "__main__":
    main()