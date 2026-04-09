from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import time
from stego import encode_image, decode_image

app = FastAPI()

# ✅ Base directory fix (VERY IMPORTANT for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Folder setup
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ✅ Static & templates FIX
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# 🏠 Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "decoded_message": None
    })


# 🔐 Encode
@app.post("/encode")
async def encode(file: UploadFile = File(...), message: str = Form(...)):
    timestamp = int(time.time())

    input_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = os.path.join(OUTPUT_DIR, f"stego_{timestamp}.png")

    encode_image(input_path, message, output_path)

    return FileResponse(output_path, filename="stego.png", media_type="image/png")


# 🔍 Decode
@app.post("/decode", response_class=HTMLResponse)
async def decode(request: Request, file: UploadFile = File(...)):
    timestamp = int(time.time())

    input_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    message = decode_image(input_path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "decoded_message": message
    })