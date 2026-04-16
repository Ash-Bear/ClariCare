# ClariCare 🏥
 
**An AI-Powered Medical Symptom Analysis System**
 
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
 
---
 
## 📋 Overview
 
ClariCare is a **hybrid AI system** that combines **deep learning** (BioBERT) with **expert rule-based logic** to provide intelligent, safe, and explainable medical symptom analysis. 
 
When users describe their symptoms, ClariCare:
- 🔍 **Extracts symptoms** using semantic understanding + keyword matching
- ⚠️ **Classifies health risk levels** (Low, Medium, High, Critical)
- 👨‍⚕️ **Recommends appropriate specialists** (Cardiologist, Neurologist, etc.)
- 💡 **Provides actionable guidance** and safety warnings
- 📊 **Achieves 99.18% accuracy** with deterministic, explainable decisions
**Key Innovation**: Unlike black-box AI, ClariCare uses a two-pronged hybrid approach where rule-based logic guardrails prevent unsafe recommendations while deep learning provides semantic flexibility.
 
---
 
## 🎯 Features
 
### Core Capabilities
- ✅ **Conversational AI** - Natural multi-turn dialogue using Finite State Machine
- ✅ **Hybrid NLP Engine** - Keyword matching + BioBERT semantic embeddings (768-dim vectors)
- ✅ **Risk Classification** - Set theory + scalar modifiers for dangerous symptom combinations
- ✅ **Specialist Routing** - Intelligent matching to appropriate medical professionals
- ✅ **Medical Safety** - Conservative thresholds (0.61 confidence floor) prioritize false negatives
- ✅ **Real-time Processing** - Sub-second symptom extraction and risk assessment
### Technical Highlights
- 🧠 **BioBERT Model** - Trained on 30M+ peer-reviewed medical papers (18B words)
- 🔐 **Deterministic Decisions** - All rules hardcoded and auditable
- 📈 **High Accuracy** - 99.18% accuracy, 76.11% F1-Score on test dataset
- 🚀 **Production Ready** - FastAPI backend, async processing, cloud-deployable
- 📱 **Modern Frontend** - HTML5,TailWind CSS,Vanilla js with real-time chat UI
- ---
 
## 📊 Performance Metrics
 
Evaluated on **31 conversational test inputs** with comprehensive medical scenarios:
 
```
════════════════════════════════════
Accuracy:   99.18%  ✅
Precision:  70.49%  
Recall:     82.69%  
F1-Score:   76.11%  ✅
════════════════════════════════════
```
- ---
## 📦 Dataset & Knowledge Sources
 
### Dataset 1: BioBERT Pre-training Corpus
- **Source**: PubMed (4.5B words) + PMC (13.5B words)
- **Total**: 18 billion words from 30M+ peer-reviewed papers
- **Domain**: Biomedical/medical research literature
- **Purpose**: Train semantic understanding of medical terminology
- **Model**: `dmis-lab/biobert-base-cased-v1.2` (HuggingFace)
### Dataset 2: ClariCare Symptom Database
- **Source**: Custom hand-curated expert database
- **Structure**: Nested Python Dictionary (not CSV)
- **Contents**: 100+ symptoms with:
  - Clinical aliases (e.g., "dyspnea" → "can't breathe")
  - Risk levels (Low, Medium, High, Critical)
  - Specialist recommendations
  - Medical guidance & warnings
- **Purpose**: Rule-based clinical decision making & safety guardrails

- - ---
## 🤝 Contributing
 
We welcome contributions! Please follow these steps:
 
1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**
### Development Guidelines
- Follow PEP 8 coding standards
- Add tests for new features
- Update documentation
- Ensure all tests pass before submitting PR
---
 
## 📝 Citation
 
If you use ClariCare in research, please cite:
 
```bibtex
@software{claricare2026,
  title={ClariCare: Hybrid AI System for Medical Symptom Analysis},
  author={Ash-Bear},
  year={2026},
  url={https://github.com/Ash-Bear/ClariCare}
}
```
 
---
## ⚖️ Disclaimer
 
**Medical Advisory**
 
ClariCare is an educational tool designed to help patients understand their symptoms and determine when to seek professional medical care. It is **not** a medical diagnosis system.
 
**Important Notices:**
- ⚠️ This system is for **informational purposes only**
- ⚠️ Do not rely solely on this system for medical decisions
- ⚠️ Always consult qualified healthcare professionals
- ⚠️ In emergencies, call 112 (or your local emergency number)
- ⚠️ This system does not replace professional medical advice
**Liability**: The developers and authors of ClariCare are not responsible for any adverse outcomes resulting from the use or misuse of this system.
 
---
 
## 👥 Support & Contact
 
- 📧 **Email**: aakanshbaghel.123@gmail.com
- 
---
 
## 🙏 Acknowledgments
 
- **BioBERT Authors** (Lee et al., Korea University) for the medical BERT model
- **HuggingFace** for the Transformers library
- **FastAPI** community for the excellent web framework
- **All contributors** who helped improve ClariCare
---
