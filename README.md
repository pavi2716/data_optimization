# Data Optimization Microservice

# Project Overview

This project is a Python-based microservice that ingests JSON data, cleans it, extracts metadata, performs ML-based predictions with reinforcement learning refinement, anonymizes sensitive information, manages assets, and stores the results in simulated external storage.
The microservice also integrates sentiment analysis to enhance the data insights.


# Features

Step 1: Data ingestion & cleaning (handles missing fields, assigns defaults)

Step 2: Metadata extraction using spaCy (named entities extraction)

Step 3: ML-based predictions with DistilBERT and Q-learning refinement

Step 4: API management with key authentication & basic rate limiting

Step 5: Asset management (assigns unique asset IDs to each record)

Step 6: Data persistence in simulated external storage (Azure Blob / SharePoint simulation)

Sentiment Analysis: Added to refined data for additional insights

Data Privacy: Names and sensitive fields masked as [MASKED]

# Project File Structure

microservice_task/
│── app.py               # FastAPI main app
│── data_optimizer.py    # Data ingestion, cleaning, metadata extraction
│── model.py             # ML model, Q-learning refinement, anonymization
│── storage_sim.py       # Simulated external storage functionality
│── input_data.json      # Sample input
│── refined_data.json    # Output of optimized data
│── metadata.json        # Extracted metadata
│── requirements.txt     # Dependencies
│── blob_storage/        # Simulated blob storage
│── logs/                # Action logs
│── .gitignore           # Ignored files/folders
│── README.md            # Project documentation


# Setup Instructions

1.Clone the repository

git clone https://github.com/pavi2716/data_optimization.git
cd data_optimization/microservice_task

2.Create a virtual environment

python -m venv microservice_task

3.Activate the virtual environment

Windows: microservice_task\Scripts\activate

4.Install dependencies

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
      "text": "The guide by [MASKED] was confusing. No rating.",
      "rating": 0,
      "initial_output": 1,
      "refined_output": 1,
      "asset_id": "asset_001",
      "sentiment": "NEGATIVE",
      "timestamp": "2025-08-22T16:00:00Z"
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
