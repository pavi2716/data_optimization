import os
import json
from datetime import datetime

# Simulated blob storage folder
BLOB_FOLDER = "./blob_storage/"
os.makedirs(BLOB_FOLDER, exist_ok=True)

def save_to_blob(df, filename="refined_data"):
    """
    Save the refined dataframe as a simulated blob.
    Adds timestamp and keeps metadata (asset_id, etc.).
    """
    # Convert dataframe to list of dicts
    data_list = df.to_dict(orient="records")

    # Add storage timestamp
    timestamp = datetime.utcnow().isoformat()
    for item in data_list:
        item["stored_at"] = timestamp

    # Save as .blob file
    blob_path = os.path.join(BLOB_FOLDER, f"{filename}.blob")
    with open(blob_path, "w") as f:
        json.dump(data_list, f, indent=4)

    print(f"Data saved to simulated blob storage: {blob_path}")
    return blob_path
