import requests
import json
from datetime import datetime
import time
import pandas as pd


BASE_URL = "https://apache-api.onrender.com/logs"

def extract():
    
    try:
        """extracting streaming log data."""
        while True:
            """Fetch log data from the API endpoint."""
            response = requests.get(BASE_URL)
            response.raise_for_status()
            data = response.json()
            timestamp = datetime.now().strftime("%H:%M:%S")

            """For local testing with a static file, uncomment below:"""
            # file_path = "/home/dell/logforge/data/logs.json"
            # with open(file_path, "r") as f:
            #     data = json.load(f)
            #     timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Return the fetched data as a dictionary
            yield {
                "response" : data, 
                "timestamp" : timestamp
            }
            
            time.sleep(0.5) # Simulate delay between log entries
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"error": str(e)}
    
streams= extract()

# extract() # Uncomment to run the extract function directly
for stream in streams:
    data = stream["response"]
    
    # print(type(data)) # Check the type of data received

    if isinstance(data, list):
        for item in data:
            print(f"{stream['timestamp']} — {item.get('raw_logs', item)}")

    elif isinstance(data, dict):
        raw_logs = data.get("raw_logs")
        if isinstance(raw_logs, list):
            for log in raw_logs:
                print(f"{stream['timestamp']} — {log}")
        else:
            print(f"{stream['timestamp']} — {raw_logs}")
