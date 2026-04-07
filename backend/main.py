"""
ClariCare - FastAPI Backend Application
AI-Powered Health Guidance Assistant API
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("ClariCare")

# ─── Lazy-loaded global instances ────────────────────────────────────────────────
analyzer = None
risk_classifier = None
doctor_recommender = None
response_generator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize models on startup."""
    global analyzer, risk_classifier, doctor_recommender, response_generator

    logger.info("=" * 60)
    logger.info("   ClariCare - AI Health Guidance Assistant")
    logger.info("   Starting up...")
    logger.info("=" * 60)

    from models.symptom_analyzer import BERTSymptomAnalyzer
    from models.risk_classifier import RiskClassifier
    from models.doctor_recommender import DoctorRecommender
    from models.response_generator import ResponseGenerator

    analyzer = BERTSymptomAnalyzer()
    risk_classifier = RiskClassifier()
    doctor_recommender = DoctorRecommender()
    response_generator = ResponseGenerator()

    if analyzer.bert_model is not None:
        logger.info("✅ BERT model loaded successfully (BioBERT)")
    else:
        logger.info("⚠️  BERT not available — using keyword-only matching")

    logger.info("✅ All models initialized")
    logger.info("=" * 60)

    yield

    logger.info("ClariCare shutting down...")


# ─── FastAPI App ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="ClariCare API",
    description="AI-Powered Health Guidance Assistant — Ethical, Non-Diagnostic Symptom Analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# ─── Request / Response Models ───────────────────────────────────────────────────

class SymptomRequest(BaseModel):
    """Request model for symptom analysis."""
    symptoms: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="User's symptom description in natural language",
        json_schema_extra={"example": "I have a persistent headache and feel very tired and nauseous"}
    )


class AnalysisResponse(BaseModel):
    """Full analysis response."""
    success: bool
    narrative: str
    disclaimer: str
    risk: dict
    sections: dict
    specialists: list
    analysis_meta: dict


# ─── API Endpoints ───────────────────────────────────────────────────────────────

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML page."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ClariCare API is running. Frontend not found."}


@app.get("/api/health")
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "ClariCare",
        "version": "1.0.0",
        "bert_available": analyzer.bert_model is not None if analyzer else False,
        "nlp_method": "BERT + Keyword Hybrid" if (analyzer and analyzer.bert_model) else "Keyword Only"
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_symptoms(request: SymptomRequest):
    """
    Main analysis endpoint.
    
    Pipeline: User Input → Symptom Extraction → Risk Assessment →
              Doctor Recommendation → Response Generation → Output
    """
    try:
        logger.info(f"Analyzing symptoms: '{request.symptoms[:80]}...'")

        # Step 1: Symptom Extraction (NLP + BERT)
        symptom_analysis = analyzer.analyze(request.symptoms)
        extracted = symptom_analysis["extracted_symptoms"]
        logger.info(f"  → Extracted {len(extracted)} symptoms via {symptom_analysis['nlp_method']}")

        # Step 2: Risk Classification
        risk_result = risk_classifier.classify(extracted)
        logger.info(f"  → Risk level: {risk_result['risk_label']}")

        # Step 3: Doctor Recommendation
        doctor_result = doctor_recommender.recommend(extracted, risk_result["overall_risk"])
        logger.info(f"  → {doctor_result['total_specialists']} specialist(s) recommended")

        # Step 4: Response Generation
        response = response_generator.generate(
            symptom_analysis, risk_result, doctor_result
        )

        return AnalysisResponse(
            success=True,
            narrative=response["narrative"],
            disclaimer=response["disclaimer"],
            risk=response["risk"],
            sections=response["sections"],
            specialists=response["specialists"],
            analysis_meta=response["analysis_meta"]
        )

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during analysis: {str(e)}"
        )


@app.get("/api/symptoms")
async def list_symptoms():
    """Return all known symptoms for autocomplete/reference."""
    from data.symptoms_db import SYMPTOM_KEYWORDS, SPECIALIST_MAP, RISK_LEVELS

    symptoms = []
    risk_map = {}
    for level, info in RISK_LEVELS.items():
        for s in info["symptoms"]:
            risk_map[s] = level

    for key, keywords in SYMPTOM_KEYWORDS.items():
        specialist_info = SPECIALIST_MAP.get(key, {})
        symptoms.append({
            "key": key,
            "name": key.replace("_", " ").title(),
            "keywords": keywords[:5],
            "risk_level": risk_map.get(key, "low"),
            "specialist": specialist_info.get("specialist", "General Physician"),
            "icon": specialist_info.get("icon", "🩺")
        })

    return {"symptoms": symptoms, "total": len(symptoms)}


# ─── Run ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
