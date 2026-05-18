from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# WORKING MODEL
model = genai.GenerativeModel("gemini-pro")

@app.get("/")
def home():
    return {"message": "Backend working"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    await file.read()

    response = model.generate_content(
        "Give 3 resume improvement tips."
    )

    return {
        "analysis": response.text
    }