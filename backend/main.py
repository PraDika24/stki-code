from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import os
from .tf_idf import get_similar_resumes
from .tf_p import get_similar_resumes_tfp

app = FastAPI()

# Konfigurasi CORS agar frontend bisa akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lokasi folder frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "frontend"))

# Mount static files (untuk akses file PDF)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "archive")), name="static")

# GET ke root: tampilkan form pencarian
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoint untuk pencarian dengan metode yang dipilih (TF-P atau TF-IDF)
@app.post("/api/search")
async def api_search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    method = data.get("method", "tf_idf")  # Default ke TF-IDF jika tidak ada metode yang dipilih

    # Pilih metode berdasarkan input
    if method == "tf_p":
        results = get_similar_resumes_tfp(query)
    else:
        results = get_similar_resumes(query)

    return JSONResponse(content=results)