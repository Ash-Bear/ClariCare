"""
ClariCare - Risk Classifier (v3)
Intelligent risk classification that accounts for:
  1. Inherent symptom risk levels
  2. Total symptom burden (multi-symptom escalation)
  3. Duration context (longer = higher risk)
  4. Severity rating (patient-reported pain scale)
  5. Combinations of medium-risk symptoms that together constitute high concern
"""

import re
from typing import Dict, List
from dataset.symptoms_db import RISK_LEVELS


# ─── Duration → risk modifier mapping ──────────────────────────────────────────
# Maps duration phrases (from follow-up Q1) to escalation scores.
# Positive value = escalate risk; 0 = no change.

DURATION_ESCALATION = {
    # Same-day / very short → no escalation
    "just started today":       0,
    "today":                    0,
    "started today":            0,
    "few hours":                0,
    "hours":                    0,

    # 1-2 days → minor escalation for medium+ symptoms
    "1-2 days":                 1,
    "1–2 days":                 1,
    "couple of days":           1,
    "two days":                 1,
    "a day or two":             1,
    "day or two":               1,

    # About a week → moderate escalation
    "about a week":             2,
    "a week":                   2,
    "week":                     2,
    "few days":                 1,
    "3-4 days":                 1,
    "4-5 days":                 1,
    "5-6 days":                 2,

    # More than a week → significant escalation
    "more than a week":         3,
    "over a week":              3,
    "ten days":                 3,
    "two weeks":                3,

    # Chronic — weeks to months → strong escalation
    "several weeks":            4,
    "a month":                  4,
    "weeks":                    3,
    "month":                    4,
    "months":                   5,
    "several months":           5,
    "long time":                4,
    "for a long time":          4,
    "chronic":                  5,
}

# ─── Severity → risk modifier mapping ──────────────────────────────────────────
# Maps severity rating bucket (from follow-up Q2) to escalation scores.

SEVERITY_ESCALATION = {
    "1":  0, "1-3": 0, "1–3": 0, "mild":       0,
    "2":  0, "3":   0,
    "4":  1, "4-6": 1, "4–6": 1, "moderate":   1,
    "5":  1, "6":   1,
    "7":  2, "7-8": 2, "7–8": 2, "severe":     2,
    "8":  2,
    "9":  3, "9-10": 3, "9–10": 3, "very severe": 3,
    "10": 3, "unbearable": 3, "excruciating": 3,
}

# ─── Symptom combinations that warrant medium→high escalation ──────────────────
# If ALL symptoms in a set are detected, that combination escalates to high risk.

HIGH_CONCERN_COMBINATIONS = [
    {"chest_pain", "shortness_of_breath"},
    {"chest_pain", "palpitations"},
    {"shortness_of_breath", "palpitations"},
    {"fever", "shortness_of_breath"},
    {"chest_pain", "dizziness"},
    {"vomiting", "blood_in_urine"},
    {"fever", "blood_in_urine"},
    {"memory_loss", "tremors"},
    {"numbness", "muscle_weakness"},
    {"numbness", "blurred_vision"},
    {"severe_headache", "numbness"},
    {"migraine", "numbness"},
    {"palpitations", "dizziness", "shortness_of_breath"},
]

# Medium symptoms that in combination (3+) escalate to medium-high
MEDIUM_COMBO_THRESHOLD = 3  # If 3+ different medium-risk symptoms detected


class RiskClassifier:
    """
    Intelligent risk classifier incorporating:
    - Symptom base risk
    - Multi-symptom burden scoring
    - Duration escalation
    - Severity escalation
    - Dangerous combination detection
    """

    def __init__(self):
        # Build reverse lookup: symptom → base risk level
        self.symptom_risk_map = {}
        for level, info in RISK_LEVELS.items():
            for symptom in info["symptoms"]:
                self.symptom_risk_map[symptom] = level

    # ─── Duration parser ──────────────────────────────────────────────────────

    def _parse_duration_score(self, context_text: str) -> int:
        """
        Extract duration escalation score from accumulated conversation text.
        Scans for 'Duration: ...' segment and matches against DURATION_ESCALATION.
        Returns 0-5 escalation score.
        """
        # Extract the duration segment
        match = re.search(r'duration[:\s]+([^.]+)', context_text, re.IGNORECASE)
        if not match:
            return 0

        duration_text = match.group(1).strip().lower()

        # Try exact match first
        for phrase, score in DURATION_ESCALATION.items():
            if phrase in duration_text:
                return score

        # Fallback: detect month/week keywords
        if re.search(r'\bmonth', duration_text):
            return 4
        if re.search(r'\bweek', duration_text):
            return 2
        if re.search(r'\bday', duration_text):
            return 1
        return 0

    # ─── Severity parser ──────────────────────────────────────────────────────

    def _parse_severity_score(self, context_text: str) -> int:
        """
        Extract severity escalation score from 'Severity: ...' segment in text.
        Returns 0-3 escalation score.
        """
        match = re.search(r'severity[:\s]+([^.]+)', context_text, re.IGNORECASE)
        if not match:
            return 0

        severity_text = match.group(1).strip().lower()

        # Try label matches
        for label, score in SEVERITY_ESCALATION.items():
            if label in severity_text:
                return score

        # Try extracting a numeric value
        nums = re.findall(r'\b(\d+)\b', severity_text)
        if nums:
            val = int(nums[0])
            if val >= 9:
                return 3
            elif val >= 7:
                return 2
            elif val >= 4:
                return 1
        return 0

    # ─── Combination checker ──────────────────────────────────────────────────

    def _check_dangerous_combinations(self, detected_symptoms: set) -> List[str]:
        """
        Check if detected symptom set matches any known high-concern combination.
        Returns list of triggered combination descriptions.
        """
        triggered = []
        for combo in HIGH_CONCERN_COMBINATIONS:
            if combo.issubset(detected_symptoms):
                names = " + ".join(s.replace("_", " ").title() for s in combo)
                triggered.append(f"High-concern symptom combination: {names}")
        return triggered

    # ─── Main classify method ─────────────────────────────────────────────────

    def classify(self, extracted_symptoms: Dict[str, Dict], context_text: str = "") -> Dict:
        """
        Classify risk based on extracted symptoms + conversation context.

        Parameters
        ----------
        extracted_symptoms : dict
            Output from BERTSymptomAnalyzer.analyze()["extracted_symptoms"]
        context_text : str
            Full accumulated conversation text (used to extract duration/severity)
        """
        if not extracted_symptoms:
            return {
                "overall_risk": "none",
                "risk_label": "No Risk Identified",
                "risk_color": "#6b7280",
                "urgency_message": "No specific symptoms were identified. If you're feeling unwell, please describe your symptoms in more detail.",
                "symptom_risks": {},
                "risk_factors": [],
                "escalation_applied": False,
            }

        # ── Step 1: Categorise each detected symptom ─────────────────────────
        symptom_risks = {}
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        detected_set = set()

        for symptom_key, details in extracted_symptoms.items():
            confidence = details.get("confidence", 0)
            if confidence < 0.4:
                continue

            risk_level = self.symptom_risk_map.get(symptom_key, "low")
            symptom_risks[symptom_key] = {
                "risk_level": risk_level,
                "confidence": confidence,
                "risk_info": RISK_LEVELS[risk_level]
            }
            risk_counts[risk_level] += 1
            detected_set.add(symptom_key)

        total_symptoms = sum(risk_counts.values())

        # ── Step 2: Determine base risk ───────────────────────────────────────
        risk_factors = []
        combination_warnings = self._check_dangerous_combinations(detected_set)

        if risk_counts["high"] > 0 or combination_warnings:
            base_risk = "high"
            if risk_counts["high"] > 0:
                risk_factors.append("⚠️ One or more high-priority symptoms detected")
            risk_factors.extend(combination_warnings)

        elif risk_counts["medium"] >= MEDIUM_COMBO_THRESHOLD:
            # 3+ medium-risk symptoms together are high concern
            base_risk = "high"
            risk_factors.append(
                f"🔴 {risk_counts['medium']} concurrent moderate-risk symptoms — "
                "this combination warrants prompt medical attention"
            )
        elif risk_counts["medium"] >= 2:
            base_risk = "medium"
            risk_factors.append("Multiple symptoms requiring attention detected")
        elif risk_counts["medium"] == 1:
            base_risk = "medium"
            risk_factors.append("A symptom requiring monitoring has been identified")
        elif risk_counts["low"] >= 4:
            base_risk = "medium"
            risk_factors.append(
                f"Multiple ({risk_counts['low']}) mild symptoms together may warrant attention"
            )
        else:
            base_risk = "low"
            risk_factors.append("Symptoms appear manageable with self-care")

        if total_symptoms >= 5:
            risk_factors.append(
                f"📋 {total_symptoms} concurrent symptoms reported — a broader evaluation is advisable"
            )
        elif total_symptoms >= 3:
            risk_factors.append(
                f"📋 {total_symptoms} symptoms reported simultaneously"
            )

        # ── Step 3: Duration escalation ───────────────────────────────────────
        duration_score = self._parse_duration_score(context_text)
        severity_score = self._parse_severity_score(context_text)
        escalation_applied = False
        escalation_reason = ""

        # Map base risk to numeric so we can escalate
        RISK_ORDER = {"low": 0, "medium": 1, "high": 2}
        RISK_NAMES = {0: "low", 1: "medium", 2: "high"}
        current_rank = RISK_ORDER[base_risk]

        # Duration escalation rules
        if duration_score >= 4:
            # Chronic (weeks/months) — escalate by one level
            if current_rank < 2:
                current_rank = min(current_rank + 1, 2)
                escalation_applied = True
                escalation_reason = "⏳ Symptoms persisting for several weeks or longer — escalated risk level"
                risk_factors.append(escalation_reason)
        elif duration_score >= 2:
            # 3+ days of medium/high symptoms → escalate from low to medium
            if base_risk == "low" and current_rank < 2:
                current_rank = min(current_rank + 1, 2)
                escalation_applied = True
                escalation_reason = "⏳ Symptoms lasting more than a few days — escalated from low to medium risk"
                risk_factors.append(escalation_reason)

        # Severity escalation rules
        if severity_score >= 3:
            # Severe (9-10) — escalate one level
            if current_rank < 2:
                current_rank = min(current_rank + 1, 2)
                escalation_applied = True
                escalation_reason = "💢 Severe pain rating (9–10) — escalated risk level"
                risk_factors.append(escalation_reason)
        elif severity_score >= 2:
            # Severe (7-8) — escalate if currently low
            if base_risk == "low" and current_rank < 2:
                current_rank = min(current_rank + 1, 2)
                escalation_applied = True
                escalation_reason = "💢 High pain severity reported — escalated risk level"
                risk_factors.append(escalation_reason)

        overall_risk = RISK_NAMES[current_rank]

        # ── Step 4: Build urgency message ─────────────────────────────────────
        base_urgency = RISK_LEVELS[overall_risk]["urgency"]

        # Add duration-specific context
        if duration_score >= 4 and overall_risk in ("medium", "high"):
            base_urgency += (
                " Given the prolonged duration of your symptoms, "
                "a medical evaluation is strongly recommended."
            )
        elif duration_score >= 2 and overall_risk == "medium":
            base_urgency += (
                " Since these symptoms have been present for several days, "
                "it would be advisable to see a doctor soon."
            )

        risk_info = RISK_LEVELS[overall_risk]

        return {
            "overall_risk": overall_risk,
            "risk_label": risk_info["label"],
            "risk_color": risk_info["color"],
            "urgency_message": base_urgency,
            "symptom_risks": symptom_risks,
            "risk_factors": risk_factors,
            "escalation_applied": escalation_applied,
            "risk_summary": {
                "high_count": risk_counts["high"],
                "medium_count": risk_counts["medium"],
                "low_count": risk_counts["low"],
                "total": total_symptoms,
                "duration_score": duration_score,
                "severity_score": severity_score,
            }
        }
