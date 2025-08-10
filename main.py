from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# import google.generativeai as genai
from google import genai
import io
import fitz  # PyMuPDF
import tempfile
# import speech_recognition as sr
import os
import requests
from google.genai import types
import json
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key=os.getenv["GEMINI_API_KEY"])

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# model = genai.GenerativeModel("gemini-2.5-flash-lite")

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    
    contents = await file.read()
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=[
        types.Part.from_bytes(
            data=contents,
            mime_type='image/jpeg',
        ),
        "Describe this image in detail including scene, objects, and context."
        ]
    )

    
    # image = Image.open(io.BytesIO(contents))

    # prompt = "Describe this image in detail including scene, objects, and context."

    try:
        #response = model.generate_content([prompt, image])
        return JSONResponse(content={"description": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    """Summarizes and analyzes the content of an uploaded PDF document."""
    try:
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = "".join(page.get_text() for page in pdf)

        if not text.strip():
            return JSONResponse(content={"success": False, "error": "No extractable text found in the PDF."}, status_code=400)

        prompt = (
            "You're an expert document analyst. Please summarize the following document, "
            "identifying its purpose, tone, and key insights."
        )

        # Pass the extracted text directly to the model
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[prompt, text[:10000]]  # Limit context size for safety
        )
        return JSONResponse(content={"success": True, "summary": response.text})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

def merge_speaker_segments(segments):
    """Merge consecutive segments from the same speaker."""
    merged = []
    for seg in segments:
        if merged and merged[-1]["speaker"] == seg["speaker"]:
            merged[-1]["text"] += " " + seg["text"]
            merged[-1]["end"] = seg["end"]
        else:
            merged.append(seg.copy())
    return merged


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    temp_path = None
    try:
        # Save uploaded file
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            temp_path = tmp.name
            tmp.write(await file.read())

        # Upload full audio file to Gemini
        uploaded_file = client.files.upload(file=temp_path)

        # Stronger instruction for JSON output
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[
                """You are a transcription and diarization engine.
                Return ONLY valid JSON with this structure:
                [
                    {"speaker": "SPEAKER_1", "start": seconds, "end": seconds, "text": "..."}
                ]
                No extra commentary, no code fences, no explanations. JSON only.""",
                uploaded_file
            ]
        )

        # Clean potential code fences or extra text
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.lower().startswith("json"):
                raw_text = raw_text[4:].strip()

        # Parse JSON
        try:
            raw_segments = json.loads(raw_text)
        except json.JSONDecodeError:
            return {
                "success": False,
                "transcript": "",
                "error": f"Invalid JSON returned from Gemini: {raw_text[:200]}..."
            }

        # Merge same-speaker consecutive segments
        cleaned_segments = merge_speaker_segments(raw_segments)

        return {
            "success": True,
            "transcript": json.dumps(cleaned_segments)  # send as string
        }

    except Exception as e:
        return {"success": False, "transcript": "", "error": str(e)}

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
