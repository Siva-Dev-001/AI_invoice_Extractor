from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_bytes 

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))

#Function to load Gemini Pro
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    print(type(image))
    
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with open(uploaded_file, "rb") as f:
                pdf_bytes = f.read()
            return pdf_bytes
            # Convert PDF to images
            # images = convert_from_bytes(uploaded_file.read())
            # image_parts = [{"mime_type": "image/jpeg", "data": image.tobytes()} for image in images]
            #return image_parts
        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            # Read image data
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
        else:
            raise ValueError("Unsupported file format")
    else:
        raise FileNotFoundError("No file uploaded")
    
#initialize our streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini LLM based Invoice Extrator")
input = st.text_input("Input prompt :",key="input")
uploaded_file = st.file_uploader("Choose an image/ pdf file",type=["jpg","jpeg","png","pdf"])
image = ""

if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image...",use_column_width=True)
    submit = st.button("Tell me about the invoice")
    input_prompt = """
    You are an expert in understanding invoices. We will upload an image as invoice and You will have to answer any questions based on the uploaded image.
                    """
    # if submit button is clicked
    if submit:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt,image_data,input)
        st.subheader("The Response is : ")
        st.write(response)
