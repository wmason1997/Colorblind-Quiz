# Colorblind Spectrum Test

An interactive web application that assesses color blindness by having users draw their perceived boundaries of the ROYGBIV color spectrum.

## Features

- Interactive color spectrum drawing interface
- Real-time image processing using OpenCV
- Color blindness assessment based on user input
- FastAPI backend for efficient processing

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

4. Open your browser and navigate to `http://localhost:8000`

## Technology Stack

- Backend: FastAPI
- Image Processing: OpenCV, NumPy
- Frontend: HTML, CSS, JavaScript 