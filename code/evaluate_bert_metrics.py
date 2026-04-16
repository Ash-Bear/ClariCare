import sys
import os
from typing import List, Dict

# Add both root and code directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "code"))

from models.symptom_analyzer import BERTSymptomAnalyzer

# ────────────────────────────────────────────────────────────────────────
# 1. Define your "Gold Standard" (Labeled) Dataset here
# Each entry is a tuple: (user_input_text, list_of_expected_symptom_keys)
# You should map these to the exact symptom keys in data/symptoms_db.py
# ────────────────────────────────────────────────────────────────────────
EVALUATION_DATASET = [
    # Original (Fixed Keys)
    (
        "my body is hurting all over and I feel really nauseous and my head is killing me",
        ["body_aches", "nausea", "headache"]  
    ),
    (
        "I have a terrible headache and feel very tired and dizzy",
        ["headache", "fatigue", "dizziness"]
    ),
    (
        "my stomach is acting up and I keep throwing up",
        ["stomach_pain", "vomiting"]
    ),
    (
        "I feel really anxious and can't sleep at all",
        ["anxiety", "insomnia"]
    ),
    (
        "my throat is sore and I have a bad cough and fever",
        ["sore_throat", "cough", "fever"]
    ),
    (
        "I feel weak and tired and my muscles are hurting",
        ["muscle_weakness", "fatigue", "body_aches"]
    ),
    
    # New Standard Cases
    (
        "my joints are swollen and my back hurts a lot",
        ["joint_pain", "back_pain"]
    ),
    (
        "I have been having loose stools and a runny stomach since yesterday",
        ["diarrhea"]
    ),
    (
        "My nose keeps running and I can't stop sneezing",
        ["runny_nose", "sneezing_fits"]
    ),
    (
        "I feel like I'm losing my memory and I get brain fog often",
        ["memory_loss"]
    ),
    (
        "My chest is tight, I'm out of breath, and my heart is racing",
        ["chest_pain", "shortness_of_breath", "palpitations"]
    ),
    
    # Edge Cases & Conversational Slang
    (
        "I stepped on a nail and now the cut is oozing pus and hot to the touch",
        ["wound_infection"]
    ),
    (
        "Every time I pee it burns and stings really badly",
        ["painful_urination"]
    ),
    (
        "I noticed my skin is turning yellow and I'm very fatigued",
        ["skin_discoloration", "jaundice", "fatigue"]
    ),
    (
        "I'm breaking out in red itchy welts all over my arms",
        ["rash", "hives", "itching"]
    ),
    (
        "I cannot taste or smell my food at all anymore",
        ["loss_of_taste"]
    ),
    
    # ─── New Random & Complex Test Cases ───
    (
        "I'm sweating buckets constantly even when it's freezing cold in the room",
        ["excessive_sweating"]
    ),
    (
        "I keep dropping things because my hands are numb and trembling",
        ["numbness", "tremors"]
    ),
    (
        "My vision is getting super blurry and I see floating spots",
        ["vision_problems"]
    ),
    (
        "I have a throbbing migraine that won't go away no matter what pills I take",
        ["migraine"]
    ),
    (
        "I feel completely bloated after every meal like a balloon",
        ["bloating", "stomach_pain"]
    ),
    (
        "my pee is very dark, almost brownish, and it smells strange",
        ["dark_urine"]
    ),
    (
        "I'm shedding a crazy amount of hair in the shower recently",
        ["hair_loss"]
    ),
    (
        "I get super dizzy whenever I stand up too fast, feels like the room is spinning",
        ["dizziness"]
    ),
    (
        "my ear aches really bad and there's a ringing sound all the time",
        ["earache", "ringing_in_ears"]
    ),
    (
        "There's this weird lump on my neck that feels tender to touch",
        ["swollen_lymph_nodes"]
    ),
    (
        "I'm totally exhausted, dragging my feet all day without any energy",
        ["fatigue"]
    ),
    (
        "My heart beats weirdly, fluttering skips like a drum",
        ["palpitations"]
    ),
    (
        "Every joint in my body is stiff when I wake up in the morning",
        ["joint_pain"]
    ),
    (
        "I've been coughing up thick green phlegm all week",
        ["cough"]
    ),
    (
        "My anxiety is through the roof and I keep having panic attacks",
        ["anxiety"]
    )
]

def calculate_metrics():
    print("Loading BERT Symptom Analyzer... (this may take a moment)")
    analyzer = BERTSymptomAnalyzer()
    print("Analyzer loaded successfully!\n")

    total_tp = 0  # True Positives: properly identified symptoms
    total_fp = 0  # False Positives: incorrectly identified symptoms
    total_fn = 0  # False Negatives: missed symptoms
    total_tn = 0  # True Negatives

    # All possible symptoms from the analyzer's embeddings/combinations
    from dataset.symptoms_db import SYMPTOM_KEYWORDS
    TOTAL_SYMPTOMS = len(SYMPTOM_KEYWORDS)

    print("Running evaluation on the dataset...\n")

    for text, expected in EVALUATION_DATASET:
        # Get predictions
        results = analyzer.analyze(text)
        predicted_symptoms = list(results.get("extracted_symptoms", {}).keys())
        
        # Sets for efficient comparison
        expected_set = set(expected)
        predicted_set = set(predicted_symptoms)

        # Calculate TP, FP, FN for this example
        tp = len(expected_set.intersection(predicted_set))
        fp = len(predicted_set - expected_set)
        fn = len(expected_set - predicted_set)
        tn = TOTAL_SYMPTOMS - (tp + fp + fn)

        total_tp += tp
        total_fp += fp
        total_fn += fn
        total_tn += tn

        print(f"Text: '{text}'")
        print(f"  Expected : {list(expected_set)}")
        print(f"  Predicted: {list(predicted_set)}")
        print(f"  -> TP: {tp}, FP: {fp}, FN: {fn}\n")

    # Calculate final metrics
    # Precision = TP / (TP + FP)
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0

    # Recall = TP / (TP + FN)
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0

    # F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Accuracy = (TP + TN) / (TP + TN + FP + FN)
    accuracy = (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn) if (total_tp + total_tn + total_fp + total_fn) > 0 else 0.0

    output = "=" * 40 + "\n"
    output += "FINAL EVALUATION METRICS:\n"
    output += "=" * 40 + "\n"
    output += f"Total True Positives (TP) : {total_tp}\n"
    output += f"Total False Positives (FP): {total_fp}\n"
    output += f"Total False Negatives (FN): {total_fn}\n"
    output += "-" * 40 + "\n"
    output += f"Accuracy  : {accuracy * 100:.2f}%\n"
    output += f"Precision : {precision * 100:.2f}%\n"
    output += f"Recall    : {recall * 100:.2f}%\n"
    output += f"F1-Score  : {f1_score * 100:.2f}%\n"
    output += "=" * 40 + "\n"
    output += "Note: Expand EVALUATION_DATASET with more queries to get more reliable overall metrics.\n"
    
    print(output)
    
    # Save the metrics to the results folder
    import os
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, "metrics.txt"), "w") as f:
        f.write(output)
    print(f"Metrics saved to {os.path.join('results', 'metrics.txt')}")

    # Generate Confusion Matrix Plot
    cm = np.array([[total_tn, total_fp],
                   [total_fn, total_tp]])
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Low Risk', 'High Risk'], 
                yticklabels=['Low Risk', 'High Risk'])
    plt.title('Confusion Matrix: Risk Classification')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'), dpi=300)
    plt.close()

    # Generate Performance Metrics Bar Chart
    metrics_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    metrics_values = [accuracy * 100, precision * 100, recall * 100, f1_score * 100]

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=metrics_labels, y=metrics_values, hue=metrics_labels, legend=False, palette='viridis')
    plt.title('BERT Classification Model Evaluation Metrics')
    plt.ylabel('Percentage (%)')
    plt.ylim(0, 110)

    # Add values on top of bars
    for i, v in enumerate(metrics_values):
        ax.text(i, v + 2, f"{v:.2f}%", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'evaluation_metrics.png'), dpi=300)
    plt.close()

    print("Graphs successfully generated and saved in 'results' directory!")

if __name__ == '__main__':
    calculate_metrics()
