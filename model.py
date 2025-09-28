# model.py
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
import random

import spacy

# Load spaCy English model once
nlp = spacy.load("en_core_web_sm")



# Define quality mapping based on rating
def map_rating_to_quality(rating):
    if rating >= 9:
        return 2  # High Quality
    elif rating >= 6:
        return 1  # Medium Quality
    else:
        return 0  # Low Quality

# Load pre-trained DistilBERT tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=3
)

QUALITY_LABELS = {0: "Low Quality", 1: "Medium Quality", 2: "High Quality"}

# Step 1: Generate initial ML predictions (meaningful quality)
def generate_initial_output(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for idx, text in enumerate(df['text']):
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            pred_label = torch.argmax(F.softmax(logits, dim=1)).item()
        # If rating exists, map to quality (optional for supervised training)
        if 'rating' in df.columns and not pd.isnull(df.loc[idx, 'rating']):
            pred_label = map_rating_to_quality(df.loc[idx, 'rating'])
        results.append(QUALITY_LABELS[pred_label])
    df['initial_output'] = results
    return df

# Step 2: Apply simple Q-learning style refinement (simulated)
def apply_q_learning(df: pd.DataFrame) -> pd.DataFrame:
    refined_results = []
    for idx, row in df.iterrows():
        current_quality = row['initial_output']
        # Map back to numeric for Q-learning adjustment
        numeric = [k for k,v in QUALITY_LABELS.items() if v==current_quality][0]
        # Simulate reward-based refinement using rating
        if 'rating' in df.columns and not pd.isnull(row['rating']):
            reward = map_rating_to_quality(row['rating'])
            # Adjust towards reward
            numeric = max(0, min(2, numeric + (reward - numeric)))
        else:
            # Random small adjustment if no rating
            numeric = max(0, min(2, numeric + random.choice([-1,0,1])))
        refined_results.append(QUALITY_LABELS[numeric])
    df['refined_output'] = refined_results
    return df

# Step 3: Mask sensitive info for privacy
def anonymize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace sensitive information (names, dates, emails, organizations, locations, etc.) with [MASKED].
    """
    def mask_sensitive(text):
        doc = nlp(text)
        masked_text = text
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "EMAIL", "DATE", "GPE", "ORG", "CARDINAL"]:
                masked_text = masked_text.replace(ent.text, "[MASKED]")
        return masked_text

    df['text'] = df['text'].apply(mask_sensitive)
    return df

