import pandas as pd
import json
from datetime import datetime
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def ingest_and_clean(input_file='input_data.json', output_file='cleaned_data.json'):
    """
    Ingest JSON input, clean missing fields, and save cleaned data.
    """
    # Load JSON
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]

    # Create DataFrame
    df = pd.DataFrame(data)

    # Fill missing ratings
    if 'rating' in df.columns:
        if df['rating'].isnull().all():
            df['rating'] = 0  # default if all are null
        else:
            df['rating'] = df['rating'].fillna(df['rating'].mean())

    # Fill missing timestamps
    if 'timestamp' in df.columns:
        df['timestamp'] = df['timestamp'].fillna(datetime.now().isoformat())

    # Save cleaned data
    df.to_json(output_file, orient='records', indent=4)
    return df

def extract_metadata(df, output_file='metadata.json'):
    """
    Extract named entities using spaCy and save metadata.
    """
    metadata_list = []

    for idx, row in df.iterrows():
        doc = nlp(row['text'])
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        metadata_list.append({
            "text": row['text'],
            "entities": entities,
            "rating": row['rating'],
            "timestamp": row['timestamp']
        })

    # Save metadata
    with open(output_file, 'w') as f:
        json.dump(metadata_list, f, indent=4)

    return metadata_list
