from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.get("/")
def home():
    return {"message": "Backend working"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    await file.read()

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Give 3 resume improvement tips."
    )

    return {
        "analysis": response.text
    }