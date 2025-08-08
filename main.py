from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from PIL import Image
import io
import os
import fitz  # PyMuPDF

genai.configure(api_key="AIzaSyAvmUQ14VQR9Eawla6aCZjvv0f5Ye_2ECA")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = genai.GenerativeModel("gemini-2.5-flash")

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    prompt = "Describe this image in detail including scene, objects, and context."
    try:
        response = model.generate_content([prompt, image])
        return JSONResponse(content={"description": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()

        if not text.strip():
            return JSONResponse(content={"error": "No extractable text found in PDF."}, status_code=400)

        prompt = (
            "You're an expert document analyst. First, check if the document follows a standard structure "
            "like Title, Sections, and Paragraphs. Then summarize its contents clearly, identifying purpose, tone, and key insights."
        )

        response = model.generate_content([prompt, text[:8000]])  # limit for Gemini models
        return JSONResponse(content={"summary": response.text})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
