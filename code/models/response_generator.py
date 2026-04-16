"""
ClariCare - Response Generator
Generates calm, ethical, non-diagnostic health guidance responses.
"""

from typing import Dict, List
from dataset.symptoms_db import POSSIBLE_CAUSES, LIFESTYLE_ADVICE

DISCLAIMER = (
    "⚕️ Important Disclaimer: ClariCare is an AI-powered guidance tool and does NOT "
    "provide medical diagnoses, treatment plans, or prescriptions. The information "
    "provided is for general informational purposes only. Always consult a qualified "
    "healthcare professional for proper medical evaluation and advice. If you are "
    "experiencing a medical emergency, please call your local emergency number immediately."
)


class ResponseGenerator:
    """
    Generates structured, empathetic health guidance responses
    that are strictly non-diagnostic and ethically responsible.
    """

    def generate(
        self,
        symptom_analysis: Dict,
        risk_result: Dict,
        doctor_result: Dict
    ) -> Dict:
        """
        Generate a complete guidance response combining all analysis results.
        """
        extracted = symptom_analysis.get("extracted_symptoms", {})

        if not extracted:
            return self._no_symptoms_response(symptom_analysis)

        # Build response sections
        greeting = self._build_greeting(risk_result["overall_risk"])
        symptom_summary = self._build_symptom_summary(extracted)
        possible_causes = self._build_causes_section(extracted)
        lifestyle_advice = self._build_lifestyle_section(extracted)
        doctor_section = self._build_doctor_section(doctor_result)

        # Compose full narrative response
        narrative = self._compose_narrative(
            greeting, symptom_summary, possible_causes,
            lifestyle_advice, doctor_section, risk_result
        )

        return {
            "narrative": narrative,
            "disclaimer": DISCLAIMER,
            "sections": {
                "greeting": greeting,
                "symptom_summary": symptom_summary,
                "possible_causes": possible_causes,
                "lifestyle_advice": lifestyle_advice,
                "doctor_recommendation": doctor_section,
            },
            "risk": {
                "level": risk_result["overall_risk"],
                "label": risk_result["risk_label"],
                "color": risk_result["risk_color"],
                "urgency": risk_result["urgency_message"],
                "factors": risk_result.get("risk_factors", [])
            },
            "specialists": doctor_result.get("specialists", []),
            "analysis_meta": {
                "method": symptom_analysis.get("nlp_method", "unknown"),
                "bert_available": symptom_analysis.get("bert_available", False),
                "symptoms_detected": len(extracted),
                "tokens_analyzed": len(symptom_analysis.get("tokens", []))
            }
        }

    def _no_symptoms_response(self, symptom_analysis: Dict) -> Dict:
        return {
            "narrative": (
                "Thank you for reaching out to ClariCare. I wasn't able to identify specific "
                "symptoms from your description. Could you please try describing how you're "
                "feeling in more detail? For example:\n\n"
                "• What part of your body is affected?\n"
                "• How long have you been experiencing this?\n"
                "• Is the discomfort constant or intermittent?\n\n"
                "The more details you provide, the better guidance I can offer."
            ),
            "disclaimer": DISCLAIMER,
            "sections": {},
            "risk": {
                "level": "none",
                "label": "No Risk Identified",
                "color": "#6b7280",
                "urgency": "",
                "factors": []
            },
            "specialists": [],
            "analysis_meta": {
                "method": symptom_analysis.get("nlp_method", "unknown"),
                "bert_available": symptom_analysis.get("bert_available", False),
                "symptoms_detected": 0,
                "tokens_analyzed": len(symptom_analysis.get("tokens", []))
            }
        }

    def _build_greeting(self, risk_level: str) -> str:
        if risk_level == "high":
            return (
                "Thank you for sharing your symptoms with ClariCare. I want to address "
                "your concerns carefully. Based on what you've described, I'd like to "
                "provide some important guidance."
            )
        elif risk_level == "medium":
            return (
                "Thank you for reaching out to ClariCare. I've reviewed what you've "
                "described, and I'd like to share some helpful information and suggestions."
            )
        else:
            return (
                "Thank you for using ClariCare! Based on your description, here's some "
                "gentle guidance that may be helpful."
            )

    def _build_symptom_summary(self, extracted: Dict) -> List[Dict]:
        summary = []
        for symptom_key, details in extracted.items():
            if details.get("confidence", 0) < 0.4:
                continue
            summary.append({
                "symptom": symptom_key.replace("_", " ").title(),
                "confidence": details["confidence"],
                "method": details.get("method", "unknown")
            })
        return summary

    def _build_causes_section(self, extracted: Dict) -> Dict[str, List[str]]:
        causes = {}
        for symptom_key in extracted:
            if extracted[symptom_key].get("confidence", 0) < 0.4:
                continue
            symptom_causes = POSSIBLE_CAUSES.get(symptom_key, [])
            if symptom_causes:
                display_name = symptom_key.replace("_", " ").title()
                causes[display_name] = symptom_causes
        return causes

    def _build_lifestyle_section(self, extracted: Dict) -> Dict[str, List[str]]:
        advice = {}
        for symptom_key in extracted:
            if extracted[symptom_key].get("confidence", 0) < 0.4:
                continue
            symptom_advice = LIFESTYLE_ADVICE.get(symptom_key, [])
            if symptom_advice:
                display_name = symptom_key.replace("_", " ").title()
                advice[display_name] = symptom_advice
        return advice

    def _build_doctor_section(self, doctor_result: Dict) -> Dict:
        return {
            "primary": doctor_result.get("primary_recommendation"),
            "all_specialists": doctor_result.get("specialists", []),
            "general_advice": doctor_result.get("general_advice", ""),
            "total": doctor_result.get("total_specialists", 0)
        }

    def _compose_narrative(
        self, greeting, symptom_summary, causes,
        lifestyle, doctor, risk_result
    ) -> str:
        parts = [greeting, ""]

        # Symptoms detected
        if symptom_summary:
            symptom_names = [s["symptom"] for s in symptom_summary]
            parts.append(
                f"Based on your description, I identified the following areas of concern: "
                f"{', '.join(symptom_names)}."
            )
            parts.append("")

        # Risk level
        parts.append(f"📊 Risk Assessment: {risk_result['risk_label']}")
        parts.append(risk_result["urgency_message"])
        parts.append("")

        # Possible causes
        if causes:
            parts.append("🔍 Some common, non-clinical factors that may be associated with your symptoms include:")
            for symptom_name, cause_list in causes.items():
                parts.append(f"\n  {symptom_name}:")
                for cause in cause_list[:3]:
                    parts.append(f"    • {cause}")
            parts.append("")

        # Lifestyle advice
        if lifestyle:
            parts.append("💡 Lifestyle suggestions that may help:")
            all_advice = []
            for advice_list in lifestyle.values():
                all_advice.extend(advice_list)
            # De-duplicate and limit
            seen = set()
            unique_advice = []
            for tip in all_advice:
                if tip not in seen:
                    seen.add(tip)
                    unique_advice.append(tip)
            for tip in unique_advice[:6]:
                parts.append(f"  • {tip}")
            parts.append("")

        # Doctor recommendation
        doc = doctor.get("primary")
        if doc:
            parts.append(
                f"👨‍⚕️ We suggest consulting a {doc['name']} "
                f"based on your described symptoms."
            )
            parts.append(doctor.get("general_advice", ""))

        return "\n".join(parts)
