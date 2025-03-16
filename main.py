from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from color_analyzer import ColorAnalyzer
import os

# Create the FastAPI app
app = FastAPI(title="Colorblind Spectrum Test")

# Create necessary directories if they don't exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize color analyzer
analyzer = ColorAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_spectrum(data: dict):
    """
    Analyze the user's drawn spectrum lines and calculate color blindness score.
    
    Args:
        data (dict): Contains the coordinates of the drawn lines
        
    Returns:
        dict: Color blindness assessment results
    """
    lines = data.get("lines", [])
    return analyzer.analyze_spectrum(lines) 