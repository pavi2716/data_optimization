# app.py
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import json
import pandas as pd
import time
import os

from data_optimizer import ingest_and_clean, extract_metadata
from model import generate_initial_output, apply_q_learning, anonymize_text
from storage_sim import save_to_blob
from transformers import pipeline

app = FastAPI(title="Data Optimization Microservice")

# --- Step 4: API Key & Logging Setup ---
API_KEY = "12345"  # static key for demo; can be unique per user
LOG_FOLDER = "./logs/"
os.makedirs(LOG_FOLDER, exist_ok=True)
rate_limit = {}  # simple rate limiting dict

# --- Sentiment Analysis Setup ---
sentiment_pipeline = pipeline("sentiment-analysis")  # Hugging Face

# --- Step 1-3: /optimize endpoint ---
@app.post("/optimize")
async def optimize_data(request: Request):
    try:
        # Get JSON payload from API
        input_data = await request.json()

        # Save input temporarily
        with open("input_data.json", "w") as f:
            json.dump(input_data, f, indent=4)

        # Step 1: Data ingestion & cleaning
        df_cleaned = ingest_and_clean("input_data.json")

        # Step 2: Metadata extraction
        metadata = extract_metadata(df_cleaned)  # saved automatically to metadata.json

        # Step 3: ML refinement
        df_ml = generate_initial_output(df_cleaned)  # initial model output
        df_refined = apply_q_learning(df_ml)         # refine outputs
        df_refined = anonymize_text(df_refined)      # anonymize sensitive info

        # --- Step 5: Asset Management ---
        df_refined['asset_id'] = [f"asset_{i+1:03d}" for i in range(len(df_refined))]

        # --- Sentiment Analysis Enhancement ---
        df_refined['sentiment'] = df_refined['text'].apply(lambda x: sentiment_pipeline(x)[0]['label'])

        # Step 6: Save refined data locally & to simulated blob storage
        df_refined.to_json("refined_data.json", orient='records', indent=4)
        save_to_blob(df_refined, filename="refined_data")

        # Logging
        log_file = os.path.join(LOG_FOLDER, "log.json")
        log_entry = {
            "timestamp": time.time(),
            "action": "optimize",
            "records": len(df_refined)
        }
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=4)

        return {"status": "success", "message": "Data optimized successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Step 4: /retrieve endpoint ---
@app.get("/retrieve")
async def retrieve_data(x_api_key: str = Header(...)):
    # Validate API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized API key")

    # Basic rate limiting: 1 request per 5 seconds per key
    now = time.time()
    last_call = rate_limit.get(x_api_key, 0)
    if now - last_call < 5:
        raise HTTPException(status_code=429, detail="Too many requests, try later")
    rate_limit[x_api_key] = now

    try:
        # Load refined data
        with open("refined_data.json", "r") as f:
            data = json.load(f)

        # Log retrieval
        log_file = os.path.join(LOG_FOLDER, "log.json")
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append({
            "timestamp": now,
            "action": "retrieve",
            "records": len(data)
        })
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=4)

        return JSONResponse(content={"status": "success", "data": data})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Refined data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
