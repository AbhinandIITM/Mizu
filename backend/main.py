from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image
import io
import os

genai.configure(api_key="AIzaSyDOTTXTU9saFnAFWv4w3lU7cO6AdeiFNiA")
model = genai.GenerativeModel("gemini-1.5-pro")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    prompt = "Describe this image in detail with scene, objects, people, and interpretation."

    try:
        response = model.generate_content([prompt, image])
        return JSONResponse(content={"description": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
