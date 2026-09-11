"""
Ford Price Predictor -- REST API

Loads a RandomForestRegressor trained on UK Ford car listings and serves
a single prediction endpoint, plus the small static frontend that talks
to it. The model and its column list are loaded once at startup, not
per-request.
"""

import os
import pickle

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Resolve paths relative to this file (not the process's working directory)
# so this works the same locally and on Render.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ford_price_predictor.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.pkl")

model = joblib.load(MODEL_PATH)
with open(COLUMNS_PATH, "rb") as f:
    MODEL_COLUMNS = pickle.load(f)

# Real category vocabulary the model was trained on (from ford.csv).
CAR_MODELS = [
    "B-MAX", "C-MAX", "EcoSport", "Edge", "Escort", "Fiesta", "Focus",
    "Fusion", "Galaxy", "Grand C-MAX", "Grand Tourneo Connect", "KA",
    "Ka+", "Kuga", "Mondeo", "Mustang", "Puma", "Ranger", "S-MAX",
    "Streetka", "Tourneo Connect", "Tourneo Custom", "Transit Tourneo",
]
TRANSMISSIONS = ["Automatic", "Manual", "Semi-Auto"]
FUEL_TYPES = ["Diesel", "Electric", "Hybrid", "Other", "Petrol"]
ENGINE_SIZE_MEDIAN = 1.2  # training-time fallback used when engineSize == 0

app = FastAPI(title="Ford Price Predictor API", version="1.0.0")

# Enabled for both local development and production so the frontend can
# call this API regardless of where it ends up being served from.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CarFeatures(BaseModel):
    model: str = Field(..., description="Ford model name, e.g. 'Fiesta'")
    year: int = Field(..., ge=1980, le=2035)
    transmission: str
    mileage: float = Field(..., ge=0)
    fuelType: str
    tax: float = Field(..., ge=0)
    mpg: float = Field(..., gt=0)
    engineSize: float = Field(..., ge=0, le=10)


class PredictionResponse(BaseModel):
    predicted_price: float


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/predict", response_model=PredictionResponse)
def predict(car: CarFeatures):
    if car.model not in CAR_MODELS:
        raise HTTPException(422, f"Unknown model '{car.model}'")
    if car.transmission not in TRANSMISSIONS:
        raise HTTPException(422, f"Unknown transmission '{car.transmission}'")
    if car.fuelType not in FUEL_TYPES:
        raise HTTPException(422, f"Unknown fuelType '{car.fuelType}'")

    # Same cleanup applied at training time: a handful of listings have
    # engineSize == 0, which the model was trained to treat as the median.
    engine_size = car.engineSize if car.engineSize > 0 else ENGINE_SIZE_MEDIAN

    try:
        input_data = pd.DataFrame(
            [[car.model, car.year, car.transmission, car.mileage,
              car.fuelType, car.tax, car.mpg, engine_size]],
            columns=["model", "year", "transmission", "mileage",
                     "fuelType", "tax", "mpg", "engineSize"],
        )
        input_encoded = pd.get_dummies(input_data)
        for col in MODEL_COLUMNS:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[MODEL_COLUMNS]

        prediction = float(model.predict(input_encoded)[0])
    except Exception as exc:  # defensive: never leak internals to the client
        raise HTTPException(500, "Prediction failed.") from exc

    return PredictionResponse(predicted_price=round(prediction, 2))


# --- Static frontend -------------------------------------------------
# Served as explicit routes (rather than mounting the whole directory)
# so main.py, requirements.txt, and the model files are never reachable
# over HTTP -- only the three frontend files are.

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/style.css")
def serve_css():
    return FileResponse(os.path.join(BASE_DIR, "style.css"), media_type="text/css")


@app.get("/script.js")
def serve_js():
    return FileResponse(os.path.join(BASE_DIR, "script.js"), media_type="text/javascript")
