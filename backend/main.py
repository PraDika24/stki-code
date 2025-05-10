from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import os
from .tf_idf import get_similar_resumes

app = FastAPI()

# ✅ Konfigurasi CORS agar frontend bisa akses API (jika pakai fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Lokasi folder frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "frontend"))

# ✅ Mount static files (untuk akses file PDF)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "archive")), name="static")

# ✅ GET ke root: tampilkan form pencarian
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ POST dari form (terima JSON alih-alih Form)
@app.post("/search", response_class=HTMLResponse)
async def search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    results = get_similar_resumes(query)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "query": query,
        "results": results
    })

# ✅ API Endpoint untuk fetch JS (optional jika pakai <script> fetch())
@app.post("/api/search")
async def api_search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    results = get_similar_resumes(query)
    return JSONResponse(content=results)