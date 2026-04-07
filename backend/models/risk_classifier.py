"""
ClariCare - Risk Classifier
Classifies extracted symptoms into Low / Medium / High risk categories.
"""

from typing import Dict, List, Tuple
from data.symptoms_db import RISK_LEVELS


class RiskClassifier:
    """
    Rule-based risk classifier that evaluates the overall risk level
    based on the combination and severity of detected symptoms.
    """

    def __init__(self):
        # Build reverse lookup: symptom -> risk level
        self.symptom_risk_map = {}
        for level, info in RISK_LEVELS.items():
            for symptom in info["symptoms"]:
                self.symptom_risk_map[symptom] = level

    def classify(self, extracted_symptoms: Dict[str, Dict]) -> Dict:
        """
        Classify risk based on extracted symptoms.
        
        Rules:
        - If ANY high-risk symptom is present → High Risk
        - If ≥2 medium-risk symptoms → Medium Risk  
        - If 1 medium-risk symptom → Medium Risk
        - Otherwise → Low Risk
        - Multiple low-risk symptoms can escalate to Medium if count ≥ 4
        """
        if not extracted_symptoms:
            return {
                "overall_risk": "none",
                "risk_label": "No Risk Identified",
                "risk_color": "#6b7280",
                "urgency_message": "No specific symptoms were identified. If you're feeling unwell, please describe your symptoms in more detail.",
                "symptom_risks": {},
                "risk_factors": []
            }

        symptom_risks = {}
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        risk_factors = []

        for symptom_key, details in extracted_symptoms.items():
            confidence = details.get("confidence", 0)
            if confidence < 0.4:  # Skip low-confidence matches
                continue

            risk_level = self.symptom_risk_map.get(symptom_key, "low")
            symptom_risks[symptom_key] = {
                "risk_level": risk_level,
                "confidence": confidence,
                "risk_info": RISK_LEVELS[risk_level]
            }
            risk_counts[risk_level] += 1

        # Determine overall risk
        if risk_counts["high"] > 0:
            overall_risk = "high"
            risk_factors.append("One or more symptoms flagged as high-priority")
        elif risk_counts["medium"] >= 2:
            overall_risk = "medium"
            risk_factors.append("Multiple symptoms requiring attention detected")
        elif risk_counts["medium"] == 1:
            overall_risk = "medium"
            risk_factors.append("A symptom requiring monitoring has been identified")
        elif risk_counts["low"] >= 4:
            overall_risk = "medium"
            risk_factors.append("Multiple mild symptoms together may warrant attention")
        else:
            overall_risk = "low"
            risk_factors.append("Symptoms appear manageable with self-care")

        # Add additional context
        if risk_counts["high"] > 0 and risk_counts["medium"] > 0:
            risk_factors.append("Combination of high and moderate priority symptoms detected")

        total_symptoms = sum(risk_counts.values())
        if total_symptoms >= 5:
            risk_factors.append("Multiple concurrent symptoms — monitoring recommended")

        risk_info = RISK_LEVELS[overall_risk]

        return {
            "overall_risk": overall_risk,
            "risk_label": risk_info["label"],
            "risk_color": risk_info["color"],
            "urgency_message": risk_info["urgency"],
            "symptom_risks": symptom_risks,
            "risk_factors": risk_factors,
            "risk_summary": {
                "high_count": risk_counts["high"],
                "medium_count": risk_counts["medium"],
                "low_count": risk_counts["low"],
                "total": total_symptoms
            }
        }
