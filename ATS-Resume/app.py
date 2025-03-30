import streamlit as st
import google.generativeai as genai
import os
import json
import requests
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import time

# ✅ Move this to the first Streamlit command
st.set_page_config(page_title="ATS Resume Pro", layout="wide")

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ API Key NOT Found! Check your .env file or set the API key manually.")
    st.stop()

# ✅ Configure Gemini API
genai.configure(api_key=api_key)

# ✅ List available models
try:
    models = [model.name for model in genai.list_models()]
    print("✅ Available Models:", models)
except Exception as e:
    st.error(f"❌ Failed to fetch models: {e}")
    st.stop()

# ✅ Choose the best available model
preferred_models = [
    "models/gemini-1.5-pro-latest",
    "models/gemini-1.5-flash-latest",
    "models/gemini-2.0-pro-exp",
    "models/gemini-2.0-flash-lite"
]

model_name = next((m for m in preferred_models if m in models), None)

if not model_name:
    st.error("❌ No suitable Gemini model found! Check API access or enable AI Studio API in Google Cloud.")
    st.stop()

st.success(f"✅ Using Gemini Model: {model_name}")

# ✅ Model Configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# ✅ Function to Generate Response
import google.generativeai as genai

import json
import re

import google.generativeai as genai
import json
import re

def generate_response_from_gemini(input_text):
    """
    Calls the Gemini API and ensures the response is always a well-formed JSON output.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        # ✅ Call the model with input text
        response = model.generate_content(input_text)

        # ✅ Print raw response for debugging
        print("\n🔍 Raw AI Response:\n", response)

        # ✅ If response is already a dictionary, return it directly
        if isinstance(response, dict):
            print("\n✅ Parsed JSON Data (Direct Dict):\n", json.dumps(response, indent=4))
            return response

        # ✅ If response is a string, extract JSON content using regex
        response_text = response.text if hasattr(response, "text") else str(response)

        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)  # Extract JSON content
        else:
            raise ValueError("❌ AI response did not contain valid JSON.")

        # ✅ Attempt to parse JSON
        response_data = json.loads(json_string)
        print("\n✅ Parsed JSON Data (Extracted from Text):\n", json.dumps(response_data, indent=4))  
        return response_data

    except json.JSONDecodeError:
        print("❌ AI response is not valid JSON.")
        return None  # Handle JSON parsing failures

    except Exception as e:
        print(f"❌ API Error: {e}")
        return None  # Handle API failures




# ✅ Extract Text from Files
def extract_text_from_pdf_file(uploaded_file):
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = "".join(page.extract_text() or "" for page in pdf_reader.pages)
    return text_content

def extract_text_from_docx_file(uploaded_file):
    return docx2txt.process(uploaded_file)

# ✅ Prompt Template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, full stack web development, cloud engineer, 
cloud developers, devops engineer and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

# ✅ Load Lottie Animations
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lottie file not found: {filepath}")
        return None

file_path = os.path.abspath("./assets/checking.json")
lottie_checking = load_lottiefile(file_path)

# ✅ Streamlit App UI
st.title("Track My Resume 😎")
st.markdown('<style>h1{color: orange; text-align: center; font-family:POPPINS}</style>', unsafe_allow_html=True)

job_description = st.text_area("Paste the Job Description", height=300)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])

if uploaded_file:
    st.markdown('<h8 style="color: lightgreen;text-align: center;">File uploaded successfully!</h8>', unsafe_allow_html=True)

# ✅ Buttons
col1, col2, col3 = st.columns([4, 4, 2])
with col1:
    submit_button = st.button("Check ATS Result")
with col2:
    submit_button1 = st.button("Check Score")
with col3:
    submit_button2 = st.button("How it Works?")

# ✅ Function to Process and Display ATS Score in Separate Columns
import json
import re


import json
import streamlit as st


import google.generativeai as genai
import json
import re


def process_ats_result():
    if uploaded_file:
        st.lottie(lottie_checking, speed=1, loop=True, quality="low", height="200px", width="200px")

        # ✅ Extract resume text based on file type
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)

        # ✅ Modify prompt to enforce JSON output
        formatted_prompt = f"""
        You are an ATS system evaluator. Your task is to analyze the resume against the given job description 
        and return a JSON response that includes the match score, missing keywords, candidate summary, and relevant experience.

        ⚠️ IMPORTANT: Return ONLY valid JSON output, formatted **exactly** like this:
        {{
          "Job Description Match": "XX%",
          "Missing Keywords": "keyword1, keyword2",
          "Candidate Summary": "A summary of the candidate",
          "Experience": "Detailed experience matching the job description"
        }}

        🚨 STRICT RULES:
        - **DO NOT include explanations, markdown, or text before/after the JSON.**  
        - **Ensure the JSON keys match EXACTLY (do not change them).**  
        - **Keep percentages inside strings, like `"XX%"`.**  
        - **Missing keywords should be a comma-separated string.**  
        - **Return pure JSON, no extra text.**

        --- Candidate Resume ---
        {resume_text}

        --- Job Description ---
        {job_description}
        """

        response_text = generate_response_from_gemini(formatted_prompt)

        # ✅ Debugging: Print raw AI response
        print("\n🔍 Raw AI Response:\n", response_text)

        # ✅ Attempt to parse JSON
        try:
            response_data = response_text
            print("\n✅ Parsed JSON Data:\n", json.dumps(response_data, indent=4))  # Pretty print JSON
        except json.JSONDecodeError:
            st.error("❌ AI response contains invalid JSON. Please retry.")
            print("❌ Failed to parse AI response into JSON.")
            return  # ❌ Stop execution if JSON parsing fails

        # ✅ Standardize response format
        ats_data = {
            "Job Description Match": response_data.get("Job Description Match", "XX%"),
            "Missing Keywords": response_data.get("Missing Keywords", "No missing keywords"),
            "Candidate Summary": response_data.get("Candidate Summary", "No summary available."),
            "Experience": response_data.get("Experience", "No experience details available.")
        }

        # ✅ Ensure AI provided a valid match score
        if ats_data["Job Description Match"] == "XX%":
            st.warning("⚠️ AI did not generate a valid match score. Please retry.")
            print("❌ AI failed to provide a valid match score.")
            return

        # ✅ UI Enhancements
        st.markdown("<h3 style='color: yellow;'>🔍 ATS Evaluation Summary</h3>", unsafe_allow_html=True)

        # ✅ Display match percentage with progress bar
        match_percentage_value = float(ats_data["Job Description Match"].replace("%", "").strip())
        st.markdown(f"<h4 style='color: green;'>✅ Match Score: <b>{ats_data['Job Description Match']}</b></h4>", unsafe_allow_html=True)
        st.progress(match_percentage_value / 100)

        # ✅ Display Missing Keywords (highlight in red if missing)
        if ats_data["Missing Keywords"].lower() != "no missing keywords":
            st.markdown(f"<h4 style='color: red;'>⚠️ Missing Keywords</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: red; font-size: 18px;'><b>{ats_data['Missing Keywords']}</b></p>", unsafe_allow_html=True)

        # ✅ Display Candidate Summary
        st.markdown(f"<h4 style='color: blue;'>👤 Candidate Summary</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'>{ats_data['Candidate Summary']}</p>", unsafe_allow_html=True)

        # ✅ Display Experience
        st.markdown(f"<h4 style='color: purple;'>💼 Experience</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'>{ats_data['Experience']}</p>", unsafe_allow_html=True)

        # ✅ Show Profile Match Recommendation
        if match_percentage_value >= 80:
            st.markdown('<p style="color: green; font-size: 20px;">✅ Move forward with hiring</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: lightgreen; font-size: 20px;">⚡ Profile Matched! Improve missing keywords.</p>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please upload your Resume to continue.")



if submit_button or submit_button1:
    process_ats_result()
