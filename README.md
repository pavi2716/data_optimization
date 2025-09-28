# Data Optimization Microservice

## Project Overview

This project is a **Python-based microservice** that ingests JSON data, cleans it, extracts metadata, performs ML-based predictions with **DistilBERT**, applies **Q-learning refinement** to improve output quality, anonymizes sensitive information, manages assets, and stores results in **simulated external storage**.  

The microservice also integrates **sentiment analysis** to enhance data insights. DistilBERT now predicts **meaningful quality labels** (Low, Medium, High) based on ratings, providing interpretable user satisfaction metrics.

## Features

1. **Data Ingestion & Cleaning**  
   - Handles missing fields and assigns default values for ratings and timestamps.

2. **Metadata Extraction**  
   - Uses **spaCy** for named entity extraction.  
   - Stores extracted metadata in `metadata.json`.

3. **ML-based Predictions**  
   - **DistilBERT** predicts **initial text quality**: Low / Medium / High Quality.  
   - **Q-learning refinement** adjusts predictions based on user rating or simulated rewards.  

4. **Data Privacy**  
   - Sensitive fields (e.g., names) are anonymized as `[MASKED]`.

5. **Asset Management**  
   - Assigns unique `asset_id` to each record for traceability.

6. **Sentiment Analysis**  
   - Adds a sentiment label (Positive / Negative / Neutral) for additional insights.  

7. **API Management**  
   - Key-based authentication and basic rate limiting for security.  

8. **Data Persistence**  
   - Stores refined data locally and in **simulated external storage** (`blob_storage/`).  
   - Includes metadata such as `asset_id` and `timestamp`.  


## Project File Structure

microservice_task/
│── app.py # FastAPI main app
│── data_optimizer.py # Data ingestion, cleaning, metadata extraction
│── model.py # DistilBERT model, Q-learning refinement, anonymization
│── storage_sim.py # Simulated external storage functionality
│── input_data.json # Sample input
│── refined_data.json # Output of optimized data
│── metadata.json # Extracted metadata
│── requirements.txt # Dependencies
│── blob_storage/ # Simulated blob storage
│── logs/ # Action logs
│── Output_Evidence/ # Example output/evidence folder
│── .gitignore # Ignored files/folders
│── README.md # Project documentation

# Setup Instructions

## 1.Clone the repository

git clone https://github.com/pavi2716/data_optimization.git
cd data_optimization/microservice_task

## 2.Create a virtual environment

python -m venv microservice_task

## 3.Activate the virtual environment

Windows: microservice_task\Scripts\activate

## 4.Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Running the FastAPI Server

Start FastAPI server: uvicorn app:app --reload

# Testing API with Postman

1.POST /optimize

Description: Ingests JSON input, cleans data, extracts metadata, performs ML refinement, anonymizes sensitive info, assigns asset IDs, and stores data locally & in simulated blob storage.

URL: http://127.0.0.1:8000/optimize

Method: POST

Headers:

Content-Type: application/json

* Body: (raw JSON)
[
  {
    "text": "The guide by Tom was confusing. No rating.",
    "rating": null,
    "timestamp": "2025-08-22T16:00:00Z"
  }
]

* Response:
{
  "status": "success",
  "message": "Data optimized successfully!"
}

2.GET /retrieve

Description: Retrieves processed/refined data (requires API key).

URL: http://127.0.0.1:8000/retrieve

Method: GET

* Headers:

x-api-key: 12345

* Response:
{
    "status": "success",
    "data": [
        {
            "text": "[MASKED] from HR rated the document 7/10 on 2025-08-22T14:00:00Z",
            "rating": 7,
            "timestamp": "2025-08-22T14:00:00Z",
            "initial_output": "Medium Quality",
            "refined_output": "Medium Quality",
            "asset_id": "asset_001",
            "sentiment": "NEGATIVE"
        }
    ]
}

# Deployment Plan

Can deploy as a serverless API using AWS Lambda + API Gateway or Azure Functions.

Dockerization is optional for containerized deployment.

ML model inference is lightweight (DistilBERT) and can be hosted on a cloud ML platform.

# External Storage

Simulated blob storage is implemented in blob_storage/.

Data is saved with metadata (asset_id, timestamp).

In production, can replace with Azure Blob Storage or SharePoint Lists.

# Data Privacy Compliance

Sensitive names are masked as [MASKED].

No personal data is stored in logs or external storage.
