from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import tempfile
from pcb_detector import PCBDefectDetector

app = FastAPI()
detector = PCBDefectDetector()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/detect", response_class=HTMLResponse)
async def detect(request: Request, file: UploadFile = File(...)):
    
    # 📌 1. Créer un fichier temporaire pour cette seule requête
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    # 📌 2. Appeler ton modèle IA sur l’image temporaire
    result = detector.detect(temp_path)

    # 📌 3. Retourner la page avec le rapport seulement (pas d’image)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "report": result["report"],
            "image_path": None  # Pas d'image affichée
        }
    )

