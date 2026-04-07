"""
ClariCare - Doctor Recommender
Maps detected symptoms to appropriate medical specialists.
"""

from typing import Dict, List
from data.symptoms_db import SPECIALIST_MAP


class DoctorRecommender:
    """
    Maps detected symptoms to the most appropriate medical specialists,
    de-duplicates recommendations, and provides context-aware suggestions.
    """

    def recommend(self, extracted_symptoms: Dict[str, Dict], risk_level: str) -> Dict:
        """
        Generate specialist recommendations based on extracted symptoms.
        Returns de-duplicated specialists with the symptoms that suggest each.
        """
        if not extracted_symptoms:
            return {
                "specialists": [],
                "primary_recommendation": None,
                "general_advice": "Please describe your symptoms in more detail so we can suggest the right type of specialist."
            }

        # Collect specialists and their triggering symptoms
        specialist_symptoms = {}  # specialist_name -> {symptoms, icon, max_confidence}

        for symptom_key, details in extracted_symptoms.items():
            confidence = details.get("confidence", 0)
            if confidence < 0.4:
                continue

            mapping = SPECIALIST_MAP.get(symptom_key)
            if not mapping:
                continue

            specialist = mapping["specialist"]
            icon = mapping["icon"]

            if specialist not in specialist_symptoms:
                specialist_symptoms[specialist] = {
                    "name": specialist,
                    "icon": icon,
                    "symptoms": [],
                    "max_confidence": 0.0
                }

            specialist_symptoms[specialist]["symptoms"].append(
                symptom_key.replace("_", " ").title()
            )
            specialist_symptoms[specialist]["max_confidence"] = max(
                specialist_symptoms[specialist]["max_confidence"], confidence
            )

        # Sort by confidence (most relevant first)
        specialists = sorted(
            specialist_symptoms.values(),
            key=lambda x: x["max_confidence"],
            reverse=True
        )

        # Primary recommendation
        primary = specialists[0] if specialists else None

        # General advice based on risk level
        if risk_level == "high":
            general_advice = (
                "Based on the symptoms described, we recommend seeking medical attention promptly. "
                "If your symptoms are severe, please consider visiting an emergency department."
            )
        elif risk_level == "medium":
            general_advice = (
                "It would be advisable to schedule an appointment with a healthcare professional "
                "to discuss these symptoms further."
            )
        else:
            general_advice = (
                "These symptoms may be manageable with self-care, but don't hesitate to "
                "consult a healthcare professional if they persist or worsen."
            )

        return {
            "specialists": specialists,
            "primary_recommendation": primary,
            "general_advice": general_advice,
            "total_specialists": len(specialists)
        }
