import requests
import json
from datetime import datetime
import time
import pandas as pd
import pprint
import re

BASE_URL =  "https://apache-api.onrender.com/logs" 

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
    

# # extract() # Uncomment to run the extract function directly
# # Testing extract() function
# streams = extract()
# for stream in streams:
#     data = stream["response"]
    
#     # print(type(data)) # Check the type of data received

#     if isinstance(data, list):
#         for item in data:
#             pprint.pprint(f"{stream['timestamp']} — {item.get('raw_logs', item)}")

#     elif isinstance(data, dict):
#         raw_logs = data.get("raw_logs")
#         if isinstance(raw_logs, list):
#             for log in raw_logs:
#                 print(f"{stream['timestamp']} — {log}")
#         else:
#             print(f"{stream['timestamp']} — {raw_logs}")

    


def processor(log_content):
    """
    Processes the log content and extracts relevant information.
    """
    log_entries = []
    error_entries = []

    # Regular expression to match log entries
    log_pattern = re.compile(
        r'^(?P<ipaddress>\d{1,3}(?:\.\d{1,3}){3}) \- - \[(?P<timestamp>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>[^"]+) (?P<protocol>[^"]+)" (?P<status_code>\d{3}) (?P<bytes_sent>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"$',
        re.MULTILINE
    )

    for line in log_content.splitlines():
        match = log_pattern.match(line)
        if match:
            entry = {
                'ipaddress': match.group('ipaddress'),
                'timestamp': match.group('timestamp'),
                'method': match.group('method'),
                'path': match.group('path'),
                'protocol': match.group('protocol'),
                'status_code': match.group('status_code'),
                'bytes_sent': match.group('bytes_sent'),
                'referrer': match.group('referrer'),
                'user_agent': match.group('user_agent')
            }
            log_entries.append(entry)
        else:
            # keep non-matching lines for inspection
            error_entries.append(line)

    return log_entries, error_entries



def etl():
    print("Starting ETL process...")
   
    streams = extract()

    for stream in streams:
        # basic error handling if extract() yields an error dict
        if isinstance(stream, dict) and "error" in stream:
            print(f"Error from extract(): {stream['error']}")
            break

        timestamp = stream.get("timestamp")
        data = stream.get("response")

        # Normalize to list of strings
        if isinstance(data, list):
            raw_list = [item.get('raw_logs', item) if isinstance(item, dict) else item for item in data]
        elif isinstance(data, dict):
            raw = data.get('raw_logs', data)
            if isinstance(raw, list):
                raw_list = raw
            else:
                raw_list = [raw]
        else:
            raw_list = [str(data)]

        # Ensure strings, then join into one text block for processor()
        raw_list = [str(r) for r in raw_list]
        log = "\n".join(raw_list)

        # Call processor inside the loop (this was the main missing behavior)
        log_entries, error_entries = processor(log)

        # Print results so you see output
        print(f"{timestamp} — parsed {len(log_entries)} entries, {len(error_entries)} errors")
        if log_entries:
            pprint.pprint(log_entries[:3])   # show up to first 3 parsed entries
        if error_entries:
            print("Sample non-matching lines (errors):")
            pprint.pprint(error_entries[:3])

        # To avoid an infinite run while testing, you can break after the first iteration.
        # Remove the next line if you want continuous streaming:
        break


# Ensure the script runs when executed directly
if __name__ == "__main__":
    etl()
