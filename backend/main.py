from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber
import io

# Load env
load_dotenv()

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini config
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# Home route
@app.get("/")
def home():
    return {"message": "Backend working"}

# Analyze route
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # Read uploaded PDF
    contents = await file.read()

    # Extract text from PDF
    pdf_text = ""

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"

    # Prompt
    prompt = f"""
    Analyze this resume and provide:

    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. ATS Score
    5. Improvement Suggestions

    Resume:
    {pdf_text}
    """

    # Gemini response
    response = model.generate_content(prompt)

    return {
        "analysis": response.text
    }