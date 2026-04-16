"""
ClariCare - Comprehensive Symptom Database (v3 — Expanded)
Maps symptoms to risk levels, possible causes, specialists, and lifestyle advice.
"""

# ─── Symptom keyword sets ───────────────────────────────────────────────────────
# Each entry has broad, colloquial, and clinical terms to maximise match coverage.

SYMPTOM_KEYWORDS = {
    # ── Head & Neurological ──────────────────────────────────────────────────────
    "headache": [
        "headache", "head pain", "head hurts", "head hurting", "head ache",
        "head aching", "head is paining", "head is hurting", "paining head",
        "pain in head", "pain in my head", "head pressure", "throbbing head",
        "pounding head", "head is heavy", "heavy head", "skull hurts",
        "top of head hurts", "temples hurting", "forehead pain", "forehead hurts",
        "pressure in head", "head feels tight", "tight head",
        "head killing me", "splitting headache", "my head", "bad headache",
        "terrible headache", "head is splitting", "head is throbbing",
        "pain in the head", "constant headache", "head paining",
    ],
    "migraine": [
        "migraine", "migraine headache", "severe headache", "one sided headache",
        "half head pain", "migraine attack", "aura", "visual aura", "light sensitivity headache",
        "throbbing headache", "pulsating headache", "headache with nausea",
        "headache with vomiting", "headache worse with light", "headache worse with sound",
        "nausea with headache", "vomiting with headache",
    ],

    "dizziness": [
        "dizziness", "dizzy", "lightheaded", "light headed", "vertigo",
        "room spinning", "spinning sensation", "faint", "feel like fainting",
        "about to faint", "unsteady", "loss of balance", "balance problems",
        "head rush", "giddy", "woozy", "swimmy head", "swaying", "off balance",
        "feeling dizzy", "feel dizzy", "everything spinning", "world is spinning",
        "head is spinning", "feeling faint", "feel faint", "almost fainted",
    ],
    "numbness": [
        "numbness", "tingling", "pins and needles", "loss of sensation", "numb",
        "numb hand", "numb feet", "numb fingers", "numb arm", "numb leg",
        "tingling in hand", "tingling in feet", "electric feeling", "dead feeling in limb",
        "can't feel my hand", "can't feel my feet", "hands asleep", "arms asleep",
    ],
    "tremors": [
        "tremors", "shaking", "trembling", "shaky hands", "hands shaking",
        "body shaking", "uncontrollable shaking", "shivering", "involuntary shaking",
        "shaky", "muscle twitching", "twitching", "spasm", "jerking", "convulsion",
    ],
    "memory_loss": [
        "memory loss", "forgetfulness", "forgetting things", "can't remember",
        "memory problems", "poor memory", "cognitive decline", "confusion",
        "brain fog", "mental fog", "foggy brain", "difficulty concentrating",
        "trouble focusing", "can't think clearly", "disorientation", "disoriented",
        "losing memory", "short term memory", "memory issues",
    ],

    # ── Chest & Heart ────────────────────────────────────────────────────────────
    "chest_pain": [
        "chest pain", "chest tightness", "chest pressure", "heart pain",
        "angina", "chest hurts", "pain in chest", "chest discomfort",
        "chest heaviness", "heavy chest", "burning in chest", "chest burning",
        "squeezing in chest", "chest squeeze", "pain radiating to arm",
        "left arm pain with chest", "jaw pain with chest",
        "chest is hurting", "chest is paining", "my chest hurts",
        "my chest is tight", "chest feels heavy", "heart hurts",
        "stabbing chest", "sharp chest pain", "dull chest pain",
    ],
    "shortness_of_breath": [
        "shortness of breath", "breathless", "difficulty breathing", "can't breathe",
        "hard to breathe", "breathing difficulty", "gasping", "unable to breathe",
        "labored breathing", "wheezing", "out of breath", "short of breath",
        "struggling to breathe", "air hunger", "suffocating feeling",
        "trouble breathing", "breath is short", "not getting enough air",
        "breathing problem", "breathing problems", "can not breathe",
        "breathing is hard", "hard time breathing", "can't breathe properly",
        "panting", "winded", "getting winded", "breathing heavy",
    ],
    "palpitations": [
        "palpitations", "heart racing", "rapid heartbeat", "heart pounding",
        "irregular heartbeat", "heart flutter", "heart skipping beats",
        "heart beating fast", "fast heart rate", "tachycardia", "racing heart",
        "heart flip flop", "fluttering in chest", "heart jumping",
        "feeling my heartbeat", "aware of heartbeat",
    ],

    # ── Fever & Infection ────────────────────────────────────────────────────────
    "fever": [
        "fever", "high temperature", "chills", "feverish", "burning up",
        "hot forehead", "temperature", "running a fever", "feeling hot",
        "body temperature high", "sweating with chills", "night sweats",
        "fever and chills", "having a fever", "temp is high", "raised temperature",
        "feeling feverish", "feel feverish", "sweating a lot",
        "body is hot", "my body is burning", "burning body", "high fever",
        "low grade fever", "mild fever", "slight fever", "body feels hot",
        "i have fever", "got fever", "having fever", "got a fever",
    ],
    "cough": [
        "cough", "coughing", "dry cough", "wet cough", "persistent cough",
        "hacking cough", "chesty cough", "productive cough", "mucus cough",
        "phlegm cough", "can't stop coughing", "constant coughing",
        "cough won't go away", "chronic cough", "morning cough", "barking cough",
        "whooping cough", "coughing fits", "cough with blood", "bloody cough",
        "i have a cough", "keep coughing", "been coughing", "bad cough",
        "terrible cough", "severe cough", "non stop coughing", "coughing a lot",
    ],
    "sore_throat": [
        "sore throat", "throat pain", "throat hurts", "scratchy throat",
        "painful swallowing", "throat irritation", "inflamed throat",
        "strep throat", "tonsil pain", "tonsils hurt", "tonsils swollen",
        "swollen tonsils", "throat ache", "burning throat", "raw throat",
        "painful throat", "throat burning", "throat swollen",
        "my throat hurts", "throat is hurting", "throat is sore",
        "throat is paining", "throat infection", "itchy throat",
    ],
    "runny_nose": [
        "runny nose", "stuffy nose", "nasal congestion", "blocked nose",
        "sneezing", "sniffles", "nose is running", "nose dripping",
        "postnasal drip", "post nasal drip", "nasal drip", "sinus congestion",
        "blocked sinuses", "nose blocked", "can't breathe through nose",
        "nose stuffed up", "watery nose", "constant sneezing",
    ],
    "cold_sores": [
        "cold sore", "blister on lip", "lip blister", "fever blister",
        "herpes labialis", "mouth blister", "blister around mouth",
        "lip ulcer", "sore on lip", "painful blister", "sores around mouth",
    ],

    # ── GI System ────────────────────────────────────────────────────────────────
    "stomach_pain": [
        "stomach pain", "abdominal pain", "belly ache", "stomach ache",
        "stomach cramps", "abdominal cramps", "tummy ache", "gut pain",
        "tummy pain", "abdomen hurts", "belly pain", "stomach hurting",
        "stomach is paining", "lower abdomen pain", "upper abdomen pain",
        "stomach feels tight", "stomach discomfort", "stomach pressure",
        "cramping in stomach", "sides are hurting", "pain in belly",
        "abdominal discomfort", "stomach is hurting", "pain under ribs",
        "my stomach hurts", "my stomach is hurting", "my tummy hurts",
        "stomach is killing me", "sharp stomach pain", "stomach is bad",
        "bad stomach", "stomach acting up", "stomach paining",
    ],
    "nausea": [
        "nausea", "nauseous", "feel sick", "queasy", "want to vomit",
        "upset stomach", "sick feeling", "feeling sick", "stomach is upset",
        "want to throw up", "about to vomit", "urge to vomit", "feeling queasy",
        "stomach is rolling", "motion sickness", "sea sickness",
        "sick to my stomach", "feeling ill", "feel like throwing up",
        "feel nauseous", "feeling nauseous", "nauseated", "feel nauseated",
        "might throw up", "going to throw up", "tummy upset", "really nauseous",
        "very nauseous", "extremely nauseous", "stomach feels weird",
    ],
    "vomiting": [
        "vomiting", "throwing up", "vomit", "puking", "retching",
        "threw up", "been vomiting", "can't keep food down", "emesis",
        "keep vomiting", "vomiting repeatedly", "vomiting blood", "blood in vomit",
        "throw up", "thrown up", "keep throwing up", "puke", "puked",
        "been throwing up", "vomited", "i vomited", "i threw up",
    ],
    "diarrhea": [
        "diarrhea", "loose stool", "watery stool", "frequent bowel", "running stomach",
        "loose motions", "watery poop", "frequent trips to bathroom",
        "stomach running", "runny stool", "liquid stool", "bowel movements frequent",
        "going to toilet often", "loose poop", "diarrhoea",
    ],
    "constipation": [
        "constipation", "constipated", "hard stool", "difficulty passing stool",
        "irregular bowel", "no bowel movement", "can't poop", "can't pass stool",
        "straining to poop", "hard to pass stool", "not going to toilet",
        "stomach not clearing", "bowel not moving",
    ],
    "heartburn": [
        "heartburn", "acid reflux", "acidity", "acid in throat", "burning in throat",
        "gerd", "indigestion", "acid indigestion", "burning after eating",
        "sour taste in mouth", "regurgitation", "belching", "burping acid",
        "chest burn after meal", "stomach acid", "stomach burning",
    ],
    "bloating": [
        "bloating", "bloated", "gassy", "gas", "flatulence",
        "stomach is bloated", "belly is bloated", "feel bloated",
        "stomach feels full", "trapped gas", "abdominal bloating",
        "distended abdomen", "stomach swollen", "stomach is puffed up",
    ],
    "loss_of_appetite": [
        "loss of appetite", "no appetite", "not hungry", "reduced appetite",
        "don't want to eat", "can't eat", "not feeling like eating",
        "food doesn't appeal", "no desire to eat", "loss of hunger",
        "not eating properly", "skipping meals", "don't feel like eating",
    ],

    # ── Musculoskeletal ──────────────────────────────────────────────────────────
    "body_aches": [
        "body aches", "muscle pain", "body pain", "sore muscles", "muscle ache",
        "whole body aches", "body is aching", "all over pain",
        "muscles are sore", "body soreness", "flu like aches", "generalized pain",
        "body is sore", "my whole body hurts", "everything hurts",
        "body hurts", "body hurting", "body is hurting", "body is paining",
        "muscles hurting", "muscles are hurting", "sore all over",
        "aching all over", "body feels sore", "my body hurts",
        "my muscles hurt", "my body is paining", "full body pain",
    ],
    "joint_pain": [
        "joint pain", "joint ache", "painful joints", "swollen joints",
        "arthritis", "arthritis pain", "knee pain", "hip pain",
        "shoulder pain", "elbow pain", "wrist pain", "ankle pain",
        "knuckle pain", "joint stiffness", "stiff joints", "joint swelling",
        "joints are swollen", "joints are painful",
    ],
    "back_pain": [
        "back pain", "lower back pain", "upper back pain", "backache",
        "spine pain", "back hurts", "my back hurts", "back is paining",
        "back is aching", "lumbar pain", "back soreness", "sore back",
        "slipped disc", "disc pain", "sciatica", "sciatic nerve pain",
        "shooting pain in back", "radiating back pain",
    ],
    "neck_pain": [
        "neck pain", "neck ache", "stiff neck", "neck stiffness",
        "neck is sore", "neck hurts", "cervical pain", "pain in neck",
        "neck is tight", "can't move neck", "neck tension", "torticollis",
    ],
    "muscle_weakness": [
        "muscle weakness", "weak muscles", "weakness in limbs",
        "arms feel weak", "legs feel weak", "can't lift things",
        "body feels weak", "feeling weak", "muscular weakness",
        "limb weakness", "loss of strength", "decreased strength",
    ],

    # ── Skin ────────────────────────────────────────────────────────────────────
    "rash": [
        "rash", "skin rash", "hives", "itchy skin", "skin irritation",
        "red skin", "bumps on skin", "skin breakout", "allergic rash",
        "skin reaction", "welts", "urticaria", "eczema flare",
        "red bumps", "red patches", "blisters on skin", "skin redness",
        "itchy rash", "raised welts",
    ],
    "skin_discoloration": [
        "skin discoloration", "yellow skin", "jaundice", "pale skin",
        "bluish skin", "skin turning yellow", "yellowing of skin",
        "skin looks yellow", "dark patches", "skin darkening",
        "skin is pale", "pallor", "skin color change", "cyanosis",
    ],
    "bruising": [
        "bruising", "easy bruising", "unexplained bruises", "bruise easily",
        "bruises appearing", "purple marks on skin", "black and blue marks",
        "blood blister", "contusion", "skin bruise",
    ],
    "hair_loss": [
        "hair loss", "hair falling", "thinning hair", "bald spots",
        "alopecia", "losing hair", "hair is falling out", "patches of hair loss",
        "hair falling in clumps", "hair thinning on top", "receding hair",
    ],
    "excessive_sweating": [
        "excessive sweating", "sweating too much", "profuse sweating",
        "sweating a lot", "night sweats", "hyperhidrosis", "sweaty palms",
        "soaking through clothes", "constant sweating", "cold sweats",
    ],

    # ── Mental Health ────────────────────────────────────────────────────────────
    "anxiety": [
        "anxiety", "anxious", "worried", "panic", "nervousness", "nervous",
        "restless", "panic attack", "stress", "stressed out", "feeling anxious",
        "heart beating fast with worry", "sweaty palms from anxiety",
        "overthinking", "can't stop worrying", "dread", "sense of doom",
        "racing thoughts", "tension", "wound up", "on edge",
        "feel anxious", "feeling nervous", "feel nervous", "very anxious",
        "really anxious", "panicking", "panicky", "feeling panicky",
        "really stressed", "very stressed", "feeling stressed",
    ],
    "depression": [
        "depression", "depressed", "sad", "hopeless", "no motivation",
        "feeling low", "down", "loss of interest", "feeling empty",
        "can't enjoy anything", "feeling worthless", "feeling sad",
        "crying a lot", "tearful", "unmotivated", "lost interest",
        "feeling blue", "melancholy", "profound sadness",
    ],
    "insomnia": [
        "insomnia", "can't sleep", "sleepless", "trouble sleeping",
        "difficulty sleeping", "sleep problems", "restless nights",
        "lying awake", "not able to sleep", "waking up at night",
        "broken sleep", "light sleeper", "poor sleep quality",
        "sleep disturbance", "unable to fall asleep", "waking up early",
        "not sleeping", "can not sleep", "unable to sleep", "no sleep",
        "haven't slept", "couldn't sleep", "hard to sleep", "sleep issue",
    ],
    "fatigue": [
        "fatigue", "tired", "exhaustion", "lethargy", "low energy",
        "no energy", "worn out", "sleepy", "drained", "always tired",
        "constantly tired", "tired all the time", "feeling drained",
        "no stamina", "exhausted", "feel exhausted", "burnt out",
        "sluggish", "heavy limbs", "run down",
        "very tired", "so tired", "really tired", "extremely tired",
        "feeling tired", "feel tired", "feeling exhausted", "really exhausted",
        "feel weak", "feeling weak", "weak and tired", "tired and weak",
        "fatigued", "feeling fatigued", "lack of energy", "energy less",
    ],

    # ── Eyes & Ears ──────────────────────────────────────────────────────────────
    "blurred_vision": [
        "blurred vision", "blurry vision", "vision problems", "can't see clearly",
        "fuzzy vision", "double vision", "diplopia", "vision is blurry",
        "hazy vision", "wavy vision", "distorted vision",
        "difficulty seeing", "text looks blurry", "vision is unclear",
    ],
    "eye_pain": [
        "eye pain", "eye strain", "red eyes", "watery eyes", "itchy eyes",
        "eyes hurt", "sore eyes", "eyes are burning", "burning eyes",
        "eye irritation", "eye discomfort", "eye pressure", "gritty eyes",
        "foreign body feeling in eye", "something in my eye",
    ],
    "ear_pain": [
        "ear pain", "earache", "ear infection", "ear hurts", "ringing in ears",
        "tinnitus", "my ear hurts", "pain in ear", "fluid in ear",
        "muffled hearing", "reduced hearing", "can't hear well",
        "hearing loss", "blocked ear", "ear is blocked", "ear fullness",
    ],

    # ── Urinary & Reproductive ────────────────────────────────────────────────────
    "frequent_urination": [
        "frequent urination", "urinating often", "peeing a lot", "overactive bladder",
        "going to bathroom often", "need to pee all the time",
        "waking up to urinate", "nocturia", "urinary frequency",
        "can't hold urine", "urgency to urinate", "bladder urgency",
    ],
    "blood_in_urine": [
        "blood in urine", "hematuria", "red urine", "bloody urine",
        "pink urine", "urine is red", "blood when urinating",
        "blood in my pee", "blood in pee",
    ],
    "painful_urination": [
        "painful urination", "burning when urinating", "pain when peeing",
        "burning urination", "dysuria", "stinging when urinating",
        "urinary pain", "painful pee", "pain in urethra",
    ],
    "uti": [
        "uti", "urinary tract infection", "bladder infection",
        "burning pee", "frequent painful urination", "cloudy urine",
        "smelly urine", "foul smelling urine", "urine infection",
        "infection in bladder", "kidney infection",
    ],
    "swelling": [
        "swelling", "swollen", "puffy", "inflammation", "edema", "bloating",
        "fluid retention", "swollen legs", "swollen feet", "swollen ankles",
        "puffiness", "facial swelling", "face is swollen", "swollen face",
        "swollen hands", "swollen lymph nodes", "glands are swollen",
    ],

    # ── Metabolic / Endocrine ─────────────────────────────────────────────────────
    "weight_loss": [
        "weight loss", "losing weight", "unintentional weight loss",
        "unexplained weight loss", "dropping weight", "losing weight rapidly",
        "clothes fitting loosely", "weight dropping fast",
    ],
    "weight_gain": [
        "weight gain", "gaining weight", "increased weight",
        "putting on weight", "gaining weight fast", "rapid weight gain",
        "weight is increasing", "clothes getting tight",
    ],
    "excessive_thirst": [
        "excessive thirst", "very thirsty", "always thirsty", "polydipsia",
        "drinking a lot of water", "can't quench thirst", "extreme thirst",
        "constantly drinking", "unusually thirsty",
    ],
    "difficulty_swallowing": [
        "difficulty swallowing", "dysphagia", "trouble swallowing",
        "food stuck in throat", "painful swallowing", "can't swallow",
        "swallowing is hard", "food going down slowly", "throat closing",
    ],

    # ── Respiratory ──────────────────────────────────────────────────────────────
    "chest_congestion": [
        "chest congestion", "congested chest", "tight chest", "heavy chest with cough",
        "mucus in chest", "phlegm in chest", "rattling chest", "chest feels full",
        "productive cough with chest tightness",
    ],
    "nasal_bleeding": [
        "nosebleed", "nose bleed", "bleeding nose", "nasal bleeding",
        "blood from nose", "my nose is bleeding", "nose keeps bleeding",
        "recurring nosebleed", "frequent nosebleeds",
    ],


    # ── New Symptoms ────────────────────────────────────────────────────────────
    "itching": [
        "itching", "itchy", "pruritus", "scratching", "itchy palm", "itchy hands",
        "itching in my palm", "itchy legs", "itchy body", "skin itching",
        "feeling itchy", "can't stop scratching", "itchy skin", "itching all over",
        "scratch"
    ],
    "muscle_cramps": [
        "muscle cramps", "leg cramps", "charley horse", "muscle spasms",
        "calf cramps", "cramping muscle", "muscle knotted", "muscle twitching"
    ],
    "dry_skin": [
        "dry skin", "flaky skin", "cracked skin", "peeling skin",
        "scaly skin", "skin feels tight", "rough skin"
    ],
    "dry_mouth": [
        "dry mouth", "cotton mouth", "no saliva", "parched",
        "mouth is dry", "thirsty constantly", "lack of saliva"
    ],
    "toothache": [
        "toothache", "dental pain", "tooth pain", "gums hurting",
        "jaw pain", "tooth hurts", "pain in tooth", "tooth sensitivity",
        "tooth ache"
    ],
    "snoring": [
        "snoring", "loud breathing at night", "sleep apnea",
        "snore loudly", "waking up gasping", "partner says I snore"
    ],
    "hot_flashes": [
        "hot flashes", "sudden heat", "feeling hot suddenly", "night sweats",
        "temperature spikes", "flushing", "sweating suddenly"
    ],
    "mood_swings": [
        "mood swings", "emotional", "crying easily", "unexplained anger",
        "mood changes", "irritability", "feeling emotional", "up and down emotions"
    ],
    "pelvic_pain": [
        "pelvic pain", "groin pain", "lower pelvic pain",
        "pain in pelvis", "pelvic pressure", "lower abdominal pain"
    ],
    "menstrual_cramps": [
        "menstrual cramps", "period pain", "dysmenorrhea",
        "bad cramps", "painful periods", "stomach pain from period"
    ],
    "foot_pain": [
        "foot pain", "heel pain", "sole pain", "arch pain",
        "plantar fasciitis", "feet hurt", "pain in foot", "stepping hurts"
    ],
    "hiccups": [
        "hiccups", "constant hiccups", "won't stop hiccuping",
        "hiccuping", "hiccuping a lot", "persistent hiccups"
    ],
    "sneezing_fits": [
        "sneezing fits", "constant sneezing", "non-stop sneezing",
        "sneezing a lot", "can't stop sneezing", "sneezing continuously",
        "sneezing"
    ],
    "dark_urine": [
        "dark urine", "brown urine", "tea-colored urine", "dark yellow pee",
        "urine is dark", "amber urine", "pee is dark"
    ],

    # ── Blood Sugar / Metabolic ──────────────────────────────────────────────────
    "hypoglycemia": [
        "low blood sugar", "blood sugar low", "hypoglycemia", "sugar dropping",
        "glucose is low", "feel shaky from hunger", "shaky and lightheaded",
        "dizzy from not eating", "hunger weakness", "sugar crash",
        "blood glucose low", "feeling faint from hunger", "low glucose",
    ],
    "diabetes_symptoms": [
        "diabetes", "high blood sugar", "hyperglycemia", "sugar levels high",
        "blood sugar high", "glucose is high", "sugar in blood",
        "diagnosed with diabetes", "diabetic symptoms", "blood sugar spike",
        "elevated blood sugar", "sugar level elevated",
    ],

    # ── Neurological / Cognitive ─────────────────────────────────────────────────
    "fainting": [
        "fainting", "fainted", "loss of consciousness", "passed out",
        "blacked out", "syncope", "fell unconscious", "went out cold",
        "faint episode", "suddenly fell", "collapsed", "brief unconsciousness",
    ],
    "seizure": [
        "seizure", "epileptic episode", "fit", "convulsions", "epilepsy",
        "body stiffened", "shaking uncontrollably", "jerking episodes",
        "grand mal", "petit mal", "absence seizure", "staring episode",
        "fell and shook",
    ],
    "speech_difficulty": [
        "speech difficulty", "slurred speech", "can't speak properly",
        "trouble speaking", "words not coming out", "mumbling",
        "trouble finding words", "word finding difficulty", "aphasia",
        "speaking is difficult", "speech is slurred", "slurring words",
    ],
    "paralysis": [
        "paralysis", "can't move arm", "can't move leg", "limb weakness sudden",
        "one side weak", "hemiplegia", "face drooping", "facial droop",
        "arm dropped", "sudden loss of movement", "unable to move arm",
        "unable to move leg",
    ],

    # ── Respiratory / Pulmonary ──────────────────────────────────────────────────
    "asthma": [
        "asthma", "asthma attack", "asthma flare", "wheezing badly",
        "severe wheezing", "bronchospasm", "bronchial asthma",
        "shortness of breath from asthma", "tight chest from asthma",
        "inhaler needed", "using inhaler", "can't breathe from asthma",
    ],
    "hiccups_chronic": [
        "hiccups that won't stop", "hiccups for days", "persistent hiccups more than 48 hours",
        "chronic hiccups", "hiccups lasting long", "hiccups for weeks",
    ],
    "coughing_blood": [
        "coughing blood", "coughing up blood", "blood in spit", "hemoptysis",
        "bloody mucus", "blood in phlegm", "blood when coughing",
        "spitting blood", "blood in sputum",
    ],

    # ── Cardiac ──────────────────────────────────────────────────────────────────
    "high_blood_pressure": [
        "high blood pressure", "hypertension", "blood pressure high",
        "BP is high", "elevated blood pressure", "raised BP",
        "blood pressure elevated", "pressure is high", "systolic high",
        "diastolic high", "hypertensive",
    ],
    "low_blood_pressure": [
        "low blood pressure", "hypotension", "blood pressure low",
        "BP is low", "pressure dropped", "blood pressure drop",
        "feeling faint from low pressure", "dizzy from low BP",
        "pressure is too low",
    ],
    "irregular_pulse": [
        "irregular pulse", "uneven heartbeat", "arrhythmia",
        "missed heartbeats", "heart skipping", "abnormal heart rhythm",
        "pulse is irregular", "heart not beating regularly", "AFib",
        "atrial fibrillation",
    ],

    # ── Gastrointestinal (extended) ──────────────────────────────────────────────
    "rectal_bleeding": [
        "rectal bleeding", "blood in stool", "bloody stool", "blood in poop",
        "blood in bowel movement", "red stool", "maroon stool",
        "black tarry stool", "melena", "hematochezia",
    ],
    "jaundice": [
        "jaundice", "yellow skin", "yellowing of eyes", "yellow eyes",
        "skin turning yellow", "eyes are yellow", "sclera yellow",
        "liver problem yellow", "yellow tinge to skin",
    ],
    "abdominal_swelling": [
        "abdominal swelling", "distended abdomen", "swollen belly",
        "stomach is distended", "abdomen is swollen", "pot belly suddenly",
        "ascites", "belly is puffed up", "swollen abdomen",
    ],

    # ── Urological (extended) ────────────────────────────────────────────────────
    "kidney_pain": [
        "kidney pain", "flank pain", "pain in side", "pain in lower back sides",
        "kidney ache", "pain near kidney", "side pain lower back",
        "pain under ribs on side", "nephralgia", "renal pain",
    ],
    "kidney_stones": [
        "kidney stones", "renal calculi", "stone in kidney", "stone passing",
        "severe side pain", "excruciating flank pain", "bladder stone",
        "ureteral stone", "passing a stone", "stone in ureter",
    ],
    "urinary_retention": [
        "urinary retention", "can't urinate", "unable to pee", "no urine output",
        "urine won't come out", "bladder won't empty", "can't empty bladder",
        "difficulty starting to urinate", "weak urine stream",
    ],

    # ── Skin (extended) ──────────────────────────────────────────────────────────
    "acne": [
        "acne", "pimples", "zits", "blackheads", "whiteheads",
        "breakout", "skin breakout", "cystic acne", "face full of pimples",
        "pimple outbreak", "pimple on face", "back acne", "chest acne",
    ],
    "psoriasis": [
        "psoriasis", "scaly skin patches", "thick skin plaques",
        "flaking red patches", "psoriasis flare", "silvery scales on skin",
        "skin plaques", "itchy scaly patches", "scaling skin condition",
    ],
    "wound_infection": [
        "wound infection", "infected cut", "cut is infected",
        "wound not healing", "pus from wound", "wound is red and hot",
        "cut is swollen", "infected wound", "wound oozing",
        "wound with discharge", "skin infection",
    ],
    "hives": [
        "hives", "urticaria", "itchy raised bumps", "welts", "raised skin welts",
        "hives outbreak", "itchy welts", "bumps after allergy",
        "skin eruption", "allergic hives",
    ],
    "sunburn": [
        "sunburn", "sun burnt skin", "burnt from sun", "skin is red from sun",
        "peeling from sunburn", "sun exposure burn", "solar erythema",
        "skin blistered from sun",
    ],

    # ── Eyes (extended) ──────────────────────────────────────────────────────────
    "pink_eye": [
        "pink eye", "conjunctivitis", "eye is pink", "red eye discharge",
        "eye discharge", "crusty eye", "eye gunk", "goopy eyes",
        "watery infected eye", "eye infection", "itchy red eyes with discharge",
    ],
    "vision_loss": [
        "vision loss", "losing vision", "can't see", "went blind suddenly",
        "sudden loss of vision", "sight lost", "partial vision loss",
        "blindness", "visual field loss", "curtain over vision",
    ],

    # ── ENT (extended) ───────────────────────────────────────────────────────────
    "hearing_loss": [
        "hearing loss", "can't hear", "deaf", "deafness", "hearing reduced",
        "hearing muffled", "sounds are muffled", "can't hear well",
        "partial deafness", "sudden hearing loss", "hearing going",
    ],
    "nasal_polyps": [
        "nasal polyps", "growths in nose", "blocked nose always",
        "can't smell", "loss of smell", "anosmia", "no sense of smell",
        "smell is gone", "can't taste or smell",
    ],
    "loss_of_taste": [
        "loss of taste", "can't taste", "food tastes bland", "ageusia",
        "taste is gone", "nothing tastes right", "altered taste",
        "taste is different", "dysgeusia",
    ],

    # ── Reproductive / Women's Health (extended) ─────────────────────────────────
    "irregular_periods": [
        "irregular periods", "missed period", "late period", "no period",
        "period is late", "skipped period", "menstrual irregularity",
        "periods are irregular", "period came early", "period stopped",
        "amenorrhea", "cycle is off",
    ],
    "heavy_bleeding": [
        "heavy bleeding", "heavy period", "menorrhagia", "flooding period",
        "bleeding heavily", "soaking pads quickly", "heavy menstrual flow",
        "abnormal uterine bleeding", "excessive period",
    ],
    "vaginal_discharge": [
        "vaginal discharge", "abnormal discharge", "unusual discharge",
        "discharge with odor", "colored discharge", "discharge that smells",
        "white discharge", "yellow discharge", "green discharge",
    ],
    "breast_pain": [
        "breast pain", "breast tenderness", "sore breasts", "breast ache",
        "pain in chest breast", "breasts are sore", "breast discomfort",
        "mastodynia", "breast lump pain", "tender breasts",
    ],

    # ── Men's Health ─────────────────────────────────────────────────────────────
    "erectile_dysfunction": [
        "erectile dysfunction", "ED", "can't get erection", "impotence",
        "difficulty with erection", "poor erection", "sexual dysfunction",
        "erection problems", "can't maintain erection",
    ],

    # ── Allergic / Immune ────────────────────────────────────────────────────────
    "allergic_reaction": [
        "allergic reaction", "allergy", "allergic", "anaphylaxis", "allergic response",
        "severe allergy", "allergy attack", "allergic to something",
        "swollen lips from allergy", "tongue swelling", "throat closing from allergy",
    ],
    "food_allergy": [
        "food allergy", "allergic to food", "reaction from eating",
        "food intolerance", "allergic to nuts", "allergic to dairy",
        "allergic to shellfish", "allergic to gluten", "food reaction",
    ],

    # ── Bone & Joints (extended) ──────────────────────────────────────────────────
    "osteoporosis": [
        "osteoporosis", "weak bones", "low bone density", "fragile bones",
        "fracture from minor fall", "bone fracture easily", "bone loss",
        "osteopenia",
    ],
    "fracture": [
        "fracture", "broken bone", "bone fracture", "cracked bone",
        "stress fracture", "hairline fracture", "i broke my bone",
        "fractured arm", "fractured leg", "broken arm", "broken leg",
    ],

    # ── Miscellaneous / Systemic ──────────────────────────────────────────────────
    "dehydration": [
        "dehydration", "dehydrated", "not drinking enough water",
        "thirsty and dizzy", "dry mouth and dizzy", "lack of fluids",
        "very thirsty", "urine is dark from dehydration", "feel parched",
    ],
    "food_poisoning": [
        "food poisoning", "ate bad food", "foodborne illness",
        "stomach bug", "gastroenteritis", "stomach flu",
        "food contaminated", "sick from food", "food related illness",
        "throwing up after eating", "diarrhea after eating",
    ],
    "sunstroke": [
        "sunstroke", "heat stroke", "heat exhaustion", "overheated",
        "too hot outside", "heat sickness", "sun sickness",
        "hyperthermia", "passed out in heat", "collapsed from heat",
    ],
    "altitude_sickness": [
        "altitude sickness", "mountain sickness", "high altitude",
        "AMS", "altitude headache", "sick from altitude",
        "nausea in mountains", "shortness of breath at altitude",
    ],
    "insect_bite": [
        "insect bite", "bug bite", "mosquito bite", "bee sting",
        "wasp sting", "ant bite", "spider bite", "tick bite",
        "bitten by insect", "stung by wasp", "stung by bee",
    ],
}



# ─── Risk classification ────────────────────────────────────────────────────────

RISK_LEVELS = {
    "low": {
        "symptoms": [
            "headache", "fatigue", "runny_nose", "sore_throat", "body_aches",
            "insomnia", "constipation", "back_pain", "ear_pain", "eye_pain",
            "hair_loss", "weight_gain", "loss_of_appetite", "neck_pain",
            "heartburn", "bloating", "cold_sores", "excessive_sweating",
            "nasal_bleeding",
            "itching", "muscle_cramps", "dry_skin", "dry_mouth", "toothache",
            "snoring", "hot_flashes", "mood_swings", "pelvic_pain",
            "menstrual_cramps", "foot_pain", "hiccups", "sneezing_fits",
            "acne", "sunburn", "insect_bite", "hiccups_chronic",
            "loss_of_taste", "nasal_polyps", "food_allergy",
        ],
        "color": "#22c55e",
        "label": "Low Risk",
        "urgency": "These symptoms are commonly manageable with self-care and lifestyle adjustments. Monitor your condition and consult a doctor if symptoms persist or worsen."
    },
    "medium": {
        "symptoms": [
            "fever", "cough", "nausea", "vomiting", "dizziness", "stomach_pain",
            "rash", "diarrhea", "anxiety", "depression", "blurred_vision",
            "swelling", "frequent_urination", "numbness", "palpitations",
            "difficulty_swallowing", "excessive_thirst", "bruising",
            "skin_discoloration", "weight_loss", "joint_pain", "muscle_weakness",
            "migraine", "memory_loss", "tremors", "painful_urination", "uti",
            "heartburn", "chest_congestion", "dark_urine",
            "hypoglycemia", "diabetes_symptoms", "high_blood_pressure",
            "low_blood_pressure", "irregular_pulse", "dehydration",
            "food_poisoning", "kidney_pain", "irregular_periods",
            "heavy_bleeding", "vaginal_discharge", "breast_pain",
            "erectile_dysfunction", "allergic_reaction", "psoriasis",
            "hives", "wound_infection", "abdominal_swelling",
            "jaundice", "rectal_bleeding", "hearing_loss",
            "urinary_retention", "osteoporosis", "altitude_sickness",
            "pink_eye", "speech_difficulty",
        ],
        "color": "#f59e0b",
        "label": "Medium Risk",
        "urgency": "These symptoms may benefit from professional evaluation. Please consider scheduling an appointment with a healthcare provider soon."
    },
    "high": {
        "symptoms": [
            "chest_pain", "shortness_of_breath", "blood_in_urine",
            "fainting", "seizure", "paralysis", "coughing_blood",
            "vision_loss", "kidney_stones", "fracture", "sunstroke",
        ],
        "color": "#ef4444",
        "label": "High Risk",
        "urgency": "These symptoms warrant prompt medical attention. Please consult a healthcare professional as soon as possible. If symptoms are severe, seek emergency care immediately."
    }
}


# ─── Symptom-to-specialist mapping ──────────────────────────────────────────────

SPECIALIST_MAP = {
    "headache":              {"specialist": "Neurologist",                         "icon": "🧠"},
    "migraine":              {"specialist": "Neurologist",                         "icon": "🧠"},
    "fever":                 {"specialist": "General Physician / Internist",       "icon": "🩺"},
    "cough":                 {"specialist": "Pulmonologist",                       "icon": "🫁"},
    "fatigue":               {"specialist": "General Physician / Internist",       "icon": "🩺"},
    "nausea":                {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "vomiting":              {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "dizziness":             {"specialist": "Neurologist / ENT Specialist",        "icon": "🧠"},
    "chest_pain":            {"specialist": "Cardiologist",                        "icon": "❤️"},
    "shortness_of_breath":   {"specialist": "Pulmonologist / Cardiologist",        "icon": "🫁"},
    "stomach_pain":          {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "sore_throat":           {"specialist": "ENT Specialist",                      "icon": "👂"},
    "runny_nose":            {"specialist": "ENT Specialist / Allergist",          "icon": "👂"},
    "body_aches":            {"specialist": "Rheumatologist / Orthopedist",        "icon": "🦴"},
    "joint_pain":            {"specialist": "Rheumatologist / Orthopedist",        "icon": "🦴"},
    "rash":                  {"specialist": "Dermatologist",                       "icon": "🩹"},
    "diarrhea":              {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "constipation":          {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "heartburn":             {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "bloating":              {"specialist": "Gastroenterologist",                  "icon": "🏥"},
    "back_pain":             {"specialist": "Orthopedist / Physiotherapist",       "icon": "🦴"},
    "neck_pain":             {"specialist": "Orthopedist / Physiotherapist",       "icon": "🦴"},
    "insomnia":              {"specialist": "Sleep Specialist / Psychiatrist",     "icon": "😴"},
    "anxiety":               {"specialist": "Psychiatrist / Psychologist",         "icon": "🧘"},
    "depression":            {"specialist": "Psychiatrist / Psychologist",         "icon": "🧘"},
    "blurred_vision":        {"specialist": "Ophthalmologist",                     "icon": "👁️"},
    "swelling":              {"specialist": "General Physician / Rheumatologist",  "icon": "🩺"},
    "weight_loss":           {"specialist": "Endocrinologist / General Physician", "icon": "⚖️"},
    "weight_gain":           {"specialist": "Endocrinologist / Nutritionist",      "icon": "⚖️"},
    "frequent_urination":    {"specialist": "Urologist / Endocrinologist",         "icon": "🏥"},
    "blood_in_urine":        {"specialist": "Urologist / Nephrologist",            "icon": "🏥"},
    "painful_urination":     {"specialist": "Urologist",                           "icon": "🏥"},
    "uti":                   {"specialist": "Urologist / General Physician",       "icon": "🏥"},
    "numbness":              {"specialist": "Neurologist",                         "icon": "🧠"},
    "tremors":               {"specialist": "Neurologist",                         "icon": "🧠"},
    "memory_loss":           {"specialist": "Neurologist / Geriatrician",          "icon": "🧠"},
    "muscle_weakness":       {"specialist": "Neurologist / Rheumatologist",        "icon": "🧠"},
    "palpitations":          {"specialist": "Cardiologist",                        "icon": "❤️"},
    "skin_discoloration":    {"specialist": "Dermatologist / Hepatologist",        "icon": "🩹"},
    "ear_pain":              {"specialist": "ENT Specialist",                      "icon": "👂"},
    "eye_pain":              {"specialist": "Ophthalmologist",                     "icon": "👁️"},
    "difficulty_swallowing": {"specialist": "ENT Specialist / Gastroenterologist", "icon": "👂"},
    "loss_of_appetite":      {"specialist": "General Physician / Gastroenterologist", "icon": "🩺"},
    "excessive_thirst":      {"specialist": "Endocrinologist",                     "icon": "⚖️"},
    "hair_loss":             {"specialist": "Dermatologist / Endocrinologist",     "icon": "🩹"},
    "bruising":              {"specialist": "Hematologist",                        "icon": "🩸"},
    "excessive_sweating":    {"specialist": "Dermatologist / Endocrinologist",     "icon": "🩹"},
    "cold_sores":            {"specialist": "Dermatologist / General Physician",   "icon": "🩹"},
    "chest_congestion":      {"specialist": "Pulmonologist",                       "icon": "🫁"},
    "nasal_bleeding":        {"specialist": "ENT Specialist",                      "icon": "👂"},

    "itching":              {"specialist": "Dermatologist / General Physician",        "icon": "🩹"},
    "muscle_cramps":        {"specialist": "General Physician / Physiotherapist",      "icon": "🦵"},
    "dry_skin":             {"specialist": "Dermatologist",                            "icon": "🧴"},
    "dry_mouth":            {"specialist": "Dentist / General Physician",              "icon": "👅"},
    "toothache":            {"specialist": "Dentist",                                  "icon": "🦷"},
    "snoring":              {"specialist": "Sleep Specialist / ENT",                   "icon": "😴"},
    "hot_flashes":          {"specialist": "Gynecologist / Endocrinologist",           "icon": "🌡️"},
    "mood_swings":          {"specialist": "Psychiatrist / Endocrinologist",           "icon": "🧠"},
    "pelvic_pain":          {"specialist": "Gynecologist / Urologist",                 "icon": "🏥"},
    "menstrual_cramps":     {"specialist": "Gynecologist / General Physician",         "icon": "🩸"},
    "foot_pain":            {"specialist": "Podiatrist / Orthopedist",                 "icon": "🦶"},
    "hiccups":              {"specialist": "General Physician",                        "icon": "🩺"},
    "sneezing_fits":        {"specialist": "Allergist / ENT Specialist",               "icon": "🤧"},
    "dark_urine":           {"specialist": "Urologist / Nephrologist",                 "icon": "💧"},

    # ── New specialists ──────────────────────────────────────────────────────────
    "hypoglycemia":         {"specialist": "Endocrinologist / General Physician",      "icon": "⚖️"},
    "diabetes_symptoms":    {"specialist": "Endocrinologist / Diabetologist",          "icon": "⚖️"},
    "fainting":             {"specialist": "Cardiologist / Neurologist",               "icon": "❤️"},
    "seizure":              {"specialist": "Neurologist / Emergency Physician",        "icon": "🧠"},
    "speech_difficulty":    {"specialist": "Neurologist / Speech Therapist",           "icon": "🧠"},
    "paralysis":            {"specialist": "Neurologist / Emergency Physician",        "icon": "🧠"},
    "asthma":               {"specialist": "Pulmonologist / Allergist",               "icon": "🫁"},
    "hiccups_chronic":      {"specialist": "Gastroenterologist / General Physician",   "icon": "🩺"},
    "coughing_blood":       {"specialist": "Pulmonologist / Emergency Physician",      "icon": "🫁"},
    "high_blood_pressure":  {"specialist": "Cardiologist / General Physician",         "icon": "❤️"},
    "low_blood_pressure":   {"specialist": "Cardiologist / General Physician",         "icon": "❤️"},
    "irregular_pulse":      {"specialist": "Cardiologist",                             "icon": "❤️"},
    "rectal_bleeding":      {"specialist": "Gastroenterologist / Colorectal Surgeon",  "icon": "🏥"},
    "jaundice":             {"specialist": "Hepatologist / Gastroenterologist",        "icon": "🏥"},
    "abdominal_swelling":   {"specialist": "Gastroenterologist / General Physician",   "icon": "🏥"},
    "kidney_pain":          {"specialist": "Nephrologist / Urologist",                 "icon": "🏥"},
    "kidney_stones":        {"specialist": "Urologist / Nephrologist",                 "icon": "🏥"},
    "urinary_retention":    {"specialist": "Urologist",                               "icon": "🏥"},
    "acne":                 {"specialist": "Dermatologist",                            "icon": "🩹"},
    "psoriasis":            {"specialist": "Dermatologist / Rheumatologist",           "icon": "🩹"},
    "wound_infection":      {"specialist": "General Physician / Surgeon",              "icon": "🩹"},
    "hives":                {"specialist": "Dermatologist / Allergist",                "icon": "🩹"},
    "sunburn":              {"specialist": "Dermatologist / General Physician",        "icon": "🩹"},
    "pink_eye":             {"specialist": "Ophthalmologist",                          "icon": "👁️"},
    "vision_loss":          {"specialist": "Ophthalmologist / Emergency Physician",    "icon": "👁️"},
    "hearing_loss":         {"specialist": "ENT Specialist / Audiologist",             "icon": "👂"},
    "nasal_polyps":         {"specialist": "ENT Specialist",                          "icon": "👂"},
    "loss_of_taste":        {"specialist": "ENT Specialist / Neurologist",             "icon": "👂"},
    "irregular_periods":    {"specialist": "Gynecologist / Endocrinologist",           "icon": "🩸"},
    "heavy_bleeding":       {"specialist": "Gynecologist",                            "icon": "🩸"},
    "vaginal_discharge":    {"specialist": "Gynecologist",                            "icon": "🩸"},
    "breast_pain":          {"specialist": "Gynecologist / Oncologist",               "icon": "🩸"},
    "erectile_dysfunction": {"specialist": "Urologist / Andrologist",                 "icon": "🏥"},
    "allergic_reaction":    {"specialist": "Allergist / Emergency Physician",         "icon": "🩺"},
    "food_allergy":         {"specialist": "Allergist / Immunologist",                "icon": "🩺"},
    "osteoporosis":         {"specialist": "Rheumatologist / Orthopedist",            "icon": "🦴"},
    "fracture":             {"specialist": "Orthopedist / Emergency Physician",       "icon": "🦴"},
    "dehydration":          {"specialist": "General Physician",                       "icon": "💧"},
    "food_poisoning":       {"specialist": "Gastroenterologist / General Physician",  "icon": "🏥"},
    "sunstroke":            {"specialist": "Emergency Physician / General Physician", "icon": "🌡️"},
    "altitude_sickness":    {"specialist": "General Physician / Emergency Physician", "icon": "🩺"},
    "insect_bite":          {"specialist": "Dermatologist / General Physician",       "icon": "🩹"},
}


# ─── Possible causes (non-diagnostic) ───────────────────────────────────────────

POSSIBLE_CAUSES = {
    "headache": [
        "tension or stress", "dehydration", "eye strain from screens",
        "irregular sleep patterns", "dietary factors",
    ],
    "migraine": [
        "hormonal changes", "specific food triggers (chocolate, caffeine)",
        "bright lights or loud sounds", "stress", "sleep disruption",
    ],

    "itching": [
        "dry skin", "allergic reactions", "insect bites",
        "contact dermatitis", "eczema or psoriasis",
    ],
    "muscle_cramps": [
        "dehydration", "electrolyte imbalance (low potassium/magnesium)", 
        "muscle fatigue from overexertion", "poor blood circulation",
    ],
    "dry_skin": [
        "winter weather/low humidity", "frequent hot showers", 
        "harsh soaps", "aging", "dehydration",
    ],
    "dry_mouth": [
        "dehydration", "medication side effects", "mouth breathing",
        "anxiety or stress", "aging",
    ],
    "toothache": [
        "tooth decay or cavities", "gum disease", "tooth fracture",
        "teeth grinding (bruxism)", "abscessed tooth",
    ],
    "snoring": [
        "nasal congestion", "sleep apnea", "alcohol consumption before bed",
        "sleeping on your back", "overweight",
    ],
    "hot_flashes": [
        "menopause or perimenopause", "hormonal imbalances", 
        "certain medications", "spicy foods or alcohol",
    ],
    "mood_swings": [
        "hormonal changes", "high stress levels", "poor sleep quality",
        "mental health conditions", "dietary factors",
    ],
    "pelvic_pain": [
        "menstrual cramps", "urinary tract infections", "digestive issues",
        "muscle spasms", "reproductive system conditions",
    ],
    "menstrual_cramps": [
        "normal uterine contractions during menstruation", "endometriosis",
        "fibroids", "pelvic inflammatory disease",
    ],
    "foot_pain": [
        "ill-fitting shoes", "plantar fasciitis", "flat feet",
        "standing for long periods", "sprains or strains",
    ],
    "hiccups": [
        "eating too quickly", "drinking carbonated beverages", "swallowing excess air",
        "sudden temperature changes", "excitement or emotional stress",
    ],
    "sneezing_fits": [
        "seasonal allergies", "dust or pet dander", "strong odors or perfumes",
        "common cold", "changes in temperature",
    ],
    "dark_urine": [
        "severe dehydration", "liver conditions", "certain medications",
        "urinary tract infections", "muscle breakdown from extreme exercise",
    ],
    "fever": [
        "viral or bacterial infections", "inflammatory conditions",
        "post-vaccination response", "environmental heat exposure",
    ],
    "cough": [
        "post-nasal drip", "seasonal allergies", "dry air exposure",
        "respiratory irritants", "common cold",
    ],
    "fatigue": [
        "insufficient sleep", "high stress levels", "poor nutrition",
        "sedentary lifestyle", "dehydration",
    ],
    "nausea": [
        "dietary factors", "motion sensitivity", "stress or anxiety",
        "medication side effects", "dehydration",
    ],
    "vomiting": [
        "food-related issues", "viral gastroenteritis", "motion sickness",
        "medication effects", "overeating",
    ],
    "dizziness": [
        "sudden position changes", "low blood sugar", "dehydration",
        "inner ear imbalance", "stress or anxiety",
    ],
    "chest_pain": [
        "muscle strain", "acid reflux", "anxiety or panic",
        "physical exertion", "respiratory issues",
    ],
    "shortness_of_breath": [
        "physical exertion", "anxiety or panic", "environmental allergens",
        "high altitude", "poor air quality",
    ],
    "stomach_pain": [
        "dietary factors", "stress", "irregular eating habits",
        "food intolerances", "gastric irritation",
    ],
    "sore_throat": [
        "viral infections", "dry air", "post-nasal drip",
        "voice strain", "seasonal allergies",
    ],
    "runny_nose": [
        "seasonal allergies", "common cold", "environmental irritants",
        "temperature changes", "dust exposure",
    ],
    "body_aches": [
        "physical overexertion", "poor posture", "stress tension",
        "inadequate rest", "weather changes",
    ],
    "joint_pain": [
        "physical overuse or strain", "inflammatory conditions", "aging-related wear",
        "weather changes", "nutritional deficiencies",
    ],
    "rash": [
        "allergic reactions", "skin irritants", "heat exposure",
        "contact with new products", "insect bites",
    ],
    "diarrhea": [
        "dietary changes", "food intolerance", "stress",
        "contaminated food or water", "viral gastroenteritis",
    ],
    "constipation": [
        "low fiber diet", "dehydration", "sedentary lifestyle",
        "dietary changes", "stress",
    ],
    "heartburn": [
        "spicy or acidic foods", "eating late at night", "excess caffeine or alcohol",
        "lying down after meals", "increased intra-abdominal pressure",
    ],
    "bloating": [
        "eating too fast", "carbonated drinks", "food intolerances",
        "high-fiber foods", "gut flora imbalance",
    ],
    "back_pain": [
        "poor posture", "prolonged sitting", "muscle strain",
        "improper lifting", "lack of exercise",
    ],
    "neck_pain": [
        "poor posture", "prolonged screen use", "sleeping in awkward position",
        "muscle tension", "stress",
    ],
    "insomnia": [
        "stress or anxiety", "screen time before bed", "caffeine intake",
        "irregular sleep schedule", "environmental noise",
    ],
    "anxiety": [
        "work or life stress", "caffeine overconsumption", "lack of sleep",
        "major life changes", "nutrient deficiencies",
    ],
    "depression": [
        "prolonged stress", "social isolation", "seasonal changes",
        "major life events", "sleep disturbances",
    ],
    "blurred_vision": [
        "eye strain", "prolonged screen use", "fatigue",
        "dry eyes", "incorrect prescription",
    ],
    "swelling": [
        "prolonged standing or sitting", "dietary sodium", "physical injury",
        "hormonal changes", "allergic reactions",
    ],
    "weight_loss": [
        "changes in diet or appetite", "increased physical activity",
        "stress or emotional factors", "metabolic changes",
    ],
    "weight_gain": [
        "dietary changes", "reduced physical activity", "stress eating",
        "hormonal fluctuations", "medication effects",
    ],
    "frequent_urination": [
        "high fluid intake", "caffeine or alcohol consumption",
        "stress or anxiety", "cold weather", "dietary factors",
    ],
    "blood_in_urine": [
        "vigorous exercise", "urinary tract irritation",
        "dietary factors (beets/berries)", "dehydration",
    ],
    "painful_urination": [
        "urinary tract infection", "dehydration", "bladder irritation",
        "sexual transmitted infections", "kidney stones",
    ],
    "uti": [
        "bacterial infection in urinary tract", "dehydration", "poor hygiene",
        "sexual activity", "holding urine too long",
    ],
    "numbness": [
        "poor circulation from position", "prolonged pressure on nerves",
        "cold exposure", "repetitive motion", "vitamin deficiencies",
    ],
    "tremors": [
        "caffeine or stimulants", "anxiety", "fatigue",
        "vitamin deficiency", "medication side effects",
    ],
    "memory_loss": [
        "sleep deprivation", "high stress levels", "nutritional deficiencies",
        "aging", "medication side effects",
    ],
    "muscle_weakness": [
        "prolonged inactivity", "nutritional deficiencies", "dehydration",
        "over-exertion", "electrolyte imbalances",
    ],
    "palpitations": [
        "caffeine or stimulants", "stress or anxiety", "physical exertion",
        "dehydration", "lack of sleep",
    ],
    "skin_discoloration": [
        "sun exposure", "dietary factors", "bruising",
        "cosmetic reactions", "circulation changes",
    ],
    "ear_pain": [
        "pressure changes", "water exposure", "loud noise exposure",
        "jaw tension", "common cold",
    ],
    "eye_pain": [
        "screen fatigue", "dry eyes", "bright light exposure",
        "contact lens irritation", "sinus pressure",
    ],
    "difficulty_swallowing": [
        "dry throat", "eating too quickly", "acid reflux",
        "throat tension", "cold or sore throat",
    ],
    "loss_of_appetite": [
        "stress or emotional distress", "medication effects",
        "irregular meal schedule", "dehydration", "fatigue",
    ],
    "excessive_thirst": [
        "dehydration", "high sodium diet", "physical activity",
        "dry environment", "medication effects",
    ],
    "hair_loss": [
        "stress", "nutritional deficiencies", "hormonal changes",
        "heat styling damage", "seasonal shedding",
    ],
    "bruising": [
        "minor physical impacts", "aging", "medication effects",
        "nutritional factors", "sun damage",
    ],
    "excessive_sweating": [
        "heat or humidity", "anxiety or stress", "exercise",
        "hormonal changes", "medication side effects",
    ],
    "cold_sores": [
        "HSV-1 viral reactivation", "stress or fatigue", "sun exposure",
        "immune system suppression", "illness or fever",
    ],
    "chest_congestion": [
        "respiratory infection", "allergies", "dry air",
        "smoking irritation", "seasonal illness",
    ],
    "nasal_bleeding": [
        "dry air", "nose picking", "high blood pressure",
        "allergies", "nasal irritation",
    ],
    "hypoglycemia": [
        "skipping meals", "excessive insulin", "prolonged exercise without eating",
        "alcohol consumption", "certain medications",
    ],
    "diabetes_symptoms": [
        "insulin resistance", "pancreatic dysfunction", "obesity",
        "genetic predisposition", "sedentary lifestyle",
    ],
    "fainting": [
        "standing up too quickly", "dehydration", "low blood pressure",
        "prolonged standing in heat", "heart rhythm issues",
    ],
    "seizure": [
        "epilepsy", "head injury", "high fever",
        "electrolyte imbalances", "stroke or brain injury",
    ],
    "speech_difficulty": [
        "stroke", "severe migraine", "extreme fatigue",
        "neurological conditions", "intoxication",
    ],
    "paralysis": [
        "stroke", "spinal cord injury", "nerve damage",
        "severe disc herniation", "Bell's palsy (facial)",
    ],
    "asthma": [
        "allergen or irritant exposure", "exercise-induced", "respiratory infections",
        "cold air", "genetic predisposition",
    ],
    "hiccups_chronic": [
        "gastroesophageal reflux", "irritation of the diaphragm", "central nervous system issues",
        "certain medications", "metabolic disorders",
    ],
    "coughing_blood": [
        "severe respiratory infection", "pulmonary embolism", "bronchiectasis",
        "lung cancer", "tuberculosis",
    ],
    "high_blood_pressure": [
        "high sodium diet", "sedentary lifestyle", "chronic stress",
        "obesity", "genetic factors",
    ],
    "low_blood_pressure": [
        "dehydration", "prolonged bed rest", "heart problems",
        "nutritional deficiencies", "blood loss",
    ],
    "irregular_pulse": [
        "caffeine or stimulants", "stress or anxiety", "electrolyte imbalances",
        "heart disease", "thyroid disorders",
    ],
    "rectal_bleeding": [
        "hemorrhoids", "anal fissure", "gastrointestinal infections",
        "inflammatory bowel disease", "colorectal polyps",
    ],
    "jaundice": [
        "liver disease or hepatitis", "bile duct obstruction", "hemolytic anemia",
        "gallstones", "certain medications",
    ],
    "abdominal_swelling": [
        "gas and bloating", "fluid accumulation (ascites)", "liver disease",
        "ovarian cysts", "weight gain",
    ],
    "kidney_pain": [
        "kidney infection (pyelonephritis)", "kidney stones", "urinary tract infection",
        "cysts on kidney", "trauma or injury",
    ],
    "kidney_stones": [
        "dehydration", "high oxalate or calcium diet", "recurrent UTIs",
        "family history of stones", "certain medications",
    ],
    "urinary_retention": [
        "enlarged prostate", "bladder nerve damage", "severe UTI",
        "certain medications", "urethral stricture",
    ],
    "acne": [
        "hormonal changes", "excess sebum production", "bacterial skin infection",
        "stress", "dietary factors (dairy, high-glycemic foods)",
    ],
    "psoriasis": [
        "immune system dysfunction", "genetic predisposition", "stress triggers",
        "skin injury (Koebner phenomenon)", "certain medications",
    ],
    "wound_infection": [
        "bacterial contamination", "delayed wound care", "weakened immune system",
        "foreign body in wound", "poor hygiene",
    ],
    "hives": [
        "allergic reactions", "medications", "insect stings",
        "emotional stress", "infections",
    ],
    "sunburn": [
        "prolonged UV exposure", "no or inadequate sunscreen", "reflective surfaces",
        "fair skin", "high altitude sun exposure",
    ],
    "pink_eye": [
        "viral or bacterial infection", "allergies", "chemical irritants",
        "contact lens irritation", "close contact with infected person",
    ],
    "vision_loss": [
        "retinal detachment", "stroke affecting visual cortex", "glaucoma",
        "severe eye injury", "central retinal artery occlusion",
    ],
    "hearing_loss": [
        "loud noise exposure", "aging", "ear infections",
        "earwax buildup", "certain medications",
    ],
    "nasal_polyps": [
        "chronic sinusitis", "allergies", "asthma",
        "aspirin sensitivity", "cystic fibrosis",
    ],
    "loss_of_taste": [
        "COVID-19 or viral infection", "zinc deficiency", "nasal congestion",
        "medication side effects", "nerve damage",
    ],
    "irregular_periods": [
        "hormonal imbalances", "PCOS", "extreme stress",
        "excessive exercise", "thyroid disorders",
    ],
    "heavy_bleeding": [
        "fibroid tumors", "hormonal imbalances", "endometriosis",
        "polyps in uterus", "blood clotting disorders",
    ],
    "vaginal_discharge": [
        "bacterial vaginosis", "yeast infection", "sexually transmitted infections",
        "hormonal changes", "douching or irritants",
    ],
    "breast_pain": [
        "hormonal fluctuations (menstrual cycle)", "caffeine intake",
        "poorly fitting bra", "breast cysts", "medication side effects",
    ],
    "erectile_dysfunction": [
        "cardiovascular disease", "diabetes", "hormonal imbalances",
        "psychological stress or anxiety", "certain medications",
    ],
    "allergic_reaction": [
        "food allergens", "insect venom", "medications",
        "latex", "environmental allergens",
    ],
    "food_allergy": [
        "immune response to specific proteins", "peanuts or tree nuts",
        "shellfish or fish", "milk or eggs", "gluten (celiac disease)",
    ],
    "osteoporosis": [
        "calcium and vitamin D deficiency", "aging", "hormonal changes (menopause)",
        "sedentary lifestyle", "certain medications (steroids)",
    ],
    "fracture": [
        "trauma or fall", "osteoporosis-related bone fragility", "overuse (stress fracture)",
        "sports injury", "accident",
    ],
    "dehydration": [
        "insufficient fluid intake", "excessive sweating", "diarrhea or vomiting",
        "hot weather", "fever",
    ],
    "food_poisoning": [
        "contaminated food or water", "improper food storage", "undercooked meat",
        "cross-contamination", "bacterial or viral pathogens",
    ],
    "sunstroke": [
        "prolonged exposure to high temperatures", "inadequate hydration in heat",
        "physical exertion in hot weather", "poor acclimatization", "elderly age or young children",
    ],
    "altitude_sickness": [
        "rapid ascent to high altitude", "lack of acclimatization",
        "overexertion at altitude", "individual susceptibility",
    ],
    "insect_bite": [
        "exposure to insects outdoors", "stagnant water breeding mosquitoes",
        "lack of insect repellent", "camping or hiking", "allergy to venom",
    ],

}


# ─── Lifestyle advice ───────────────────────────────────────────────────────────

LIFESTYLE_ADVICE = {
    "headache": [
        "Stay well-hydrated throughout the day",
        "Take regular breaks from screen time (20-20-20 rule)",
        "Practice stress-reduction techniques like deep breathing",
        "Maintain a consistent sleep schedule",
    ],
    "migraine": [
        "Keep a migraine diary to identify food/environment triggers",
        "Avoid known triggers such as bright screens or strong scents",
        "Rest in a dark, quiet room during episodes",
        "Maintain a consistent sleep and meal schedule",
    ],

    "itching": [
        "Apply a gentle, fragrance-free moisturizer regularly",
        "Avoid scratching, which can worsen irritation and cause infection",
        "Use over-the-counter anti-itch creams if needed",
        "Take lukewarm (not hot) baths or showers",
    ],
    "muscle_cramps": [
        "Gently stretch and massage the affected muscle",
        "Apply heat to relaxed tense muscles, or cold for pain",
        "Ensure adequate hydration and electrolyte intake",
        "Stretch regularly, especially before and after exercise",
    ],
    "dry_skin": [
        "Moisturize immediately after showering while skin is damp",
        "Use a humidifier in your home during dry months",
        "Avoid harsh soaps containing alcohol or heavy fragrances",
        "Limit showers to 5-10 minutes using lukewarm water",
    ],
    "dry_mouth": [
        "Sip water regularly throughout the day",
        "Chew sugar-free gum to stimulate saliva production",
        "Limit caffeine and alcohol, which can cause dryness",
        "Breathe through your nose rather than your mouth",
    ],
    "toothache": [
        "Rinse mouth with warm salt water",
        "Use an over-the-counter pain reliever",
        "Apply a cold compress to the outside of your cheek",
        "Avoid very cold, hot, or sweet foods",
    ],
    "snoring": [
        "Try sleeping on your side instead of your back",
        "Elevate the head of your bed slightly",
        "Avoid alcohol and heavy meals before sleeping",
        "Maintain a healthy weight",
    ],
    "hot_flashes": [
        "Dress in layers so you can easily remove clothing",
        "Keep a fan nearby or use cooling products",
        "Avoid triggers like spicy foods, caffeine, and alcohol",
        "Practice deep, slow abdominal breathing",
    ],
    "mood_swings": [
        "Maintain a regular sleep schedule",
        "Engage in regular physical activity to boost endorphins",
        "Practice stress management techniques like meditation",
        "Eat regular, balanced meals to keep blood sugar stable",
    ],
    "pelvic_pain": [
        "Apply a heating pad to the lower abdomen or back",
        "Take warm baths to help relax pelvic muscles",
        "Practice gentle stretching or yoga",
        "Rest with your legs elevated",
    ],
    "menstrual_cramps": [
        "Apply heat to your lower abdomen or lower back",
        "Exercise regularly to improve blood flow",
        "Stay hydrated and avoid excess caffeine or salty foods",
        "Try over-the-counter pain relievers if appropriate",
    ],
    "foot_pain": [
        "Wear supportive, well-fitting shoes with good arch support",
        "Rest and elevate your feet when possible",
        "Apply ice to painful areas for 15-20 minutes",
        "Perform gentle foot and calf stretches",
    ],
    "hiccups": [
        "Drink a glass of cold water slowly",
        "Hold your breath for a short period",
        "Breathe into a paper bag (not plastic)",
        "Eat and drink more slowly to avoid swallowing air",
    ],
    "sneezing_fits": [
        "Identify and avoid your allergy triggers",
        "Keep windows closed during high pollen seasons",
        "Use a HEPA air purifier in your home",
        "Wash your hands frequently",
    ],
    "dark_urine": [
        "Increase your water intake immediately",
        "Monitor your urine color to ensure it returns to pale yellow",
        "Avoid strenuous workouts until hydration improves",
        "Seek medical advice if discoloration persists or is accompanied by pain",
    ],

    "fever": [
        "Rest and stay hydrated with water and clear fluids",
        "Wear light, breathable clothing",
        "Monitor your temperature periodically",
        "Avoid strenuous physical activity until recovered",
    ],
    "cough": [
        "Stay hydrated with warm fluids like herbal tea",
        "Use a humidifier to add moisture to the air",
        "Avoid exposure to smoke and air pollutants",
        "Honey in warm water may help soothe the throat",
    ],
    "fatigue": [
        "Aim for 7-9 hours of quality sleep each night",
        "Incorporate light exercise like walking into your routine",
        "Eat balanced meals with whole grains, proteins, and vegetables",
        "Limit caffeine, especially in the afternoon and evening",
    ],
    "nausea": [
        "Eat small, frequent meals rather than large ones",
        "Try ginger tea or peppermint tea",
        "Avoid strong odors and greasy foods",
        "Stay hydrated with small sips of clear fluids",
    ],
    "vomiting": [
        "Rest the stomach, then slowly reintroduce clear fluids",
        "Try the BRAT diet (bananas, rice, applesauce, toast)",
        "Avoid dairy, caffeine, and spicy foods temporarily",
        "Replenish electrolytes with oral rehydration solutions",
    ],
    "dizziness": [
        "Move slowly when changing positions (sitting to standing)",
        "Stay hydrated and maintain stable blood sugar",
        "Avoid sudden head movements",
        "Sit or lie down when feeling dizzy to prevent falls",
    ],
    "chest_pain": [
        "Avoid heavy physical exertion until evaluated",
        "Practice calm, deep breathing exercises",
        "Reduce caffeine and tobacco intake",
        "Seek immediate medical attention if pain is severe or persistent",
    ],
    "shortness_of_breath": [
        "Practice pursed-lip breathing techniques",
        "Avoid known allergens and irritants",
        "Maintain good posture to open airways",
        "Seek immediate help if breathing difficulty is severe",
    ],
    "stomach_pain": [
        "Eat smaller, more frequent meals",
        "Avoid spicy, fatty, or acidic foods",
        "Stay hydrated and try warm peppermint tea",
        "Practice stress management techniques",
    ],
    "sore_throat": [
        "Gargle with warm salt water several times a day",
        "Drink warm fluids and stay hydrated",
        "Use throat lozenges for comfort",
        "Rest your voice when possible",
    ],
    "runny_nose": [
        "Use saline nasal sprays for relief",
        "Stay hydrated with warm fluids",
        "Use a humidifier in dry environments",
        "Identify and reduce exposure to allergens",
    ],
    "body_aches": [
        "Gentle stretching and light movement can help",
        "Apply warm compresses to sore areas",
        "Ensure adequate rest and recovery time",
        "Stay hydrated and consider an Epsom salt bath",
    ],
    "joint_pain": [
        "Apply warm or cold compresses to affected joints",
        "Maintain gentle low-impact exercise like swimming",
        "Avoid activities that aggravate the pain",
        "Maintain a healthy weight to reduce joint load",
    ],
    "rash": [
        "Avoid scratching the affected area",
        "Use gentle, fragrance-free skin products",
        "Keep the area clean and moisturized",
        "Note any new products or exposures that may be triggers",
    ],
    "diarrhea": [
        "Stay hydrated with water and electrolyte drinks",
        "Follow the BRAT diet temporarily",
        "Avoid dairy, caffeine, and high-fiber foods",
        "Wash hands frequently to prevent spread",
    ],
    "constipation": [
        "Increase fiber intake with fruits, vegetables, and whole grains",
        "Drink plenty of water throughout the day",
        "Engage in regular physical activity",
        "Establish a regular bathroom routine",
    ],
    "heartburn": [
        "Avoid eating 2-3 hours before lying down",
        "Elevate the head of your bed slightly",
        "Limit spicy, acidic, and fatty foods",
        "Eat smaller meals throughout the day",
    ],
    "bloating": [
        "Eat slowly and chew food thoroughly",
        "Avoid carbonated beverages",
        "Identify and avoid gas-producing foods",
        "Try gentle abdominal massage or light walking after meals",
    ],
    "back_pain": [
        "Maintain good posture while sitting and standing",
        "Take breaks from prolonged sitting every 30 minutes",
        "Strengthen core muscles with gentle exercises",
        "Use proper lifting techniques (bend at the knees)",
    ],
    "neck_pain": [
        "Adjust your screen height to eye level",
        "Take regular breaks from desk work to stretch",
        "Apply a warm compress to relieve tension",
        "Practice gentle neck stretches and rotations",
    ],
    "insomnia": [
        "Maintain a consistent sleep and wake schedule",
        "Create a relaxing bedtime routine",
        "Limit screen time at least 1 hour before bed",
        "Keep your bedroom cool, dark, and quiet",
    ],
    "anxiety": [
        "Practice daily mindfulness or meditation",
        "Engage in regular physical exercise",
        "Limit caffeine and alcohol intake",
        "Consider journaling to process your thoughts",
    ],
    "depression": [
        "Maintain social connections, even when it feels difficult",
        "Engage in activities you used to enjoy",
        "Get regular sunlight exposure and physical activity",
        "Consider speaking with a mental health professional",
    ],
    "blurred_vision": [
        "Follow the 20-20-20 rule for screen breaks",
        "Ensure proper lighting when reading or working",
        "Keep eyes lubricated with artificial tears if dry",
        "Schedule regular comprehensive eye exams",
    ],
    "swelling": [
        "Elevate the affected area when possible",
        "Reduce sodium intake in your diet",
        "Stay active with gentle movement",
        "Apply cold compresses for acute swelling",
    ],
    "weight_loss": [
        "Ensure you're eating balanced, nutrient-dense meals",
        "Track your caloric intake to ensure adequacy",
        "Manage stress that may affect appetite",
        "Consult with a nutritionist for personalized guidance",
    ],
    "weight_gain": [
        "Focus on whole, unprocessed foods",
        "Increase daily physical activity gradually",
        "Manage emotional eating through mindful eating practices",
        "Stay hydrated — thirst can mimic hunger",
    ],
    "frequent_urination": [
        "Monitor your fluid intake, especially before bedtime",
        "Reduce caffeine and alcohol consumption",
        "Practice pelvic floor exercises",
        "Track frequency to share with your healthcare provider",
    ],
    "blood_in_urine": [
        "Increase water intake to stay well-hydrated",
        "Avoid strenuous exercise temporarily",
        "Avoid irritants like caffeine and spicy foods",
        "Seek prompt medical evaluation",
    ],
    "painful_urination": [
        "Drink plenty of water to flush the urinary tract",
        "Avoid caffeine and alcohol during discomfort",
        "Practice good hygiene",
        "Seek medical attention if accompanied by fever or blood",
    ],
    "uti": [
        "Drink plenty of water throughout the day",
        "Urinate frequently — avoid holding for long periods",
        "Avoid bubble baths and scented hygiene products near the urethra",
        "Seek medical attention — antibiotics may be needed",
    ],
    "numbness": [
        "Change positions frequently to improve circulation",
        "Stretch regularly, especially during desk work",
        "Ensure adequate intake of B vitamins",
        "Avoid repetitive motions without breaks",
    ],
    "tremors": [
        "Reduce caffeine and stimulant intake",
        "Ensure adequate rest and sleep",
        "Practice relaxation techniques to reduce anxiety-related shaking",
        "Note when tremors occur for discussion with your doctor",
    ],
    "memory_loss": [
        "Stay mentally active with puzzles, reading, or learning",
        "Get adequate sleep — memory consolidation happens during sleep",
        "Reduce stress and practice mindfulness",
        "Maintain social engagement and physical activity",
    ],
    "muscle_weakness": [
        "Incorporate gentle strength training exercises",
        "Ensure adequate protein and electrolyte intake",
        "Avoid prolonged bed rest unless medically advised",
        "Stay well hydrated",
    ],
    "palpitations": [
        "Reduce caffeine, nicotine, and alcohol intake",
        "Practice deep breathing and relaxation techniques",
        "Get regular, moderate exercise",
        "Maintain consistent sleep patterns",
    ],
    "skin_discoloration": [
        "Use broad-spectrum sunscreen daily",
        "Stay hydrated and maintain good nutrition",
        "Note any new medications that could cause changes",
        "Consult a dermatologist for persistent changes",
    ],
    "ear_pain": [
        "Avoid inserting objects into the ear canal",
        "Keep ears dry after swimming or bathing",
        "Use ear protection in loud environments",
        "Apply a warm cloth to the affected ear for comfort",
    ],
    "eye_pain": [
        "Take regular breaks from screens and close work",
        "Ensure adequate lighting in your workspace",
        "Use artificial tears for dry eye relief",
        "Wear UV-protective sunglasses outdoors",
    ],
    "difficulty_swallowing": [
        "Eat slowly and chew food thoroughly",
        "Take smaller bites and sips",
        "Stay upright during and after meals",
        "Stay hydrated to keep the throat moist",
    ],
    "loss_of_appetite": [
        "Try eating smaller, more frequent meals",
        "Choose nutrient-dense foods when you do eat",
        "Stay physically active to stimulate appetite",
        "Create a pleasant, stress-free eating environment",
    ],
    "excessive_thirst": [
        "Track your daily water intake",
        "Reduce salty and processed food consumption",
        "Monitor for other symptoms like frequent urination",
        "Carry water with you throughout the day",
    ],
    "hair_loss": [
        "Eat a balanced diet rich in iron, zinc, and biotin",
        "Manage stress through relaxation techniques",
        "Avoid harsh chemical treatments and excessive heat styling",
        "Be gentle when brushing and avoid tight hairstyles",
    ],
    "bruising": [
        "Protect your skin from impacts where possible",
        "Ensure adequate vitamin C and K in your diet",
        "Apply cold compresses to reduce swelling of new bruises",
        "Note any medications that may increase bruising",
    ],
    "excessive_sweating": [
        "Wear breathable, moisture-wicking clothing",
        "Shower regularly and use clinical-strength antiperspirant",
        "Stay cool and avoid triggers like caffeine or spicy food",
        "Consult a doctor if sweating is sudden or accompanied by other symptoms",
    ],
    "cold_sores": [
        "Avoid picking or touching the sore",
        "Use lip balm with sun protection to prevent triggers",
        "Avoid sharing utensils, towels, or lip products",
        "Manage stress and get adequate sleep to reduce outbreaks",
    ],
    "chest_congestion": [
        "Use steam inhalation to loosen mucus",
        "Stay well hydrated with warm fluids",
        "Use a humidifier in your living space",
        "Avoid cold air and respiratory irritants",
    ],
    "nasal_bleeding": [
        "Keep indoor air humidified",
        "Avoid blowing your nose too forcefully",
        "Apply gentle pressure to stop bleeding — lean forward, not back",
        "Use saline nasal spray to prevent drying of nasal membranes",
    ],
    "hypoglycemia": [
        "Eat regular small meals to maintain steady blood sugar",
        "Carry a quick-sugar snack (glucose tablets, juice) if prone to low sugar",
        "Avoid skipping meals, especially breakfast",
        "Track blood sugar levels if diabetic",
    ],
    "diabetes_symptoms": [
        "Monitor blood sugar regularly with a glucometer",
        "Follow a low-glycemic, balanced diet",
        "Exercise regularly to improve insulin sensitivity",
        "Stay well hydrated and limit sugary beverages",
    ],
    "fainting": [
        "Lie down immediately if you feel faint",
        "Rise slowly from sitting or lying positions",
        "Stay well hydrated and avoid prolonged standing",
        "Seek medical evaluation after any fainting episode",
    ],
    "seizure": [
        "Never leave a person alone during a seizure episode",
        "Keep calm and ensure a safe environment (remove sharp objects)",
        "Do not restrain or put anything in the mouth",
        "Seek emergency medical care immediately",
    ],
    "speech_difficulty": [
        "Seek emergency medical care immediately — may signal a stroke",
        "Note the time symptoms started",
        "Do not give food or water",
        "Keep the person calm and still until help arrives",
    ],
    "paralysis": [
        "Call emergency services immediately",
        "Keep the person still and do not move them unnecessarily",
        "Note the time of symptom onset",
        "Monitor breathing and remain calm",
    ],
    "asthma": [
        "Use your prescribed inhaler as directed",
        "Identify and avoid personal asthma triggers",
        "Keep indoor air clean and free of allergens",
        "Create an action plan with your doctor",
    ],
    "hiccups_chronic": [
        "Eat smaller, more frequent meals",
        "Avoid carbonated beverages and alcohol",
        "Try relaxation breathing techniques",
        "Seek medical evaluation if hiccups persist beyond 48 hours",
    ],
    "coughing_blood": [
        "Seek emergency medical care immediately",
        "Do not smoke or expose yourself to respiratory irritants",
        "Note the amount and color of blood for the doctor",
        "Stay calm and seated in an upright position",
    ],
    "high_blood_pressure": [
        "Reduce sodium (salt) intake significantly",
        "Exercise regularly with aerobic activities like walking",
        "Manage stress through relaxation techniques",
        "Avoid smoking and limit alcohol consumption",
    ],
    "low_blood_pressure": [
        "Rise slowly from lying or sitting positions",
        "Increase fluid and mild salt intake as advised by a doctor",
        "Wear compression stockings to improve circulation",
        "Avoid prolonged standing and hot showers",
    ],
    "irregular_pulse": [
        "Reduce caffeine, alcohol, and stimulant intake",
        "Practice stress management and relaxation techniques",
        "Monitor your heart rate regularly",
        "Seek prompt medical evaluation",
    ],
    "rectal_bleeding": [
        "Seek medical attention promptly for any rectal bleeding",
        "Stay hydrated and maintain a high-fiber diet",
        "Avoid straining during bowel movements",
        "Use sitz baths for hemorrhoid relief",
    ],
    "jaundice": [
        "Seek medical evaluation immediately",
        "Avoid alcohol completely",
        "Stay well hydrated and rest",
        "Eat a low-fat, easily digestible diet",
    ],
    "abdominal_swelling": [
        "Reduce gas-producing foods (beans, carbonated drinks)",
        "Seek medical attention if swelling is sudden or severe",
        "Monitor for other symptoms like pain or fever",
        "Avoid large meals and eat slowly",
    ],
    "kidney_pain": [
        "Drink plenty of water to support kidney function",
        "Seek prompt medical evaluation",
        "Avoid high-sodium and high-protein foods temporarily",
        "Rest and avoid strenuous activity",
    ],
    "kidney_stones": [
        "Drink 8–10 glasses of water daily",
        "Reduce sodium, animal protein, and oxalate-rich foods",
        "Seek prompt medical evaluation for severe pain",
        "Strain urine to catch stone for analysis",
    ],
    "urinary_retention": [
        "Seek urgent medical attention",
        "Avoid delay in urinating once you feel the urge",
        "Apply warm compress to the lower abdomen",
        "Avoid medications known to cause retention if possible",
    ],
    "acne": [
        "Cleanse face gently twice daily with a mild, non-comedogenic cleanser",
        "Avoid touching or popping pimples",
        "Use oil-free, non-comedogenic skincare products",
        "Manage stress and maintain a balanced diet",
    ],
    "psoriasis": [
        "Keep skin well moisturized with thick creams",
        "Identify and avoid personal triggers (stress, infections)",
        "Use gentle, fragrance-free soap",
        "Get moderate sun exposure but avoid sunburn",
    ],
    "wound_infection": [
        "Clean the wound thoroughly with soap and water",
        "Apply antiseptic and keep the wound covered",
        "Seek medical attention if redness, swelling, or pus appears",
        "Complete any prescribed antibiotic course fully",
    ],
    "hives": [
        "Identify and avoid allergy triggers",
        "Apply cool compresses to reduce itching and swelling",
        "Avoid hot showers and tight clothing",
        "Use antihistamines as directed",
    ],
    "sunburn": [
        "Get out of the sun immediately and cool the skin",
        "Apply aloe vera or a cool wet cloth",
        "Drink plenty of water to rehydrate",
        "Avoid further sun exposure until healed",
    ],
    "pink_eye": [
        "Avoid touching or rubbing your eyes",
        "Wash hands frequently",
        "Avoid sharing towels, pillowcases, or eye makeup",
        "Apply warm compresses for bacterial/viral type",
    ],
    "vision_loss": [
        "Seek emergency medical care immediately",
        "Do not rub your eyes",
        "Note the time and pattern of vision loss",
        "Avoid driving or operating machinery",
    ],
    "hearing_loss": [
        "Wear ear protection in loud environments",
        "Avoid cotton swabs in the ear canal",
        "Seek evaluation if hearing loss is sudden",
        "Turn down volume on headphones and devices",
    ],
    "nasal_polyps": [
        "Use saline nasal rinses to keep passages clear",
        "Treat underlying allergies and sinusitis",
        "Avoid known nasal irritants and allergens",
        "Seek ENT evaluation for persistent nasal obstruction",
    ],
    "loss_of_taste": [
        "Stay well hydrated",
        "Maintain good oral hygiene",
        "Eat a diet rich in zinc (nuts, seeds, legumes)",
        "Seek medical evaluation if taste loss persists beyond a few weeks",
    ],
    "irregular_periods": [
        "Track your menstrual cycle with an app or journal",
        "Manage stress and maintain a healthy weight",
        "Exercise regularly but avoid over-exercising",
        "Seek gynecological evaluation if irregularity persists",
    ],
    "heavy_bleeding": [
        "Track period flow and duration carefully",
        "Stay hydrated and eat iron-rich foods",
        "Rest when bleeding is heavy",
        "Seek prompt medical evaluation",
    ],
    "vaginal_discharge": [
        "Wear breathable cotton underwear",
        "Avoid scented feminine hygiene products",
        "Practice good hygiene without douching",
        "Seek evaluation if discharge changes color, smell, or amount",
    ],
    "breast_pain": [
        "Wear a well-fitting, supportive bra",
        "Reduce caffeine and salt intake",
        "Apply warm or cold compresses for relief",
        "Seek evaluation if pain is accompanied by lumps or skin changes",
    ],
    "erectile_dysfunction": [
        "Maintain cardiovascular health through exercise",
        "Manage stress and anxiety",
        "Avoid smoking and excessive alcohol",
        "Seek medical evaluation — it may signal an underlying condition",
    ],
    "allergic_reaction": [
        "Seek emergency care immediately for severe reactions (throat swelling)",
        "Use prescribed epinephrine (EpiPen) if available",
        "Identify and strictly avoid the trigger",
        "Carry antihistamines and wear a medical alert bracelet",
    ],
    "food_allergy": [
        "Read food labels carefully and ask about ingredients when dining out",
        "Avoid cross-contamination during food preparation",
        "Carry prescribed emergency medication (EpiPen)",
        "Consult an allergist for formal testing and guidance",
    ],
    "osteoporosis": [
        "Ensure adequate calcium and vitamin D intake daily",
        "Engage in weight-bearing exercises like walking",
        "Avoid smoking and limit alcohol",
        "Have regular bone density screenings",
    ],
    "fracture": [
        "Immobilize the injured area and do not move it",
        "Apply ice wrapped in cloth to reduce swelling",
        "Seek emergency medical attention immediately",
        "Elevate the injured limb if possible",
    ],
    "dehydration": [
        "Drink water regularly throughout the day",
        "Replace electrolytes lost through sweat (sports drinks, coconut water)",
        "Eat water-rich foods like fruits and vegetables",
        "Avoid alcohol and caffeine when dehydrated",
    ],
    "food_poisoning": [
        "Rest the stomach and stay hydrated with small sips",
        "Try the BRAT diet as you recover",
        "Avoid anti-diarrhea medication unless advised by a doctor",
        "Seek medical care if symptoms are severe or prolonged",
    ],
    "sunstroke": [
        "Move to a cool, shaded area immediately",
        "Apply cold water or ice packs to neck, armpits, and groin",
        "Drink cool water if conscious and able to swallow",
        "Call emergency services — heat stroke is life-threatening",
    ],
    "altitude_sickness": [
        "Descend to a lower altitude immediately if symptoms worsen",
        "Rest and acclimatize slowly before ascending further",
        "Stay well hydrated",
        "Avoid alcohol and sleeping pills at altitude",
    ],
    "insect_bite": [
        "Clean the bite area with soap and water",
        "Apply a cold pack to reduce swelling and itching",
        "Use antihistamine cream or oral antihistamine",
        "Seek medical care if you develop signs of allergic reaction or infection",
    ],

}


# ─── BERT-enhanced symptom descriptions for semantic matching ────────────────────
# Rich, descriptive sentences enable BioBERT to match paraphrased/colloquial inputs.

SYMPTOM_DESCRIPTIONS = {
    "headache": "pain or discomfort in any part of the head, ranging from sharp to dull, throbbing to constant pressure, often worsening with movement or light",
    "migraine": "severe, debilitating headache often on one side of the head, accompanied by nausea, vomiting, sensitivity to light and sound, sometimes preceded by visual aura",
    "fever": "elevated body temperature above normal, often accompanied by chills, sweating, hot skin, and general malaise or weakness",
    "cough": "sudden expulsion of air from the lungs which may be dry, hacking, or productive with mucus or phlegm",
    "fatigue": "persistent feeling of tiredness, exhaustion, or lack of energy that doesn't improve with rest, often accompanied by low motivation",
    "nausea": "sensation of unease and discomfort in the stomach with an urge to vomit, stomach turning, or feeling sick",
    "vomiting": "forceful expulsion of stomach contents through the mouth, retching, or repeatedly throwing up",
    "dizziness": "feeling of lightheadedness, unsteadiness, wooziness, or sensation that the surroundings are spinning or tilting",
    "chest_pain": "discomfort, pressure, squeezing, heaviness, or pain in the chest area, possibly radiating to the arm or jaw",
    "shortness_of_breath": "difficulty breathing, feeling of not getting enough air, breathlessness, labored breathing or wheezing",
    "stomach_pain": "pain or discomfort in the abdominal area, including cramping, bloating, sharp pain, or pressure in the belly or gut",
    "sore_throat": "pain, scratchiness, irritation, or rawness of the throat that often worsens when swallowing or speaking",
    "runny_nose": "excess nasal discharge, congestion, sneezing, blocked or stuffy nasal passages, post-nasal drip",
    "body_aches": "generalized muscle or joint pain throughout the body, widespread soreness, stiffness, and flu-like aching",
    "joint_pain": "pain, stiffness, swelling, or tenderness in one or more joints such as knees, hips, shoulders, or wrists",
    "rash": "changes in skin appearance including redness, bumps, blisters, welts, itching, or irritation across a skin area",
    "diarrhea": "frequent loose, watery, or runny bowel movements, stomach running, or urgent need to use the bathroom",
    "constipation": "infrequent bowel movements, difficulty or straining to pass hard stool, feeling of incomplete evacuation",
    "heartburn": "burning sensation in the chest or throat caused by acid reflux, sour taste in mouth, indigestion after eating",
    "bloating": "uncomfortable fullness, swelling, or distension in the abdomen, trapped gas, feeling bloated after eating",
    "back_pain": "pain or discomfort in the upper or lower back, spine, or lumbar region, sometimes radiating to the legs",
    "neck_pain": "pain, stiffness, soreness, or tension in the neck or cervical area, limited range of motion",
    "insomnia": "difficulty falling asleep, staying asleep, waking up too early, poor sleep quality, lying awake at night",
    "anxiety": "persistent worry, nervousness, restlessness, racing thoughts, feelings of panic, dread, or being on edge",
    "depression": "persistent feelings of sadness, hopelessness, emptiness, loss of interest, crying, or feeling unmotivated",
    "blurred_vision": "inability to see clearly, fuzzy or doubled images, difficulty focusing, hazy or distorted visual field",
    "swelling": "abnormal puffiness, enlargement, or fluid accumulation in limbs, face, or body parts",
    "weight_loss": "unintended decrease in body weight occurring without changes in diet or exercise",
    "weight_gain": "unintended or unexplained increase in body weight over time",
    "frequent_urination": "needing to urinate more often than usual, urgency to urinate, waking at night to urinate",
    "blood_in_urine": "presence of blood or red or pink coloring in urine",
    "painful_urination": "burning, stinging, or pain when urinating, discomfort in the urethra during urination",
    "uti": "urinary tract infection with symptoms of burning urination, frequent urge to pee, cloudy or smelly urine",
    "numbness": "loss of sensation, tingling, pins and needles feeling, or deadness in body parts like hands, feet, or limbs",
    "tremors": "involuntary shaking, trembling, or twitching of hands, arms, legs, or other body parts",
    "memory_loss": "difficulty remembering recent events, forgetfulness, confusion, brain fog, or trouble concentrating",
    "muscle_weakness": "reduced strength in muscles, difficulty lifting, weakness in arms or legs, loss of muscular power",
    "palpitations": "awareness of heartbeat being rapid, irregular, pounding, fluttering, or skipping beats",
    "skin_discoloration": "changes in skin color including yellowing, paleness, bluish tint, dark patches, or unusual coloration",
    "ear_pain": "pain, aching, fullness, or ringing sensation in one or both ears",
    "eye_pain": "pain, discomfort, pressure, burning, redness, or irritation in or around the eyes",
    "difficulty_swallowing": "trouble, pain, or choking sensation when swallowing food, liquid, or saliva",
    "loss_of_appetite": "reduced desire to eat, lack of hunger, not feeling like eating, skipping meals",
    "excessive_thirst": "abnormally strong, frequent, or unquenchable feeling of thirst",
    "hair_loss": "thinning, falling, or shedding of hair from the scalp or body in patches or diffusely",
    "bruising": "discoloration of skin from broken blood vessels, dark marks appearing without clear cause",
    "excessive_sweating": "unusually heavy sweating beyond what is expected from exertion or heat",
    "cold_sores": "small, fluid-filled blisters or sores on or around the lips and mouth, often preceded by tingling",
    "chest_congestion": "feeling of heaviness, mucus buildup, or tightness in the chest with difficult breathing or coughing",
    "nasal_bleeding": "bleeding from one or both nostrils, blood dripping from the nose",

    "itching": "irritating sensation on the skin that causes an urge to scratch, which can be localized (like palms or feet) or generalized across the body",
    "muscle_cramps": "sudden, involuntary, and painful contraction of one or more muscles, often occurring in the legs or calves",
    "dry_skin": "skin that feels rough, tight, flaky, scaly, or cracked, often worse during cold or dry weather",
    "dry_mouth": "uncomfortable feeling of not having enough saliva in the mouth, leading to difficulty swallowing or feeling parched",
    "toothache": "pain or inflammation in or around a tooth, jaw, or gums, often sensitive to temperature or pressure",
    "snoring": "harsh, noisy breathing during sleep caused by vibration of respiratory structures, sometimes indicating sleep apnea",
    "hot_flashes": "sudden feeling of intense heat, primarily in the upper body and face, often accompanied by flushing and sweating",
    "mood_swings": "rapid and noticeable changes in emotional state, alternating between emotions like happiness, anger, sadness, or irritability",
    "pelvic_pain": "pain or discomfort in the lowest part of the abdomen and pelvis, which can be dull, sharp, or cramping",
    "menstrual_cramps": "throbbing or cramping pains in the lower abdomen experienced before or during menstrual periods",
    "foot_pain": "discomfort or pain in any part of the foot including heels, arches, toes, or soles, often worsening with weight-bearing",
    "hiccups": "involuntary spasms of the diaphragm followed by sudden closure of the vocal cords, producing a characteristic sound",
    "sneezing_fits": "sudden, forceful, involuntary expulsions of air through the nose and mouth, occurring multiple times in rapid succession",
    "dark_urine": "urine that appears darker than the usual pale yellow, ranging from deep yellow or amber to brown or tea-colored",

    "hypoglycemia": "abnormally low blood sugar causing shakiness, dizziness, sweating, confusion, and weakness especially after missing meals",
    "diabetes_symptoms": "elevated blood sugar levels causing excessive thirst, frequent urination, fatigue, blurred vision, and slow wound healing",
    "fainting": "temporary loss of consciousness caused by reduced blood flow to the brain, often preceded by lightheadedness or nausea",
    "seizure": "sudden uncontrolled electrical disturbance in the brain causing convulsions, muscle stiffening, or brief loss of awareness",
    "speech_difficulty": "trouble speaking, slurred speech, or inability to find words, which may indicate a stroke or neurological event",
    "paralysis": "loss of ability to move one or more muscles, which may be sudden and is often associated with stroke or nerve injury",
    "asthma": "chronic respiratory condition causing airway inflammation, wheezing, chest tightness, and difficulty breathing especially during attacks",
    "hiccups_chronic": "repeated, involuntary spasms of the diaphragm lasting more than 48 hours, requiring medical evaluation",
    "coughing_blood": "coughing up blood or blood-tinged mucus from the respiratory tract, which is always a serious symptom",
    "high_blood_pressure": "chronically elevated pressure of blood in the arteries, often asymptomatic but a major cardiovascular risk factor",
    "low_blood_pressure": "abnormally low blood pressure causing dizziness, fainting, and inadequate blood flow to organs",
    "irregular_pulse": "abnormal heart rhythm with a pulse that feels uneven, rapid, slow, or skipping beats",
    "rectal_bleeding": "presence of blood in or on the stool or coming from the rectum, ranging from bright red to dark maroon or black",
    "jaundice": "yellowing of the skin and whites of the eyes caused by elevated bilirubin, indicating liver or bile duct issues",
    "abdominal_swelling": "visible distension or enlargement of the abdomen due to gas, fluid, or internal organ swelling",
    "kidney_pain": "pain in the flank or lower back area near the kidneys, often deep and aching, worsened by tapping the area",
    "kidney_stones": "hard mineral deposits in the kidneys causing severe flank pain, nausea, and pain during urination",
    "urinary_retention": "inability to empty the bladder fully or at all, causing discomfort, pressure, and sometimes overflow incontinence",
    "acne": "skin condition involving pimples, blackheads, whiteheads, and cysts on the face, neck, chest, and back",
    "psoriasis": "chronic skin condition causing thick, red, scaly patches covered by silvery scales that itch and may crack",
    "wound_infection": "infection of a wound or cut characterized by redness, swelling, warmth, pus, and delayed healing",
    "hives": "raised, itchy, red welts on the skin that appear and disappear due to allergic reactions or other triggers",
    "sunburn": "redness, pain, and peeling of skin caused by overexposure to ultraviolet radiation from the sun",
    "pink_eye": "inflammation of the conjunctiva causing red, itchy, watery eyes with possible discharge",
    "vision_loss": "partial or complete loss of vision in one or both eyes, which may be sudden or gradual",
    "hearing_loss": "partial or complete inability to hear in one or both ears, ranging from mild to profound deafness",
    "nasal_polyps": "soft, non-cancerous growths in the nasal passages causing nasal obstruction and loss of smell",
    "loss_of_taste": "reduced or absent ability to taste food and drinks, often accompanied by smell disturbance",
    "irregular_periods": "menstrual cycles that are unpredictable, too long, too short, or absent entirely",
    "heavy_bleeding": "abnormally heavy or prolonged menstrual bleeding that may require frequent pad or tampon changes",
    "vaginal_discharge": "fluid produced by the vagina that is abnormal in color, odor, or amount and may indicate infection",
    "breast_pain": "tenderness, heaviness, or discomfort in one or both breasts, which may be cyclical or non-cyclical",
    "erectile_dysfunction": "consistent difficulty achieving or maintaining an erection sufficient for sexual activity",
    "allergic_reaction": "immune response to a substance causing symptoms ranging from mild itching to severe anaphylaxis",
    "food_allergy": "adverse immune reaction triggered by specific foods causing skin, gastrointestinal, or respiratory symptoms",
    "osteoporosis": "condition of reduced bone density making bones fragile and more susceptible to fractures",
    "fracture": "break or crack in a bone caused by trauma, stress, or underlying bone weakness",
    "dehydration": "condition resulting from insufficient fluid intake causing dark urine, dizziness, dry mouth, and weakness",
    "food_poisoning": "illness from consuming contaminated food causing nausea, vomiting, diarrhea, and stomach cramps",
    "sunstroke": "life-threatening condition from overheating where body temperature rises dangerously high causing confusion and collapse",
    "altitude_sickness": "group of symptoms from ascending too quickly to high altitude including headache, nausea, and breathlessness",
    "insect_bite": "skin reaction from insect bite or sting causing local pain, itching, swelling, or allergic response",

}
