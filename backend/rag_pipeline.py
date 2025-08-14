# backend/rag_pipeline.py
"""
RAG pipeline for AgriAgent.
- Builds grounded 'facts' from live/mock data (weather, market, soil)
- Stores them in a local ChromaDB vector store
- Retrieves top-k facts per query
"""

import os
import time
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
import numpy as np
from sentence_transformers import SentenceTransformer

# Local persistent vector store directory
VSTORE_DIR = os.getenv("AGRI_VECTORSTORE_DIR", os.path.join(os.path.dirname(__file__), "..", "vectorstore"))

# Initialize Chroma client (persistent)
client = chromadb.PersistentClient(path=VSTORE_DIR, settings=Settings(allow_reset=False))

# Create / get collection
COLLECTION_NAME = "agri_facts"
collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

# Embedding model (downloads the first time)
_EMBEDDER = None
def _embedder():
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _EMBEDDER

def _emb(texts: List[str]) -> List[List[float]]:
    # Convert to vectors (list of floats)
    model = _embedder()
    vecs = model.encode(texts, normalize_embeddings=True).astype(np.float32)
    return vecs.tolist()

# --------- Fact building ---------
def _to_fact_text(kind: str, payload: Dict[str, Any], location: str, crop: str) -> List[str]:
    """
    Convert raw dicts from data_fetcher into small, retrievable fact sentences.
    """
    facts = []
    if kind == "weather":
        # Example payload: {"forecast": "...", "risk": "..."}
        if payload.get("forecast"):
            facts.append(f"[WEATHER] District={location} | Forecast: {payload['forecast']}")
        if payload.get("risk"):
            facts.append(f"[WEATHER] District={location} | Risk: {payload['risk']}")
    elif kind == "market":
        # Example payload: {"latest_price": "₹2,100/quintal", "trend": "Prices stable"}
        if payload.get("latest_price"):
            facts.append(f"[MARKET] Crop={crop} | Latest modal price: {payload['latest_price']}")
        if payload.get("trend"):
            facts.append(f"[MARKET] Crop={crop} | Price trend: {payload['trend']}")
    elif kind == "soil":
        # Example payload: {"status": "Low nitrogen", "recommendation": "Apply urea"}
        if payload.get("status"):
            facts.append(f"[SOIL] District={location} | Status: {payload['status']}")
        if payload.get("recommendation"):
            facts.append(f"[SOIL] District={location} | Recommendation: {payload['recommendation']}")
    return [f for f in facts if f and isinstance(f, str)]

def upsert_agri_facts(location: str, crop: str, weather: Dict[str, Any], market: Dict[str, Any], soil: Dict[str, Any]) -> int:
    """
    Upsert (add) fact chunks for this (location, crop) snapshot.
    Returns number of facts inserted.
    """
    now = int(time.time())
    texts: List[str] = []
    metas: List[Dict[str, Any]] = []
    ids: List[str] = []

    for kind, payload in [("weather", weather), ("market", market), ("soil", soil)]:
        for idx, fact in enumerate(_to_fact_text(kind, payload, location, crop)):
            texts.append(fact)
            metas.append({"kind": kind, "location": location, "crop": crop, "ts": now})
            ids.append(f"{kind}:{location}:{crop}:{now}:{idx}")

    if not texts:
        return 0

    collection.add(documents=texts, metadatas=metas, ids=ids, embeddings=_emb(texts))
    return len(texts)

def retrieve_facts(query: str, top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Retrieve top-k similar facts for the given query.
    Returns list of dicts: {"text": str, "metadata": {...}, "distance": float}
    """
    results = collection.query(
        query_embeddings=_emb([query]),
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    out = []
    if results and results.get("documents"):
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]
        for d, m, dist in zip(docs, metas, dists):
            out.append({"text": d, "metadata": m, "distance": float(dist)})
    return out

def build_rag_prompt(query: str, retrieved: List[Dict[str, Any]]) -> str:
    """
    Build a compact, instruction-following prompt for Gemini using retrieved facts.
    Output must be JSON with keys: recommendation, rationale, confidence, sources.
    """
    facts = "\n".join(f"- {r['text']}" for r in retrieved) or "- (no facts found)"
    prompt = f"""
You are AgriAgent, a safety-first agricultural advisor. Use ONLY the facts provided.
If facts are insufficient or conflicting, say so and advise contacting a local officer.

User question:
{query}

Retrieved factual context:
{facts}

Instructions:
- Answer in **English**.
- Give a single, actionable **recommendation** under 30 words.
- Provide a **brief rationale** using the retrieved facts only (no outside assumptions).
- Estimate a **confidence** between 0 and 1 based on how relevant/specific the facts are.
- Provide **sources** as high-level dataset names (e.g., "IMD", "Agmarknet", "Soil Health Card").
- Output strict JSON only with keys: recommendation, rationale, confidence, sources.
"""
    return prompt
