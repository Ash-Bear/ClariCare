"""
ClariCare - FastAPI Backend Application (v2)
AI-Powered Health Guidance Assistant — Chatbot + Multi-Page API
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
conversation_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize all models and conversation manager on startup."""
    global analyzer, risk_classifier, doctor_recommender, response_generator, conversation_manager

    logger.info("=" * 60)
    logger.info("   ClariCare v2 — AI Health Guidance Chatbot")
    logger.info("   Starting up...")
    logger.info("=" * 60)

    from models.symptom_analyzer import BERTSymptomAnalyzer
    from models.risk_classifier import RiskClassifier
    from models.doctor_recommender import DoctorRecommender
    from models.response_generator import ResponseGenerator
    from models.conversation_manager import ConversationManager

    analyzer = BERTSymptomAnalyzer()
    risk_classifier = RiskClassifier()
    doctor_recommender = DoctorRecommender()
    response_generator = ResponseGenerator()
    conversation_manager = ConversationManager(
        analyzer, risk_classifier, doctor_recommender, response_generator
    )

    if analyzer.bert_model is not None:
        logger.info("✅ BERT model loaded successfully (BioBERT)")
    else:
        logger.info("⚠️  BERT not available — using keyword-only matching")

    logger.info("✅ All models initialized")
    logger.info("✅ ConversationManager ready")
    logger.info("=" * 60)

    yield

    logger.info("ClariCare shutting down...")


# ─── FastAPI App ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="ClariCare API",
    description="AI-Powered Health Guidance Assistant — Chatbot & Multi-Page Platform",
    version="2.0.0",
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
    """Request model for direct symptom analysis (legacy endpoint)."""
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


class ChatMessageRequest(BaseModel):
    """Request model for sending a chat message."""
    session_id: str = Field(..., description="Session ID from /api/chat/start")
    message: str = Field(..., min_length=1, max_length=2000, description="User's message text")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    session_id: str
    phase: str
    bot_reply: str
    quick_replies: list
    analysis: Optional[dict] = None
    show_emergency_alert: bool = False


# ─── Page Routes ─────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_landing():
    """Serve the landing page."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ClariCare API v2 is running. Frontend not found."}


@app.get("/chat")
async def serve_chat():
    """Serve the chatbot page."""
    chat_path = os.path.join(frontend_dir, "chat.html")
    if os.path.exists(chat_path):
        return FileResponse(chat_path)
    raise HTTPException(status_code=404, detail="chat.html not found")


@app.get("/about")
async def serve_about():
    """Serve the about page."""
    about_path = os.path.join(frontend_dir, "about.html")
    if os.path.exists(about_path):
        return FileResponse(about_path)
    raise HTTPException(status_code=404, detail="about.html not found")


@app.get("/explore")
async def serve_explore():
    """Serve the symptom explorer page."""
    explore_path = os.path.join(frontend_dir, "explore.html")
    if os.path.exists(explore_path):
        return FileResponse(explore_path)
    raise HTTPException(status_code=404, detail="explore.html not found")


# ─── Health API ───────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "ClariCare",
        "version": "2.0.0",
        "bert_available": analyzer.bert_model is not None if analyzer else False,
        "nlp_method": "BERT + Keyword Hybrid" if (analyzer and analyzer.bert_model) else "Keyword Only",
        "active_sessions": len(conversation_manager.sessions) if conversation_manager else 0,
    }


# ─── Chat API (Conversational) ────────────────────────────────────────────────────

@app.post("/api/chat/start", response_model=ChatResponse)
async def start_chat():
    """
    Create a new chat session and return the opening greeting.
    Call this when the user first opens the chat page.
    """
    if not conversation_manager:
        raise HTTPException(status_code=503, detail="ConversationManager not initialized")
    result = conversation_manager.get_greeting()
    return ChatResponse(**result)


@app.post("/api/chat/message", response_model=ChatResponse)
async def chat_message(request: ChatMessageRequest):
    """
    Send a user message and receive the bot's next reply.

    The conversation progresses through phases:
        greeting → follow_up_1 → follow_up_2 → follow_up_3 → analysis → done

    When phase reaches 'analysis', the response includes a full 'analysis' object.
    """
    if not conversation_manager:
        raise HTTPException(status_code=503, detail="ConversationManager not initialized")

    try:
        result = conversation_manager.process_message(request.session_id, request.message)
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Chat message error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Retrieve the full history and state of a chat session."""
    if not conversation_manager:
        raise HTTPException(status_code=503, detail="ConversationManager not initialized")
    session = conversation_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return session


# ─── Direct Analysis API (Legacy) ─────────────────────────────────────────────────

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_symptoms(request: SymptomRequest):
    """
    Direct (non-conversational) analysis endpoint.
    Pipeline: Input → Symptom Extraction → Risk Assessment → Doctor Recommendation → Response
    """
    try:
        logger.info(f"Direct analyze: '{request.symptoms[:80]}...'")

        symptom_analysis = analyzer.analyze(request.symptoms)
        extracted = symptom_analysis["extracted_symptoms"]
        logger.info(f"  → Extracted {len(extracted)} symptoms via {symptom_analysis['nlp_method']}")

        risk_result = risk_classifier.classify(extracted)
        logger.info(f"  → Risk level: {risk_result['risk_label']}")

        doctor_result = doctor_recommender.recommend(extracted, risk_result["overall_risk"])
        logger.info(f"  → {doctor_result['total_specialists']} specialist(s) recommended")

        response = response_generator.generate(symptom_analysis, risk_result, doctor_result)

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
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")


@app.get("/api/symptoms")
async def list_symptoms():
    """Return all known symptoms for the explorer page."""
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
