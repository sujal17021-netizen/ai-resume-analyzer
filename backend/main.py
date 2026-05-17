from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

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

# AI route
@app.get("/analyze")
def analyze():

    response = model.generate_content(
        "Give 3 tips to improve a software engineering resume."
    )

    return {
        "result": response.text
    }