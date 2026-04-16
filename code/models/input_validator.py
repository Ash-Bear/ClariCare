"""
ClariCare - Input Validator (v1)
Screens user messages for intent BEFORE the NLP symptom pipeline runs.

Handles:
  - Greetings / pleasantries          → redirect to describing symptoms
  - Wellness / "I'm fine" statements  → acknowledge, offer to help
  - Gibberish / random characters     → polite prompt for real input
  - Very short / vague input          → ask to elaborate
  - Off-topic questions               → redirect to health scope
  - Testing phrases                   → friendly challenge
  - Mental-health crisis signals      → provide crisis resources
  - Follow-up phase mis-answers       → gentle reclarification

Each check returns an InputValidationResult with:
  - is_valid   : bool    — True if input should proceed to NLP pipeline
  - intent     : str     — detected intent label (for logging)
  - reply      : str     — Clara's redirect reply (empty if valid)
  - quick_replies : list — suggested quick replies to show the user
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    is_valid: bool
    intent: str = "valid"
    reply: str = ""
    quick_replies: List[str] = field(default_factory=list)


# ─── Intent pattern tables ────────────────────────────────────────────────────
# Ordered from most specific → least specific.

_CRISIS_PATTERNS = [
    r"\bkill\s*(my)?self\b",
    r"\bsuicid",
    r"\bwant\s+to\s+die\b",
    r"\bend\s+(my|it\s+all|everything)\b",
    r"\bhurt\s*(my)?self\b",
    r"\bself[- ]?harm\b",
    r"\bno\s+reason\s+to\s+(live|exist)\b",
    r"\bfeel\s+like\s+dying\b",
    r"\bgo\s+away\s+forever\b",
]

_GREETING_PATTERNS = [
    r"^(hi|hey|hello|howdy|hiya|yo|sup|greetings|good\s+(morning|afternoon|evening|night))\W*$",
    r"^\bwhat[' ]?s\s+up\b",
    r"^\bwhats\s+new\b",
    r"^(namaste|hola|bonjour|salut|ciao)\W*$",
]

_WELLBEING_OK_PATTERNS = [
    r"\b(i[' ]?m|i\s+am)\s+(fine|okay|ok|good|great|well|alright|fit|healthy|perfectly fine|all good|feeling good|feeling well|feeling great|feeling fine|doing well|doing good|doing great|doing fine)\b",
    r"\b(feeling\s+)?(perfectly|totally|absolutely)\s+(fine|good|ok|great|normal)\b",
    r"\bno\s+(symptoms|complaints|issues|problems|concerns)\b",
    r"\bnothing\s+(is\s+)?(wrong|wrong with me|to report)\b",
    r"\ball\s+good\b",
    r"\bnothing\s+wrong\b",
    r"\bcompletely\s+healthy\b",
    r"\bjust\s+checking\s*(it|this)?\s*out\b",
    r"\bjust\s+(browsing|looking|testing|exploring)\b",
]

_TESTING_PATTERNS = [
    r"^(test|testing|test\s+\d*|sample|dummy|placeholder|hello world|foo|bar|baz|qux|asdf|lorem)\W*$",
    r"^(check|ping|check\s*\d*|status|is this (on|working|live))\W*$",
    r"^(1234|0000|1111|9999|abcd|xyz|hack)\W*$",
    r"\bjust\s+testing\b",
    r"\bletting\s+you\s+know\s+i[' ]?m\s+",  # "letting you know i'm fine" etc.
]

_GIBBERISH_PATTERNS = [
    r"^[^a-z\s]{3,}$",                           # only symbols / numbers
    r"^([a-z])\1{4,}$",                          # aaaaaaa, bbbbbb
    r"^[a-z]{1,2}$",                             # single/double char: "a", "xy"
    r"^(qwerty|asdfgh|zxcvbn|qazwsx)",           # keyboard smash
    # NOTE: the former r"^([a-z]{1,3}\s*){5,}$" was REMOVED because regex
    # backtracking allowed it to match any normal sentence (e.g. "i have fever"
    # was matched because "have" splits as "hav"+"e" — two 1-3 char chunks).
    # The word-level check is now handled by _is_all_short_words() below.
]


def _is_all_short_words(text: str, max_len: int = 3, min_words: int = 5) -> bool:
    """Return True only if the text has ≥min_words tokens and ALL are ≤max_len chars.
    Uses actual word splitting (not regex backtracking) to avoid false positives."""
    words = re.findall(r"[a-z]+", text.lower())
    if len(words) < min_words:
        return False
    return all(len(w) <= max_len for w in words)

_SHORT_VAGUE_MAX_WORDS = 2   # ≤2 real words counts as "too vague"

_OFFTOPIC_PATTERNS = [
    r"\bweather\b",
    r"\bwhat\s+(time|day|date|year)\b",
    r"\btell\s+me\s+a\s+(joke|story|fact)\b",
    r"\bwho\s+(are\s+you|made\s+you|created\s+you|built\s+you)\b",
    r"\bwhat\s+(is|are)\s+(your\s+name|claricare)\b",
    r"\b(recommend|suggest)\s+(a\s+)?(movie|book|song|restaurant|food)\b",
    r"\bplay\s+(music|song|video)\b",
    r"\blaugh|entertain|funny\b",
    r"\bcovid\s+(?!symptom)",  # COVID topics not about symptoms
    r"\bpolitics|election|government\b",
    r"\bstock|crypto|bitcoin|invest\b",
]

# ─── Follow-up phase validators ───────────────────────────────────────────────

_DURATION_VALID_HINTS = [
    r"\bday(s)?\b", r"\bweek(s)?\b", r"\bmonth(s)?\b", r"\bhour(s)?\b",
    r"\bmorning\b", r"\btoday\b", r"\byesterday\b", r"\brecent\b",
    r"\blong\b", r"\bjust\b", r"\bstarted\b", r"\bago\b",
    r"\bsince\b", r"\bwhile\b",
    # quick reply selections
    r"\b(1|2|3|4|5|6|7|8|9|10)\b",
    r"just started", r"about a week", r"more than",
    r"several", r"over a month",
]

_SEVERITY_VALID_HINTS = [
    r"\b([1-9]|10)\b",                        # any number 1-10
    r"\b(mild|moderate|severe|very severe|unbearable|excruciating)\b",
    r"\b(a\s+)?\d\s*(out\s+of\s*10|\/\s*10)\b",
]


# ─── Utility helpers ─────────────────────────────────────────────────────────

def _match_any(text: str, patterns: list, flags=re.IGNORECASE) -> bool:
    for p in patterns:
        if re.search(p, text, flags):
            return True
    return False


def _word_count(text: str) -> int:
    return len(re.findall(r"[a-zA-Z']+", text))


def _char_entropy(text: str) -> float:
    """Rough measure of character-level entropy — low = repetitive/gibberish."""
    import math
    text = text.lower()
    if len(text) < 3:
        return 0.0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    total = len(text)
    entropy = -sum((n / total) * math.log2(n / total) for n in freq.values())
    return entropy


# ─── Main Validator class ─────────────────────────────────────────────────────

class InputValidator:
    """
    Screens user input for intent before the NLP symptom pipeline runs.
    Call validate_greeting() for the initial symptom description phase,
    and validate_followup() for duration/severity phases.
    """

    # ── Greeting phase ────────────────────────────────────────────────────────

    def validate_greeting(self, text: str) -> ValidationResult:
        """
        Check if the initial symptom input is:
        1. A mental-health crisis signal
        2. A greeting
        3. A "I'm fine / all good" statement
        4. A testing / dummy input
        5. Gibberish
        6. Off-topic
        7. Too short/vague to extract symptoms from

        Returns ValidationResult. If is_valid=True, proceed to NLP pipeline.
        """
        t = text.strip()
        lower = t.lower()

        # ── 1. Crisis / self-harm ─────────────────────────────────────────────
        if _match_any(lower, _CRISIS_PATTERNS):
            logger.info("InputValidator: crisis signal detected")
            return ValidationResult(
                is_valid=False,
                intent="crisis",
                reply=(
                    "💙 I hear you, and I want you to know that you matter deeply. "
                    "ClariCare is not equipped to provide crisis support, but help is available right now.\n\n"
                    "Please reach out to a mental health crisis line:\n"
                    "• 🇮🇳 iCall (India): 9152987821\n"
                    "• 🌍 International Association for Suicide Prevention: "
                    "https://www.iasp.info/resources/Crisis_Centres/\n\n"
                    "You are not alone. Please talk to someone. 💙"
                ),
                quick_replies=[]
            )

        # ── 2. Greeting / pleasantry ──────────────────────────────────────────
        if _match_any(lower, _GREETING_PATTERNS) and _word_count(t) <= 5:
            logger.info("InputValidator: greeting detected")
            return ValidationResult(
                is_valid=False,
                intent="greeting",
                reply=(
                    "Hey there! 👋 I'm Clara, your ClariCare health assistant. "
                    "I'm here specifically to help you understand health symptoms and guide you "
                    "toward the right care.\n\n"
                    "Are you experiencing any symptoms today? "
                    "Just describe how you're feeling and I'll take it from there!"
                ),
                quick_replies=[
                    "I have a headache", "I'm feeling feverish",
                    "My stomach hurts", "I feel very tired"
                ]
            )

        # ── 3. Wellness / "I'm fine" ──────────────────────────────────────────
        if _match_any(lower, _WELLBEING_OK_PATTERNS):
            logger.info("InputValidator: wellness statement detected")
            return ValidationResult(
                is_valid=False,
                intent="wellness",
                reply=(
                    "That's wonderful to hear — I'm glad you're feeling well! 😊\n\n"
                    "ClariCare is here whenever you or someone you know needs health guidance. "
                    "If you're testing the platform, try describing a symptom like "
                    "\"I have a headache and feel tired\" to see a full analysis."
                ),
                quick_replies=[
                    "I have a headache", "I feel dizzy",
                    "My stomach hurts", "I have a cough"
                ]
            )

        # ── 4. Testing / dummy phrases ────────────────────────────────────────
        if _match_any(lower, _TESTING_PATTERNS):
            logger.info("InputValidator: test/dummy input detected")
            return ValidationResult(
                is_valid=False,
                intent="testing",
                reply=(
                    "Looks like you might be testing me! 🔍 "
                    "I'm designed to understand real health symptoms — "
                    "I work best when you describe what you're actually feeling.\n\n"
                    "Try something like: \"I've had a throbbing headache and "
                    "feel nauseous since yesterday\" — and watch me analyse it!"
                ),
                quick_replies=[
                    "I have a headache", "I'm feeling feverish",
                    "I have chest pain", "My stomach hurts"
                ]
            )

        # ── 5. Gibberish detection ────────────────────────────────────────────
        words = _word_count(t)
        entropy = _char_entropy(re.sub(r'\s+', '', lower))

        if _match_any(lower, _GIBBERISH_PATTERNS):
            logger.info("InputValidator: gibberish pattern detected")
            return self._gibberish_response()

        if words <= 1 and len(t) > 1 and entropy < 2.5:
            logger.info(f"InputValidator: low-entropy single token (entropy={entropy:.2f})")
            return self._gibberish_response()

        # Mostly non-alpha characters (symbols / numbers) with no real word
        alpha_ratio = len(re.sub(r'[^a-z]', '', lower)) / max(len(lower), 1)
        if alpha_ratio < 0.4 and words == 0:
            logger.info("InputValidator: non-alpha dominated input")
            return self._gibberish_response()

        # ── 6. Off-topic ──────────────────────────────────────────────────────
        if _match_any(lower, _OFFTOPIC_PATTERNS):
            logger.info("InputValidator: off-topic input detected")
            return ValidationResult(
                is_valid=False,
                intent="off_topic",
                reply=(
                    "I appreciate the curiosity! 😊 "
                    "I'm Clara, ClariCare's health assistant — I specialise in "
                    "understanding health symptoms and guiding you toward the right care.\n\n"
                    "I'm not able to help with that, but if you have any health concern, "
                    "I'm all ears! What symptoms are you experiencing?"
                ),
                quick_replies=[
                    "I have a headache", "I'm feeling feverish",
                    "My stomach hurts", "I have a cough"
                ]
            )

        # ── 7. Too short / vague ──────────────────────────────────────────────
        if words <= _SHORT_VAGUE_MAX_WORDS and len(t) < 10:
            logger.info(f"InputValidator: too short/vague ({words} words)")
            return ValidationResult(
                is_valid=False,
                intent="vague",
                reply=(
                    "I got your message, but I need a bit more detail to help you properly. 🩺\n\n"
                    "Could you describe what you're feeling? For example:\n"
                    "• Which part of your body is affected?\n"
                    "• What does the discomfort feel like (sharp, dull, throbbing)?\n"
                    "• Any other symptoms alongside it?\n\n"
                    "The more you share, the better I can guide you!"
                ),
                quick_replies=[
                    "I have a headache", "I feel very tired",
                    "My stomach hurts", "I have a fever"
                ]
            )

        # ── All checks passed — input is likely a real symptom description ────
        return ValidationResult(is_valid=True, intent="symptom")

    # ── Follow-up phase validators ─────────────────────────────────────────────

    def validate_duration(self, text: str) -> ValidationResult:
        """
        Check that the user's reply to 'how long?' is actually a time expression.
        Allows free-text like 'since Monday' as well as quick-reply buttons.
        """
        lower = text.strip().lower()

        # Wellness / off-topic during follow-up
        if _match_any(lower, _WELLBEING_OK_PATTERNS) or _match_any(lower, _GREETING_PATTERNS):
            return ValidationResult(
                is_valid=False,
                intent="off_topic_followup",
                reply=(
                    "I still need to know how long you've been experiencing these symptoms "
                    "to give you an accurate assessment. "
                    "Could you pick an option or estimate the duration?"
                ),
                quick_replies=[
                    "Just started today", "1–2 days", "About a week",
                    "More than a week", "Several weeks", "Over a month"
                ]
            )

        # Check for any time-related hint
        if _match_any(lower, _DURATION_VALID_HINTS):
            return ValidationResult(is_valid=True, intent="duration")

        # Numbers alone (e.g. "3") could be days — accept
        if re.match(r"^\d+$", lower.strip()):
            return ValidationResult(is_valid=True, intent="duration")

        # Too short and no time hint
        if _word_count(text) <= 2 and not _match_any(lower, _DURATION_VALID_HINTS):
            return ValidationResult(
                is_valid=False,
                intent="unclear_duration",
                reply=(
                    "I didn't quite catch that. "
                    "How long have you been experiencing these symptoms? "
                    "For example: '2 days', 'about a week', or 'over a month'."
                ),
                quick_replies=[
                    "Just started today", "1–2 days", "About a week",
                    "More than a week", "Several weeks", "Over a month"
                ]
            )

        return ValidationResult(is_valid=True, intent="duration")

    def validate_severity(self, text: str) -> ValidationResult:
        """
        Check that the user's reply to 'rate 1-10' is a valid severity answer.
        """
        lower = text.strip().lower()

        # Wellness / off-topic
        if _match_any(lower, _WELLBEING_OK_PATTERNS) or _match_any(lower, _GREETING_PATTERNS):
            return ValidationResult(
                is_valid=False,
                intent="off_topic_followup",
                reply=(
                    "To continue the assessment, I need you to rate the severity "
                    "of your symptoms on a scale of 1 to 10 — "
                    "where 1 is barely noticeable and 10 is unbearable."
                ),
                quick_replies=[
                    "1–3 (Mild)", "4–6 (Moderate)", "7–8 (Severe)", "9–10 (Very Severe)"
                ]
            )

        if _match_any(lower, _SEVERITY_VALID_HINTS):
            return ValidationResult(is_valid=True, intent="severity")

        # Accept any free-text description that has a number
        if re.search(r"\b\d+\b", lower):
            return ValidationResult(is_valid=True, intent="severity")

        # No numeric or label hint
        return ValidationResult(
            is_valid=False,
            intent="unclear_severity",
            reply=(
                "I need a severity rating to factor it into your risk assessment. "
                "On a scale of 1 to 10, how would you rate the discomfort — "
                "1 being barely noticeable and 10 being unbearable?"
            ),
            quick_replies=[
                "1–3 (Mild)", "4–6 (Moderate)", "7–8 (Severe)", "9–10 (Very Severe)"
            ]
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _gibberish_response() -> ValidationResult:
        return ValidationResult(
            is_valid=False,
            intent="gibberish",
            reply=(
                "I wasn't able to understand that input. 🤔 "
                "I work best when you describe your health symptoms in plain language.\n\n"
                "For example: \"I've had a bad headache, feel nauseous, and "
                "am running a temperature since yesterday.\"\n\n"
                "Give it a try — what are you experiencing?"
            ),
            quick_replies=[
                "I have a headache", "I'm feeling feverish",
                "My stomach hurts", "I have a cough"
            ]
        )
