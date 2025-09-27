# model.py
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
import random

# Load pre-trained DistilBERT tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=3
)

# Step 1: Generate initial ML predictions
def generate_initial_output(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for text in df['text']:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            pred_label = torch.argmax(F.softmax(logits, dim=1)).item()
        results.append(pred_label)
    df['initial_output'] = results
    return df

# Step 2: Apply simple Q-learning style refinement (simulated)
def apply_q_learning(df: pd.DataFrame) -> pd.DataFrame:
    # Simulate reward-based refinement
    df['refined_output'] = df['initial_output'].apply(lambda x: x + random.choice([-1,0,1]))
    df['refined_output'] = df['refined_output'].clip(0,2)  # Keep within valid labels
    return df

# Step 3: Mask sensitive info for privacy
def anonymize_text(df: pd.DataFrame) -> pd.DataFrame:
    # Replace names with [MASKED] (very simple example)
    df['text'] = df['text'].str.replace(r'\b(John|Sarah|Tom|Jane)\b', '[MASKED]', regex=True)
    return df
