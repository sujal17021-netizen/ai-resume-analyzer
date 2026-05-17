from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Gemini model
model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# Home route
@app.get("/")
def home():
    return {
        "message": "Backend is working"
    }

# Analyze route
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    response = model.generate_content(
        "Give 3 tips to improve a software engineering resume."
    )

    return {
        "analysis": response.text
    }