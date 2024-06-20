from dotenv import load_dotenv
import streamlit as st
import os
from langchain_groq import ChatGroq
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
               "mime_type":uploaded_file.type,
               "data":bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")


st.set_page_config(page_title='Query.jpg')
st.header("Query.jpg 🖼️🔍")

uploaded_file=st.file_uploader("Upload an image : ",type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uplaoded Image.", use_column_width=True)

input=st.text_input("What would you like to know about the image: ",key='input')
submit=st.button("Submit")

input_prompt="""
You are an expert in understanding every type of image .we will upload an image of anything 
and you will be asked any question regarding the details that the image contain,
you have to answer those questions. """

if submit:
    image_data= input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.write(response)
