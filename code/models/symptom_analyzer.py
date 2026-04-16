"""
ClariCare - BERT-enhanced NLP Symptom Analyzer
Uses a pre-trained BERT model + traditional NLP for symptom extraction and matching.
"""

import re
import logging
from typing import List, Dict, Tuple

import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from dataset.symptoms_db import SYMPTOM_KEYWORDS, SYMPTOM_DESCRIPTIONS

logger = logging.getLogger(__name__)

# ─── Download required NLTK data ────────────────────────────────────────────────
def _ensure_nltk_data():
    """Download NLTK resources if not already present."""
    for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet']:
        try:
            nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource else f'corpora/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

_ensure_nltk_data()


class BERTSymptomAnalyzer:
    """
    Hybrid symptom analyzer combining:
    1) BERT-based semantic similarity for nuanced matching
    2) Rule-based keyword matching for reliability
    3) NLP preprocessing for text normalization
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Medical stopwords to keep (don't remove these even though they're common)
        self.medical_keep = {
            'pain', 'ache', 'sore', 'burning', 'sharp', 'dull',
            'no', 'not', 'can', 'cannot', 'hard', 'short', 'cold',
            'hot', 'dry', 'wet', 'red', 'high', 'low', 'fast', 'slow'
        }
        self.stop_words -= self.medical_keep
        
        # Add tokenization artifacts that cause false positive partial matches
        self.stop_words.update({'ca', "n't", "'s", "'m", "'re", "'ve", "'d", "'ll", 'feel', 'feeling', 'feels', 'felt'})

        # BERT model for semantic matching
        self.bert_model = None
        self.bert_tokenizer = None
        self.symptom_embeddings = {}
        self._load_bert_model()

    def _load_bert_model(self):
        """Load pre-trained BERT model for semantic symptom matching."""
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch

            logger.info("Loading BERT model for semantic symptom analysis...")
            model_name = "dmis-lab/biobert-base-cased-v1.2"
            self.bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.bert_model = AutoModel.from_pretrained(model_name)
            self.bert_model.eval()

            # Pre-compute embeddings for all symptom descriptions
            logger.info("Computing symptom embeddings...")
            with torch.no_grad():
                for symptom_key, description in SYMPTOM_DESCRIPTIONS.items():
                    embedding = self._get_bert_embedding(description)
                    if embedding is not None:
                        self.symptom_embeddings[symptom_key] = embedding

            logger.info(f"BERT model loaded. {len(self.symptom_embeddings)} symptom embeddings cached.")

        except Exception as e:
            logger.warning(f"BERT model could not be loaded: {e}. Falling back to keyword-only matching.")
            self.bert_model = None
            self.bert_tokenizer = None

    def _get_bert_embedding(self, text: str) -> np.ndarray:
        """Get BERT mean-pooled embedding for a text string.
        
        Uses mean pooling over token embeddings (excluding padding) instead of
        the [CLS] token, which produces more discriminative representations
        for short medical phrases.
        """
        if self.bert_model is None or self.bert_tokenizer is None:
            return None

        try:
            import torch
            inputs = self.bert_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=128,
                padding=True
            )
            with torch.no_grad():
                outputs = self.bert_model(**inputs)

            # Mean pooling over non-padding tokens for more discriminative embeddings
            attention_mask = inputs['attention_mask']
            token_embeddings = outputs.last_hidden_state  # (1, seq_len, hidden_dim)
            mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            sum_embeddings = torch.sum(token_embeddings * mask_expanded, dim=1)
            sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
            mean_embedding = (sum_embeddings / sum_mask).squeeze().numpy()

            # Normalize for cosine similarity
            norm = np.linalg.norm(mean_embedding)
            if norm > 0:
                mean_embedding = mean_embedding / norm
            return mean_embedding
        except Exception as e:
            logger.error(f"BERT embedding error: {e}")
            return None

    def _preprocess_text(self, text: str) -> str:
        """NLP preprocessing: lowercase, remove special chars, lemmatize."""
        text = text.lower().strip()
        text = re.sub(r'[^a-z\s\'-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _tokenize_and_clean(self, text: str) -> List[str]:
        """Tokenize text and remove stopwords, apply lemmatization."""
        tokens = word_tokenize(text)
        cleaned = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 1:
                lemma = self.lemmatizer.lemmatize(token)
                cleaned.append(lemma)
        return cleaned

    def _lemmatize_text(self, text: str) -> str:
        """Lemmatize all words in text for flexible matching.
        
        Converts 'paining' → 'pain', 'hurting' → 'hurt', 'aching' → 'ache', etc.
        so keyword matching works with natural language variations.
        """
        tokens = word_tokenize(text.lower())
        lemmatized = []
        for token in tokens:
            # Try verb lemmatization first (paining→pain), then noun
            verb_lemma = self.lemmatizer.lemmatize(token, pos='v')
            if verb_lemma != token:
                lemmatized.append(verb_lemma)
            else:
                lemmatized.append(self.lemmatizer.lemmatize(token))
        return ' '.join(lemmatized)

    def _words_in_proximity(self, words: List[str], text_tokens: List[str], window: int = 6) -> bool:
        """Check if all words appear within a proximity window in the text.
        
        Handles cases like 'head is paining' matching 'head pain' by checking
        if 'head' and 'pain' appear within 6 words of each other.
        """
        if len(words) == 1:
            return words[0] in text_tokens

        # Find positions of each keyword word in the text
        positions = {}
        for word in words:
            positions[word] = [i for i, t in enumerate(text_tokens) if t == word]
            if not positions[word]:
                return False  # Word not found at all

        # Check if any combination of positions fits within the window
        # For 2-word keywords (most common case)
        if len(words) == 2:
            for p1 in positions[words[0]]:
                for p2 in positions[words[1]]:
                    if abs(p1 - p2) <= window:
                        return True
            return False

        # For 3+ word keywords, check if all appear within a window
        from itertools import product
        all_positions = [positions[w] for w in words]
        for combo in product(*all_positions):
            if max(combo) - min(combo) <= window:
                return True
        return False

    def _keyword_match(self, text: str) -> Dict[str, float]:
        """Smart keyword matching with lemmatization and proximity-based matching.
        
        Three-pass matching strategy:
        1. Exact substring match on raw text (highest confidence)
        2. Exact substring match on lemmatized text (catches 'paining'→'pain')
        3. Proximity match: multi-word keywords matched within a word window
           (catches 'head is paining' → matches 'head pain')
        """
        matches = {}
        text_lower = text.lower()
        text_lemmatized = self._lemmatize_text(text_lower)
        lemma_tokens = text_lemmatized.split()

        for symptom_key, keywords in SYMPTOM_KEYWORDS.items():
            best_score = 0.0

            for keyword in keywords:
                keyword_lower = keyword.lower()
                keyword_words = keyword_lower.split()
                word_count = len(keyword_words)

                # Pass 1: Exact substring match on raw text (highest confidence)
                if keyword_lower in text_lower:
                    score = min(0.7 + (word_count * 0.1), 1.0)
                    best_score = max(best_score, score)
                    continue

                # Pass 2: Exact substring match on lemmatized text
                keyword_lemmatized = self._lemmatize_text(keyword_lower)
                if keyword_lemmatized in text_lemmatized:
                    score = min(0.65 + (word_count * 0.1), 0.95)
                    best_score = max(best_score, score)
                    continue

                # Pass 3: Proximity match on lemmatized tokens
                # For multi-word keywords, check if all lemmatized words
                # appear near each other in the text
                lemma_keyword_words = keyword_lemmatized.split()
                if word_count >= 2:
                    if self._words_in_proximity(lemma_keyword_words, lemma_tokens):
                        score = min(0.6 + (word_count * 0.1), 0.9)
                        best_score = max(best_score, score)

                # Pass 3b: Partial multi-word match — if most words from a
                # multi-word keyword appear in the text (not necessarily near
                # each other), assign a reduced confidence score. This catches
                # cases like "my body is hurting everywhere" matching the keyword
                # "whole body hurts" when exact proximity fails.
                if word_count >= 2 and best_score == 0:
                    # Filter out stopwords from the matching requirement to avoid "ca n't" triggering everything
                    significant_keyword_words = [w for w in lemma_keyword_words if w not in self.stop_words and len(w) > 1]
                    sig_word_count = len(significant_keyword_words)
                    
                    if sig_word_count > 0:
                        matched_sig_words = [w for w in significant_keyword_words if w in lemma_tokens]
                        ratio = len(matched_sig_words) / sig_word_count
                        
                        # At least 2 significant words must match, unless the keyword only has 1 significant word
                        # In which case, we don't do partial match (handled by Pass 1 & 2)
                        if len(matched_sig_words) >= 2 and ratio >= 0.5:
                            score = round(0.45 + (ratio * 0.2), 3)
                            best_score = max(best_score, score)

            if best_score > 0:
                matches[symptom_key] = best_score

        return matches

    def _bert_semantic_match(self, text: str, threshold: float = 0.91) -> Dict[str, float]:
        """BERT-based semantic similarity matching.
        
        Threshold set to 0.91 — tight enough to filter out the high baseline
        cosine similarity (~0.85-0.89) that BioBERT assigns to all medical text,
        but low enough to catch genuinely similar descriptions. Combined with
        the BERT-only discount in analyze() (×0.65), a raw score of 0.91 yields
        ~0.59 final confidence — just above the 0.57 cutoff.
        """
        if not self.symptom_embeddings:
            return {}

        text_embedding = self._get_bert_embedding(text)
        if text_embedding is None:
            return {}

        matches = {}
        for symptom_key, symptom_embedding in self.symptom_embeddings.items():
            similarity = float(np.dot(text_embedding, symptom_embedding))
            if similarity >= threshold:
                matches[symptom_key] = round(similarity, 3)

        return matches

    def analyze(self, user_input: str) -> Dict:
        """
        Full analysis pipeline:
        1. Preprocess text with NLP
        2. Run keyword matching
        3. Run BERT semantic matching
        4. Combine results with weighted scoring
        """
        preprocessed = self._preprocess_text(user_input)
        tokens = self._tokenize_and_clean(preprocessed)

        # 1. Keyword matching
        keyword_matches = self._keyword_match(preprocessed)

        # 2. BERT semantic matching
        bert_matches = self._bert_semantic_match(user_input)

        # 3. Combine results
        all_symptoms = set(list(keyword_matches.keys()) + list(bert_matches.keys()))
        combined_results = {}

        for symptom in all_symptoms:
            kw_score = keyword_matches.get(symptom, 0.0)
            bert_score = bert_matches.get(symptom, 0.0)

            # Weighted combination: keyword matches are more reliable for exact matches,
            # BERT catches semantic/paraphrased descriptions
            if kw_score > 0 and bert_score > 0:
                # Both agree → high confidence
                combined_score = 0.6 * kw_score + 0.4 * bert_score
                method = "keyword + BERT"
            elif kw_score > 0:
                combined_score = kw_score
                method = "keyword"
            else:
                # Discount for BERT-only matches to reduce false positives,
                # but not so heavy that BERT matches never pass the 0.5 cutoff
                combined_score = bert_score * 0.65
                method = "BERT semantic"

            # Filter out low-confidence matches.
            # Cutoff at 0.61 eliminates BERT-only noise (~0.59 range) while
            # preserving all keyword matches (0.65+) and very strong BERT matches.
            if combined_score < 0.61:
                continue

            combined_results[symptom] = {
                "confidence": round(combined_score, 3),
                "method": method,
                "keyword_score": round(kw_score, 3),
                "bert_score": round(bert_score, 3)
            }

        # Sort by confidence descending
        sorted_results = dict(
            sorted(combined_results.items(), key=lambda x: x[1]["confidence"], reverse=True)
        )

        return {
            "extracted_symptoms": sorted_results,
            "preprocessed_text": preprocessed,
            "tokens": tokens,
            "nlp_method": "BERT + Keyword Hybrid" if self.bert_model else "Keyword Only",
            "bert_available": self.bert_model is not None
        }
