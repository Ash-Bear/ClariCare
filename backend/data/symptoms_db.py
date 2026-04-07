"""
ClariCare - Comprehensive Symptom Database
Maps symptoms to risk levels, possible causes, specialists, and lifestyle advice.
"""

# ─── Symptom keyword sets ───────────────────────────────────────────────────────

SYMPTOM_KEYWORDS = {
    "headache": ["headache", "head pain", "migraine", "head hurts", "throbbing head", "head pressure",
                  "head paining", "head is paining", "head is hurting", "head ache", "head aching",
                  "pain in head", "pain in my head", "paining head"],
    "fever": ["fever", "high temperature", "chills", "feverish", "burning up", "hot forehead"],
    "cough": ["cough", "coughing", "dry cough", "wet cough", "persistent cough", "hacking cough"],
    "fatigue": ["fatigue", "tired", "exhaustion", "lethargy", "low energy", "no energy", "worn out", "sleepy"],
    "nausea": ["nausea", "nauseous", "feel sick", "queasy", "want to vomit", "upset stomach"],
    "vomiting": ["vomiting", "throwing up", "vomit", "puking"],
    "dizziness": ["dizziness", "dizzy", "lightheaded", "light headed", "vertigo", "room spinning", "faint"],
    "chest_pain": ["chest pain", "chest tightness", "chest pressure", "heart pain", "angina", "chest hurts"],
    "shortness_of_breath": ["shortness of breath", "breathless", "difficulty breathing", "can't breathe",
                            "hard to breathe", "breathing difficulty", "gasping"],
    "stomach_pain": ["stomach pain", "abdominal pain", "belly ache", "stomach ache", "stomach cramps",
                     "abdominal cramps", "tummy ache"],
    "sore_throat": ["sore throat", "throat pain", "throat hurts", "scratchy throat", "painful swallowing"],
    "runny_nose": ["runny nose", "stuffy nose", "nasal congestion", "blocked nose", "sneezing", "sniffles"],
    "body_aches": ["body aches", "muscle pain", "body pain", "aching", "sore muscles", "joint pain",
                   "muscle ache"],
    "rash": ["rash", "skin rash", "hives", "itchy skin", "skin irritation", "red skin", "bumps on skin",
             "skin breakout"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool", "frequent bowel", "running stomach"],
    "constipation": ["constipation", "constipated", "hard stool", "difficulty passing stool",
                     "irregular bowel"],
    "back_pain": ["back pain", "lower back pain", "upper back pain", "backache", "spine pain",
                  "back hurts"],
    "insomnia": ["insomnia", "can't sleep", "sleepless", "trouble sleeping", "difficulty sleeping",
                 "sleep problems", "restless nights"],
    "anxiety": ["anxiety", "anxious", "worried", "panic", "nervousness", "nervous", "restless",
                "panic attack", "stress"],
    "depression": ["depression", "depressed", "sad", "hopeless", "no motivation", "feeling low",
                   "down", "loss of interest"],
    "blurred_vision": ["blurred vision", "blurry vision", "vision problems", "can't see clearly",
                       "fuzzy vision", "double vision"],
    "swelling": ["swelling", "swollen", "puffy", "inflammation", "edema", "bloating"],
    "weight_loss": ["weight loss", "losing weight", "unintentional weight loss", "unexplained weight loss"],
    "weight_gain": ["weight gain", "gaining weight", "increased weight"],
    "frequent_urination": ["frequent urination", "urinating often", "peeing a lot", "overactive bladder"],
    "blood_in_urine": ["blood in urine", "hematuria", "red urine", "bloody urine"],
    "numbness": ["numbness", "tingling", "pins and needles", "loss of sensation", "numb"],
    "palpitations": ["palpitations", "heart racing", "rapid heartbeat", "heart pounding",
                     "irregular heartbeat", "heart flutter"],
    "skin_discoloration": ["skin discoloration", "yellow skin", "jaundice", "pale skin", "bluish skin"],
    "ear_pain": ["ear pain", "earache", "ear infection", "ear hurts", "ringing in ears", "tinnitus"],
    "eye_pain": ["eye pain", "eye strain", "red eyes", "watery eyes", "itchy eyes"],
    "difficulty_swallowing": ["difficulty swallowing", "dysphagia", "trouble swallowing",
                              "food stuck in throat"],
    "loss_of_appetite": ["loss of appetite", "no appetite", "not hungry", "reduced appetite"],
    "excessive_thirst": ["excessive thirst", "very thirsty", "always thirsty", "polydipsia"],
    "hair_loss": ["hair loss", "hair falling", "thinning hair", "bald spots", "alopecia"],
    "bruising": ["bruising", "easy bruising", "unexplained bruises", "bruise easily"],
}

# ─── Risk classification ────────────────────────────────────────────────────────

RISK_LEVELS = {
    "low": {
        "symptoms": [
            "headache", "fatigue", "runny_nose", "sore_throat", "body_aches",
            "insomnia", "constipation", "back_pain", "ear_pain", "eye_pain",
            "hair_loss", "weight_gain", "loss_of_appetite"
        ],
        "color": "#22c55e",
        "label": "Low Risk",
        "urgency": "These symptoms are commonly manageable with self-care and lifestyle adjustments."
    },
    "medium": {
        "symptoms": [
            "fever", "cough", "nausea", "vomiting", "dizziness", "stomach_pain",
            "rash", "diarrhea", "anxiety", "depression", "blurred_vision",
            "swelling", "frequent_urination", "numbness", "palpitations",
            "difficulty_swallowing", "excessive_thirst", "bruising", "skin_discoloration",
            "weight_loss"
        ],
        "color": "#f59e0b",
        "label": "Medium Risk",
        "urgency": "These symptoms may benefit from professional evaluation. Consider scheduling an appointment."
    },
    "high": {
        "symptoms": [
            "chest_pain", "shortness_of_breath", "blood_in_urine"
        ],
        "color": "#ef4444",
        "label": "High Risk",
        "urgency": "These symptoms warrant prompt medical attention. Please consult a healthcare professional soon."
    }
}

# ─── Symptom-to-specialist mapping ──────────────────────────────────────────────

SPECIALIST_MAP = {
    "headache": {"specialist": "Neurologist", "icon": "🧠"},
    "fever": {"specialist": "General Physician / Internist", "icon": "🩺"},
    "cough": {"specialist": "Pulmonologist", "icon": "🫁"},
    "fatigue": {"specialist": "General Physician / Internist", "icon": "🩺"},
    "nausea": {"specialist": "Gastroenterologist", "icon": "🏥"},
    "vomiting": {"specialist": "Gastroenterologist", "icon": "🏥"},
    "dizziness": {"specialist": "Neurologist / ENT Specialist", "icon": "🧠"},
    "chest_pain": {"specialist": "Cardiologist", "icon": "❤️"},
    "shortness_of_breath": {"specialist": "Pulmonologist / Cardiologist", "icon": "🫁"},
    "stomach_pain": {"specialist": "Gastroenterologist", "icon": "🏥"},
    "sore_throat": {"specialist": "ENT Specialist", "icon": "👂"},
    "runny_nose": {"specialist": "ENT Specialist / Allergist", "icon": "👂"},
    "body_aches": {"specialist": "Rheumatologist / Orthopedist", "icon": "🦴"},
    "rash": {"specialist": "Dermatologist", "icon": "🩹"},
    "diarrhea": {"specialist": "Gastroenterologist", "icon": "🏥"},
    "constipation": {"specialist": "Gastroenterologist", "icon": "🏥"},
    "back_pain": {"specialist": "Orthopedist / Physiotherapist", "icon": "🦴"},
    "insomnia": {"specialist": "Sleep Specialist / Psychiatrist", "icon": "😴"},
    "anxiety": {"specialist": "Psychiatrist / Psychologist", "icon": "🧘"},
    "depression": {"specialist": "Psychiatrist / Psychologist", "icon": "🧘"},
    "blurred_vision": {"specialist": "Ophthalmologist", "icon": "👁️"},
    "swelling": {"specialist": "General Physician / Rheumatologist", "icon": "🩺"},
    "weight_loss": {"specialist": "Endocrinologist / General Physician", "icon": "⚖️"},
    "weight_gain": {"specialist": "Endocrinologist / Nutritionist", "icon": "⚖️"},
    "frequent_urination": {"specialist": "Urologist / Endocrinologist", "icon": "🏥"},
    "blood_in_urine": {"specialist": "Urologist / Nephrologist", "icon": "🏥"},
    "numbness": {"specialist": "Neurologist", "icon": "🧠"},
    "palpitations": {"specialist": "Cardiologist", "icon": "❤️"},
    "skin_discoloration": {"specialist": "Dermatologist / Hepatologist", "icon": "🩹"},
    "ear_pain": {"specialist": "ENT Specialist", "icon": "👂"},
    "eye_pain": {"specialist": "Ophthalmologist", "icon": "👁️"},
    "difficulty_swallowing": {"specialist": "ENT Specialist / Gastroenterologist", "icon": "👂"},
    "loss_of_appetite": {"specialist": "General Physician / Gastroenterologist", "icon": "🩺"},
    "excessive_thirst": {"specialist": "Endocrinologist", "icon": "⚖️"},
    "hair_loss": {"specialist": "Dermatologist / Endocrinologist", "icon": "🩹"},
    "bruising": {"specialist": "Hematologist", "icon": "🩸"},
}

# ─── Possible causes (non-diagnostic) ───────────────────────────────────────────

POSSIBLE_CAUSES = {
    "headache": [
        "tension or stress", "dehydration", "eye strain from screens",
        "irregular sleep patterns", "dietary factors"
    ],
    "fever": [
        "viral or bacterial infections", "inflammatory conditions",
        "post-vaccination response", "environmental heat exposure"
    ],
    "cough": [
        "post-nasal drip", "seasonal allergies", "dry air exposure",
        "respiratory irritants", "common cold"
    ],
    "fatigue": [
        "insufficient sleep", "high stress levels", "poor nutrition",
        "sedentary lifestyle", "dehydration"
    ],
    "nausea": [
        "dietary factors", "motion sensitivity", "stress or anxiety",
        "medication side effects", "dehydration"
    ],
    "vomiting": [
        "food-related issues", "viral gastroenteritis", "motion sickness",
        "medication effects", "overeating"
    ],
    "dizziness": [
        "sudden position changes", "low blood sugar", "dehydration",
        "inner ear imbalance", "stress or anxiety"
    ],
    "chest_pain": [
        "muscle strain", "acid reflux", "anxiety or panic",
        "physical exertion", "respiratory issues"
    ],
    "shortness_of_breath": [
        "physical exertion", "anxiety or panic", "environmental allergens",
        "high altitude", "poor air quality"
    ],
    "stomach_pain": [
        "dietary factors", "stress", "irregular eating habits",
        "food intolerances", "gastric irritation"
    ],
    "sore_throat": [
        "viral infections", "dry air", "post-nasal drip",
        "voice strain", "seasonal allergies"
    ],
    "runny_nose": [
        "seasonal allergies", "common cold", "environmental irritants",
        "temperature changes", "dust exposure"
    ],
    "body_aches": [
        "physical overexertion", "poor posture", "stress tension",
        "inadequate rest", "weather changes"
    ],
    "rash": [
        "allergic reactions", "skin irritants", "heat exposure",
        "contact with new products", "insect bites"
    ],
    "diarrhea": [
        "dietary changes", "food intolerance", "stress",
        "contaminated food or water", "viral gastroenteritis"
    ],
    "constipation": [
        "low fiber diet", "dehydration", "sedentary lifestyle",
        "dietary changes", "stress"
    ],
    "back_pain": [
        "poor posture", "prolonged sitting", "muscle strain",
        "improper lifting", "lack of exercise"
    ],
    "insomnia": [
        "stress or anxiety", "screen time before bed", "caffeine intake",
        "irregular sleep schedule", "environmental noise"
    ],
    "anxiety": [
        "work or life stress", "caffeine overconsumption", "lack of sleep",
        "major life changes", "nutrient deficiencies"
    ],
    "depression": [
        "prolonged stress", "social isolation", "seasonal changes",
        "major life events", "sleep disturbances"
    ],
    "blurred_vision": [
        "eye strain", "prolonged screen use", "fatigue",
        "dry eyes", "incorrect prescription"
    ],
    "swelling": [
        "prolonged standing or sitting", "dietary sodium", "physical injury",
        "hormonal changes", "allergic reactions"
    ],
    "weight_loss": [
        "changes in diet or appetite", "increased physical activity",
        "stress or emotional factors", "metabolic changes"
    ],
    "weight_gain": [
        "dietary changes", "reduced physical activity", "stress eating",
        "hormonal fluctuations", "medication effects"
    ],
    "frequent_urination": [
        "high fluid intake", "caffeine or alcohol consumption",
        "stress or anxiety", "cold weather", "dietary factors"
    ],
    "blood_in_urine": [
        "vigorous exercise", "urinary tract irritation",
        "dietary factors (beets/berries)", "dehydration"
    ],
    "numbness": [
        "poor circulation from position", "prolonged pressure on nerves",
        "cold exposure", "repetitive motion", "vitamin deficiencies"
    ],
    "palpitations": [
        "caffeine or stimulants", "stress or anxiety", "physical exertion",
        "dehydration", "lack of sleep"
    ],
    "skin_discoloration": [
        "sun exposure", "dietary factors", "bruising",
        "cosmetic reactions", "circulation changes"
    ],
    "ear_pain": [
        "pressure changes", "water exposure", "loud noise exposure",
        "jaw tension", "common cold"
    ],
    "eye_pain": [
        "screen fatigue", "dry eyes", "bright light exposure",
        "contact lens irritation", "sinus pressure"
    ],
    "difficulty_swallowing": [
        "dry throat", "eating too quickly", "acid reflux",
        "throat tension", "cold or sore throat"
    ],
    "loss_of_appetite": [
        "stress or emotional distress", "medication effects",
        "irregular meal schedule", "dehydration", "fatigue"
    ],
    "excessive_thirst": [
        "dehydration", "high sodium diet", "physical activity",
        "dry environment", "medication effects"
    ],
    "hair_loss": [
        "stress", "nutritional deficiencies", "hormonal changes",
        "heat styling damage", "seasonal shedding"
    ],
    "bruising": [
        "minor physical impacts", "aging", "medication effects",
        "nutritional factors", "sun damage"
    ],
}

# ─── Lifestyle advice ───────────────────────────────────────────────────────────

LIFESTYLE_ADVICE = {
    "headache": [
        "Stay well-hydrated throughout the day",
        "Take regular breaks from screen time (20-20-20 rule)",
        "Practice stress-reduction techniques like deep breathing",
        "Maintain a consistent sleep schedule"
    ],
    "fever": [
        "Rest and stay hydrated with water and clear fluids",
        "Wear light, breathable clothing",
        "Monitor your temperature periodically",
        "Avoid strenuous physical activity until recovered"
    ],
    "cough": [
        "Stay hydrated with warm fluids like herbal tea",
        "Use a humidifier to add moisture to the air",
        "Avoid exposure to smoke and air pollutants",
        "Honey in warm water may help soothe the throat"
    ],
    "fatigue": [
        "Aim for 7-9 hours of quality sleep each night",
        "Incorporate light exercise like walking into your routine",
        "Eat balanced meals with whole grains, proteins, and vegetables",
        "Limit caffeine, especially in the afternoon and evening"
    ],
    "nausea": [
        "Eat small, frequent meals rather than large ones",
        "Try ginger tea or peppermint tea",
        "Avoid strong odors and greasy foods",
        "Stay hydrated with small sips of clear fluids"
    ],
    "vomiting": [
        "Rest the stomach, then slowly reintroduce clear fluids",
        "Try the BRAT diet (bananas, rice, applesauce, toast)",
        "Avoid dairy, caffeine, and spicy foods temporarily",
        "Replenish electrolytes with oral rehydration solutions"
    ],
    "dizziness": [
        "Move slowly when changing positions (sitting to standing)",
        "Stay hydrated and maintain stable blood sugar",
        "Avoid sudden head movements",
        "Sit or lie down when feeling dizzy to prevent falls"
    ],
    "chest_pain": [
        "Avoid heavy physical exertion until evaluated",
        "Practice calm, deep breathing exercises",
        "Reduce caffeine and tobacco intake",
        "Seek immediate medical attention if pain is severe or persistent"
    ],
    "shortness_of_breath": [
        "Practice pursed-lip breathing techniques",
        "Avoid known allergens and irritants",
        "Maintain good posture to open airways",
        "Seek immediate help if breathing difficulty is severe"
    ],
    "stomach_pain": [
        "Eat smaller, more frequent meals",
        "Avoid spicy, fatty, or acidic foods",
        "Stay hydrated and try warm peppermint tea",
        "Practice stress management techniques"
    ],
    "sore_throat": [
        "Gargle with warm salt water several times a day",
        "Drink warm fluids and stay hydrated",
        "Use throat lozenges for comfort",
        "Rest your voice when possible"
    ],
    "runny_nose": [
        "Use saline nasal sprays for relief",
        "Stay hydrated with warm fluids",
        "Use a humidifier in dry environments",
        "Identify and reduce exposure to allergens"
    ],
    "body_aches": [
        "Gentle stretching and light movement can help",
        "Apply warm compresses to sore areas",
        "Ensure adequate rest and recovery time",
        "Stay hydrated and consider an Epsom salt bath"
    ],
    "rash": [
        "Avoid scratching the affected area",
        "Use gentle, fragrance-free skin products",
        "Keep the area clean and moisturized",
        "Note any new products or exposures that may be triggers"
    ],
    "diarrhea": [
        "Stay hydrated with water and electrolyte drinks",
        "Follow the BRAT diet temporarily",
        "Avoid dairy, caffeine, and high-fiber foods",
        "Wash hands frequently to prevent spread"
    ],
    "constipation": [
        "Increase fiber intake with fruits, vegetables, and whole grains",
        "Drink plenty of water throughout the day",
        "Engage in regular physical activity",
        "Establish a regular bathroom routine"
    ],
    "back_pain": [
        "Maintain good posture while sitting and standing",
        "Take breaks from prolonged sitting every 30 minutes",
        "Strengthen core muscles with gentle exercises",
        "Use proper lifting techniques (bend at the knees)"
    ],
    "insomnia": [
        "Maintain a consistent sleep and wake schedule",
        "Create a relaxing bedtime routine",
        "Limit screen time at least 1 hour before bed",
        "Keep your bedroom cool, dark, and quiet"
    ],
    "anxiety": [
        "Practice daily mindfulness or meditation",
        "Engage in regular physical exercise",
        "Limit caffeine and alcohol intake",
        "Consider journaling to process your thoughts"
    ],
    "depression": [
        "Maintain social connections, even when it feels difficult",
        "Engage in activities you used to enjoy",
        "Get regular sunlight exposure and physical activity",
        "Consider speaking with a mental health professional"
    ],
    "blurred_vision": [
        "Follow the 20-20-20 rule for screen breaks",
        "Ensure proper lighting when reading or working",
        "Keep eyes lubricated with artificial tears if dry",
        "Schedule regular comprehensive eye exams"
    ],
    "swelling": [
        "Elevate the affected area when possible",
        "Reduce sodium intake in your diet",
        "Stay active with gentle movement",
        "Apply cold compresses for acute swelling"
    ],
    "weight_loss": [
        "Ensure you're eating balanced, nutrient-dense meals",
        "Track your caloric intake to ensure adequacy",
        "Manage stress that may affect appetite",
        "Consult with a nutritionist for personalized guidance"
    ],
    "weight_gain": [
        "Focus on whole, unprocessed foods",
        "Increase daily physical activity gradually",
        "Manage emotional eating through mindful eating practices",
        "Stay hydrated — thirst can mimic hunger"
    ],
    "frequent_urination": [
        "Monitor your fluid intake, especially before bedtime",
        "Reduce caffeine and alcohol consumption",
        "Practice pelvic floor exercises",
        "Track frequency to share with your healthcare provider"
    ],
    "blood_in_urine": [
        "Increase water intake to stay well-hydrated",
        "Avoid strenuous exercise temporarily",
        "Avoid irritants like caffeine and spicy foods",
        "Seek prompt medical evaluation"
    ],
    "numbness": [
        "Change positions frequently to improve circulation",
        "Stretch regularly, especially during desk work",
        "Ensure adequate intake of B vitamins",
        "Avoid repetitive motions without breaks"
    ],
    "palpitations": [
        "Reduce caffeine, nicotine, and alcohol intake",
        "Practice deep breathing and relaxation techniques",
        "Get regular, moderate exercise",
        "Maintain consistent sleep patterns"
    ],
    "skin_discoloration": [
        "Use broad-spectrum sunscreen daily",
        "Stay hydrated and maintain good nutrition",
        "Note any new medications that could cause changes",
        "Consult a dermatologist for persistent changes"
    ],
    "ear_pain": [
        "Avoid inserting objects into the ear canal",
        "Keep ears dry after swimming or bathing",
        "Use ear protection in loud environments",
        "Apply a warm cloth to the affected ear for comfort"
    ],
    "eye_pain": [
        "Take regular breaks from screens and close work",
        "Ensure adequate lighting in your workspace",
        "Use artificial tears for dry eye relief",
        "Wear UV-protective sunglasses outdoors"
    ],
    "difficulty_swallowing": [
        "Eat slowly and chew food thoroughly",
        "Take smaller bites and sips",
        "Stay upright during and after meals",
        "Stay hydrated to keep the throat moist"
    ],
    "loss_of_appetite": [
        "Try eating smaller, more frequent meals",
        "Choose nutrient-dense foods when you do eat",
        "Stay physically active to stimulate appetite",
        "Create a pleasant, stress-free eating environment"
    ],
    "excessive_thirst": [
        "Track your daily water intake",
        "Reduce salty and processed food consumption",
        "Monitor for other symptoms like frequent urination",
        "Carry water with you throughout the day"
    ],
    "hair_loss": [
        "Eat a balanced diet rich in iron, zinc, and biotin",
        "Manage stress through relaxation techniques",
        "Avoid harsh chemical treatments and excessive heat styling",
        "Be gentle when brushing and avoid tight hairstyles"
    ],
    "bruising": [
        "Protect your skin from impacts where possible",
        "Ensure adequate vitamin C and K in your diet",
        "Apply cold compresses to reduce swelling of new bruises",
        "Note any medications that may increase bruising"
    ],
}

# ─── BERT-enhanced symptom descriptions for semantic matching ────────────────────

SYMPTOM_DESCRIPTIONS = {
    "headache": "pain or discomfort in any part of the head, ranging from sharp to dull, throbbing to constant pressure",
    "fever": "elevated body temperature above normal, often accompanied by chills, sweating, and general malaise",
    "cough": "sudden expulsion of air from the lungs, which may be dry and irritating or productive with mucus",
    "fatigue": "persistent feeling of tiredness, exhaustion, or lack of energy that doesn't improve with rest",
    "nausea": "sensation of unease and discomfort in the stomach with an urge to vomit",
    "vomiting": "forceful expulsion of stomach contents through the mouth",
    "dizziness": "feeling of lightheadedness, unsteadiness, or sensation that the surroundings are spinning",
    "chest_pain": "discomfort, pressure, squeezing, or pain in the chest area",
    "shortness_of_breath": "difficulty breathing, feeling of not getting enough air, breathlessness",
    "stomach_pain": "pain or discomfort in the abdominal area, including cramping, bloating, or sharp pain",
    "sore_throat": "pain, scratchiness, or irritation of the throat that often worsens when swallowing",
    "runny_nose": "excess nasal discharge, congestion, sneezing, or blocked nasal passages",
    "body_aches": "generalized muscle or joint pain throughout the body, soreness, and stiffness",
    "rash": "changes in skin appearance including redness, bumps, itching, or irritation",
    "diarrhea": "frequent loose or watery bowel movements",
    "constipation": "infrequent bowel movements or difficulty passing stool",
    "back_pain": "pain or discomfort in the upper or lower back, spine area",
    "insomnia": "difficulty falling asleep, staying asleep, or getting restful sleep",
    "anxiety": "persistent worry, nervousness, restlessness, or feelings of panic and dread",
    "depression": "persistent feelings of sadness, hopelessness, loss of interest, or emotional numbness",
    "blurred_vision": "inability to see clearly, fuzzy or doubled images, difficulty focusing",
    "swelling": "abnormal enlargement of body parts due to fluid accumulation or inflammation",
    "weight_loss": "unintended decrease in body weight over time",
    "weight_gain": "unintended increase in body weight over time",
    "frequent_urination": "needing to urinate more often than usual",
    "blood_in_urine": "presence of blood or red coloring in urine",
    "numbness": "loss of sensation, tingling, or pins and needles feeling in body parts",
    "palpitations": "awareness of heartbeat being rapid, irregular, pounding, or fluttering",
    "skin_discoloration": "changes in skin color including yellowing, paleness, or unusual patches",
    "ear_pain": "pain, discomfort, or ringing in one or both ears",
    "eye_pain": "pain, discomfort, redness, or irritation in or around the eyes",
    "difficulty_swallowing": "trouble or pain when swallowing food, liquids, or saliva",
    "loss_of_appetite": "reduced desire to eat or lack of hunger",
    "excessive_thirst": "abnormally strong or persistent feeling of thirst",
    "hair_loss": "thinning or loss of hair from the head or body",
    "bruising": "discoloration of skin from broken blood vessels, may appear without clear cause",
}
