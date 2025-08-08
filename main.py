from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from PIL import Image
import io
import os
# from dotenv import load_dotenv

# load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDOTTXTU9saFnAFWv4w3lU7cO6AdeiFNiA"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = genai.GenerativeModel("gemini-1.5-pro")

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
