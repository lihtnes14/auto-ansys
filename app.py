import streamlit as st
import openai
import base64
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key (Set this as an environment variable for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text.strip()

def process_fbd_image(image_file):
    """Uses OpenAI GPT-4 Vision to analyze an FBD image from an uploaded file."""
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    vision_response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Extract forces, dimensions, and constraints from this Free Body Diagram (FBD)."},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this FBD and describe its contents."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=500
    )
    return vision_response["choices"][0]["message"]["content"]

def generate_apdl_script(problem_text, fbd_data):
    """Generates an ANSYS APDL script based on extracted problem description and FBD data."""
    prompt = f"""
    Based on the following problem description and Free Body Diagram (FBD) data, generate an ANSYS APDL script, the response shouldn't contain any other text expect the code and don't add ``` ``` :
    
    Problem Description:
    {problem_text}
    
    FBD Data (Extracted from image):
    {fbd_data}
    
    The ANSYS APDL script should include:
    - Material properties
    - Nodes and elements
    - Boundary conditions
    - Forces or loads
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("FBD Analyzer & APDL Script Generator")
st.write("Upload a PDF with the problem statement and an image of the Free Body Diagram (FBD).")

pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
image_file = st.file_uploader("Upload FBD Image", type=["jpg", "jpeg", "png"])

# Track process state using session_state
if "process_done" not in st.session_state:
    st.session_state.process_done = False

if pdf_file and image_file and not st.session_state.process_done:
    with st.spinner("Extracting text from PDF..."):
        problem_text = extract_text_from_pdf(pdf_file)
        st.text_area("Extracted Problem Description", problem_text, height=200)
    
    with st.spinner("Analyzing FBD image..."):
        fbd_data = process_fbd_image(image_file)
    
    with st.spinner("Generating APDL script..."):
        apdl_script = generate_apdl_script(problem_text, fbd_data)

    # Set session state to prevent rerunning the process
    st.session_state.process_done = True

    # Allow user to download the APDL script
    st.download_button(
        label="Download APDL Script",
        data=apdl_script,
        file_name="generated_apdl_script.inp",
        mime="text/plain"
    )

# If process is done, inform the user
if st.session_state.process_done:
    st.success("APDL Script generated and ready for download!")
    st.write("You can download the script from the button above.")
