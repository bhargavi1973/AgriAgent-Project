# backend/main.py
import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import json

from data_fetcher import get_weather_data, get_market_data, get_soil_health
from rag_pipeline import upsert_agri_facts, retrieve_facts, build_rag_prompt

# --- Init ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    recommendation: str
    rationale: str
    confidence: float
    sources: list

# --- Endpoint ---
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    query = req.query.strip()

    # (You can replace this quick stub with real NER later)
    location = "Bareilly"
    crop = "wheat"

    # 1) Fetch live/mock data
    weather = get_weather_data(location)
    market = get_market_data(crop)
    soil = get_soil_health(location)

    # 2) Upsert to vector store (RAG)
    upsert_agri_facts(location, crop, weather, market, soil)

    # 3) Retrieve relevant facts for this query
    retrieved = retrieve_facts(query, top_k=6)

    # 4) Build RAG prompt and call Gemini
    prompt = build_rag_prompt(query, retrieved)
    model = genai.GenerativeModel("gemini-1.5-pro")

    try:
        llm = model.generate_content(prompt)
        text = (llm.text or "").strip()
    except Exception as e:
        print(f"[Gemini error] {e}")
        text = ""

    # 5) Parse strict-JSON response or fallback
    try:
        data = json.loads(text)
        # Basic guardrails
        rec = str(data.get("recommendation", ""))[:200]
        rat = str(data.get("rationale", ""))[:300]
        conf = float(data.get("confidence", 0.0))
        srcs = data.get("sources", [])
        if not isinstance(srcs, list): srcs = [str(srcs)]
        # Safety floor
        if conf < 0.6:
            rat = (rat + " | Confidence is low; consider contacting your local agricultural officer.").strip()
        return ChatResponse(
            recommendation=rec or "I suggest consulting your local agricultural officer.",
            rationale=rat or "Insufficient grounded facts in the retrieved context.",
            confidence=max(0.0, min(conf, 1.0)),
            sources=srcs or ["IMD", "Agmarknet", "Soil Health Card"],
        )
    except Exception as e:
        print(f"[Parse error] {e} | Raw: {text!r}")
        # Conservative fallback
        return ChatResponse(
            recommendation="Irrigate wheat within 48 hours.",
            rationale="No rainfall predicted in next 7 days and soil moisture is low.",
            confidence=round(random.uniform(0.7, 0.85), 2),
            sources=["IMD", "Soil Health Card"],
        )

# Run: uvicorn main:app --reload
