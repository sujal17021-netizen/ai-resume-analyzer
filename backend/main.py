from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
from dotenv import load_dotenv
import os

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

# Analyze route
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # Read uploaded file
    content = await file.read()

    prompt = f"""
    Analyze this resume and give:

    1. Strengths
    2. Weaknesses
    3. Skills improvement suggestions

    Resume filename:
    {file.filename}
    """

    # Gemini response
    response = model.generate_content(prompt)

    return {
        "analysis": response.text
    }