"""
ClariCare - Conversation Manager (v4)
Manages stateful multi-turn chatbot sessions via a phase-based state machine.

Phase Flow:
    greeting → follow_up_1 (duration) → follow_up_2 (severity) → follow_up_3 (add. symptoms) → analysis → done
    (emergency shortcut: greeting → analysis if HIGH-RISK symptom detected immediately)

v4 Changes (on top of v3):
- InputValidator screens every user turn BEFORE the NLP pipeline runs
- Greetings, wellness, gibberish, testing, off-topic, and crisis signals are
  intercepted and returned with empathetic redirect replies
- Duration and severity follow-up answers are validated for expected format
  (invalid answers re-prompt without consuming the phase transition)
"""

import uuid
import time
import logging
from typing import Dict, Optional

from models.input_validator import InputValidator

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Multi-turn conversation state machine for the ClariCare chatbot (Clara).

    Sessions are stored in-memory. Each session tracks:
        - Current phase
        - Full message history
        - Accumulated symptom text (sent to analysis pipeline)
        - Duration and severity metadata for risk escalation
        - Final analysis result
    """

    HIGH_RISK_SYMPTOMS = {"chest_pain", "shortness_of_breath", "blood_in_urine"}

    QUICK_REPLIES_F1 = [
        "Just started today", "1–2 days", "About a week",
        "More than a week", "Several weeks", "Over a month"
    ]
    QUICK_REPLIES_F2 = [
        "1–3 (Mild)", "4–6 (Moderate)", "7–8 (Severe)", "9–10 (Very Severe)"
    ]
    QUICK_REPLIES_F3 = [
        "No other symptoms", "I have a fever", "Feeling nauseous",
        "Feeling dizzy", "Very tired / fatigued", "Shortness of breath"
    ]
    QUICK_REPLIES_DONE = ["Start New Consultation"]
    QUICK_REPLIES_INIT = [
        "I have a headache", "I'm feeling feverish",
        "I have chest pain", "I'm very tired", "My stomach hurts"
    ]

    def __init__(self, analyzer, risk_classifier, doctor_recommender, response_generator):
        self.analyzer = analyzer
        self.risk_classifier = risk_classifier
        self.doctor_recommender = doctor_recommender
        self.response_generator = response_generator
        self.sessions: Dict[str, dict] = {}
        self.validator = InputValidator()

    # ─── Session helpers ──────────────────────────────────────────────────────────

    def _create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "phase": "greeting",
            "messages": [],
            "accumulated_text": "",
            "analysis_result": None,
            "created_at": time.time(),
            # v3: store parsed metadata for richer context
            "duration_answer": "",
            "severity_answer": "",
            "detected_symptoms_initial": {},
        }
        return session_id

    def _add_message(self, session: dict, role: str, text: str, extra: Optional[dict] = None):
        msg = {"role": role, "text": text, "timestamp": time.time()}
        if extra:
            msg.update(extra)
        session["messages"].append(msg)

    # ─── Emergency / risk helpers ─────────────────────────────────────────────────

    def _check_high_risk(self, extracted_symptoms: dict) -> bool:
        """Return True if any high-risk symptom is detected with ≥50% confidence."""
        for symptom, details in extracted_symptoms.items():
            if symptom in self.HIGH_RISK_SYMPTOMS and details.get("confidence", 0) >= 0.5:
                return True
        return False

    def _personalize_f1_question(self, extracted_symptoms: dict) -> str:
        """Craft a personalised duration question referencing the top detected symptoms."""
        if not extracted_symptoms:
            return (
                "I understand you're not feeling well. "
                "How long have you been experiencing these symptoms?"
            )
        symptom_names = [k.replace("_", " ") for k in list(extracted_symptoms.keys())[:2]]
        if len(symptom_names) == 1:
            return (
                f"I understand you're experiencing {symptom_names[0]}. "
                "How long have you been feeling this way?"
            )
        names_str = " and ".join(symptom_names)
        return (
            f"I understand you're experiencing {names_str}. "
            "How long have these symptoms been present?"
        )

    def _personalize_f2_question(self, extracted_symptoms: dict, duration_answer: str) -> str:
        """
        Craft a personalised severity question that references:
        - The primary symptom (most confident match)
        - The duration they just told us
        """
        top = list(extracted_symptoms.keys())[0] if extracted_symptoms else None
        top_name = top.replace("_", " ") if top else "your symptoms"

        duration_context = ""
        low_dur = duration_answer.lower()
        if any(x in low_dur for x in ["month", "weeks", "several"]):
            duration_context = " You've mentioned this has been going on for a while — "
        elif any(x in low_dur for x in ["week", "more than"]):
            duration_context = " For a symptom that's lasted this long, "
        else:
            duration_context = " "

        return (
            f"Got it.{duration_context}on a scale of 1 to 10, "
            f"how severe is your {top_name} right now? "
            "1 being barely noticeable, 10 being unbearable."
        )

    def _personalize_f3_question(self, extracted_symptoms: dict, severity_answer: str) -> str:
        """
        Craft an additional-symptoms question that adds urgency cues if
        severity is high.
        """
        high_severity = any(x in severity_answer.lower() for x in ["7", "8", "9", "10", "severe"])

        if high_severity:
            return (
                "I can see you're in significant discomfort. "
                "Are there **any other symptoms** alongside these? "
                "For example — fever, nausea, dizziness, difficulty breathing, or anything else unusual?"
            )
        return (
            "Thank you. Are there any **other symptoms** you've noticed alongside these? "
            "For example, fever, nausea, dizziness, fatigue, or anything else unusual?"
        )

    # ─── Analysis runner ──────────────────────────────────────────────────────────

    def _run_analysis(self, session: dict, emergency: bool = False) -> dict:
        """
        Run the full 4-stage pipeline on accumulated text and return the chat response.
        Passes full accumulated_text to RiskClassifier so it can parse duration/severity.
        """
        full_text = session["accumulated_text"]
        response = None

        try:
            symptom_analysis = self.analyzer.analyze(full_text)
            extracted = symptom_analysis["extracted_symptoms"]

            # v3: pass full context text so classifier can extract duration & severity
            risk_result = self.risk_classifier.classify(extracted, context_text=full_text)

            doctor_result = self.doctor_recommender.recommend(extracted, risk_result["overall_risk"])
            response = self.response_generator.generate(symptom_analysis, risk_result, doctor_result)
            logger.info(
                f"Session {session['session_id']}: analysis complete, "
                f"risk={risk_result['overall_risk']}, symptoms={len(extracted)}, "
                f"escalation={risk_result.get('escalation_applied', False)}"
            )
        except Exception as e:
            logger.error(f"Analysis failed in session {session['session_id']}: {e}", exc_info=True)

        session["analysis_result"] = response
        session["phase"] = "done"

        if emergency:
            bot_reply = (
                "⚠️ Some of your symptoms may need prompt attention. "
                "Here's my complete assessment — please review it carefully:"
            )
        else:
            bot_reply = (
                "Thank you for sharing all of that with me. "
                "Based on everything you've described, here's my comprehensive health guidance:"
            )

        self._add_message(session, "bot", bot_reply)
        if response:
            self._add_message(session, "analysis", "", extra={"data": response})

        show_emergency = bool(
            response and response.get("risk", {}).get("level") == "high"
        )

        return {
            "session_id": session["session_id"],
            "phase": "done",
            "bot_reply": bot_reply,
            "quick_replies": self.QUICK_REPLIES_DONE,
            "analysis": response,
            "show_emergency_alert": show_emergency,
        }

    # ─── Public API ───────────────────────────────────────────────────────────────

    def get_greeting(self) -> dict:
        """Create a new session and return the opening greeting message."""
        session_id = self._create_session()
        session = self.sessions[session_id]

        bot_reply = (
            "Hello! I'm Clara, your ClariCare health assistant. 👋\n\n"
            "I'm here to help you understand your symptoms and guide you toward the right care. "
            "Just describe how you're feeling in your own words — no medical jargon needed!\n\n"
            "What symptoms are you experiencing today?"
        )

        self._add_message(session, "bot", bot_reply)

        return {
            "session_id": session_id,
            "phase": "greeting",
            "bot_reply": bot_reply,
            "quick_replies": self.QUICK_REPLIES_INIT,
            "analysis": None,
            "show_emergency_alert": False,
        }

    def process_message(self, session_id: str, user_message: str) -> dict:
        """
        Process a user message within a session and advance the conversation state.

        If session_id is invalid or expired, a fresh greeting session is started
        and the user message is immediately processed in the new session.
        """
        session = self.sessions.get(session_id)

        if not session:
            logger.warning(f"Session {session_id} not found — creating new session")
            greeting = self.get_greeting()
            session_id = greeting["session_id"]
            session = self.sessions[session_id]

        self._add_message(session, "user", user_message)
        phase = session["phase"]

        # ── Phase: greeting (initial symptom description) ───────────────────────
        if phase == "greeting":

            # ── Input guard: screen before NLP ──────────────────────────────
            vr = self.validator.validate_greeting(user_message)
            if not vr.is_valid:
                # Do NOT advance the phase — let the user try again
                logger.info(f"Session {session_id}: input blocked [{vr.intent}]")
                self._add_message(session, "bot", vr.reply)
                return {
                    "session_id": session_id,
                    "phase": "greeting",
                    "bot_reply": vr.reply,
                    "quick_replies": vr.quick_replies,
                    "analysis": None,
                    "show_emergency_alert": False,
                }

            session["accumulated_text"] = user_message

            # Quick emergency scan
            try:
                quick = self.analyzer.analyze(user_message)
                extracted = quick["extracted_symptoms"]
                session["detected_symptoms_initial"] = extracted
                if self._check_high_risk(extracted):
                    session["phase"] = "analysis"
                    return self._run_analysis(session, emergency=True)
            except Exception:
                extracted = {}

            # If NLP found absolutely nothing after validation passed, re-prompt gently
            if not extracted:
                redirect = (
                    "I wasn't able to identify specific health symptoms in what you described. 🤔\n\n"
                    "Could you try describing your symptoms in more detail? For example:\n"
                    "• Which part of your body is bothering you?\n"
                    "• What does it feel like (sharp, dull, throbbing, burning)?\n"
                    "• Are there any other things you're noticing?"
                )
                self._add_message(session, "bot", redirect)
                return {
                    "session_id": session_id,
                    "phase": "greeting",
                    "bot_reply": redirect,
                    "quick_replies": self.QUICK_REPLIES_INIT,
                    "analysis": None,
                    "show_emergency_alert": False,
                }

            bot_reply = self._personalize_f1_question(extracted)
            session["phase"] = "follow_up_1"
            quick_replies = self.QUICK_REPLIES_F1

        # ── Phase: follow_up_1 — ask duration ───────────────────────────────────
        elif phase == "follow_up_1":

            # ── Input guard: must be a time expression ───────────────────────
            vr = self.validator.validate_duration(user_message)
            if not vr.is_valid:
                logger.info(f"Session {session_id}: duration answer blocked [{vr.intent}]")
                self._add_message(session, "bot", vr.reply)
                return {
                    "session_id": session_id,
                    "phase": "follow_up_1",
                    "bot_reply": vr.reply,
                    "quick_replies": vr.quick_replies,
                    "analysis": None,
                    "show_emergency_alert": False,
                }

            # Tag the answer so the risk classifier can parse it later
            session["duration_answer"] = user_message
            session["accumulated_text"] += f". Duration: {user_message}"

            bot_reply = self._personalize_f2_question(
                session.get("detected_symptoms_initial", {}),
                user_message
            )
            session["phase"] = "follow_up_2"
            quick_replies = self.QUICK_REPLIES_F2

        # ── Phase: follow_up_2 — ask severity ───────────────────────────────────
        elif phase == "follow_up_2":

            # ── Input guard: must be a severity rating ───────────────────────
            vr = self.validator.validate_severity(user_message)
            if not vr.is_valid:
                logger.info(f"Session {session_id}: severity answer blocked [{vr.intent}]")
                self._add_message(session, "bot", vr.reply)
                return {
                    "session_id": session_id,
                    "phase": "follow_up_2",
                    "bot_reply": vr.reply,
                    "quick_replies": vr.quick_replies,
                    "analysis": None,
                    "show_emergency_alert": False,
                }

            # Tag the answer so the risk classifier can parse it later
            session["severity_answer"] = user_message
            session["accumulated_text"] += f". Severity: {user_message}"

            bot_reply = self._personalize_f3_question(
                session.get("detected_symptoms_initial", {}),
                user_message
            )
            session["phase"] = "follow_up_3"
            quick_replies = self.QUICK_REPLIES_F3

        # ── Phase: follow_up_3 — collect additional symptoms → run analysis ─────
        elif phase == "follow_up_3":
            lower = user_message.lower()
            if "no other" not in lower and "none" not in lower and not lower.strip().startswith("no "):
                session["accumulated_text"] += f". Additional symptoms: {user_message}"
            session["phase"] = "analysis"
            return self._run_analysis(session)

        # ── Phase: done — user wants a new consultation ──────────────────────────
        elif phase == "done":
            session["phase"] = "greeting"
            session["accumulated_text"] = ""
            session["analysis_result"] = None
            session["duration_answer"] = ""
            session["severity_answer"] = ""
            session["detected_symptoms_initial"] = {}
            bot_reply = (
                "Of course! I'm ready to help again. "
                "What symptoms are you experiencing now?"
            )
            quick_replies = self.QUICK_REPLIES_INIT

        # ── Fallback ─────────────────────────────────────────────────────────────
        else:
            bot_reply = (
                "I didn't quite catch that. Could you describe your symptoms again? "
                "For example: 'I have a headache and feel tired.'"
            )
            quick_replies = self.QUICK_REPLIES_INIT

        self._add_message(session, "bot", bot_reply)

        return {
            "session_id": session_id,
            "phase": session["phase"],
            "bot_reply": bot_reply,
            "quick_replies": quick_replies,
            "analysis": None,
            "show_emergency_alert": False,
        }

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve a session by ID (for GET /api/session/{id})."""
        return self.sessions.get(session_id)
