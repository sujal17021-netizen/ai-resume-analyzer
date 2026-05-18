from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber
import io
import json

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Home route
@app.get("/")
def home():
    return {"message": "Backend working"}

# Analyze resume route
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

    # ATS Prompt
    prompt = f"""
    You are an advanced ATS Resume Analyzer.

    Analyze the following resume professionally.

    Return ONLY valid JSON.

    Resume:
    {pdf_text}

    JSON format:
    {{
      "ats_score": 82,
      "breakdown": {{
        "skills_match": 20,
        "formatting": 12,
        "keywords": 16,
        "experience": 18,
        "readability": 8,
        "grammar": 9
      }},
      "strengths": [
        "Strong technical skills",
        "Good project experience"
      ],
      "weaknesses": [
        "Missing quantified achievements",
        "Formatting can be improved"
      ],
      "missing_skills": [
        "Docker",
        "AWS"
      ],
      "suggestions": [
        "Add measurable achievements",
        "Improve resume formatting",
        "Include more ATS keywords"
      ]
    }}
    """

    try:
        # Generate response
        response = model.generate_content(prompt)

        # Clean response text
        raw_text = response.text.strip()

        # Remove markdown formatting if Gemini adds it
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")

        # Convert JSON string to Python dictionary
        data = json.loads(raw_text)

        return data

    except Exception as e:
        return {
            "error": str(e)
        }