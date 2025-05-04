import sys
import os 
import json
#from dhanhq import marketfeed
import os
import pandas as pd
from datetime import datetime, timedelta, time as dtime
import time
from instruments_list import * 


# Function to load user credentials based on uid
def load_user_credentials(uid):
    file_path = os.path.join(os.path.dirname(__file__), uid, f"{uid}_userdetails.json")
    try:
        with open(file_path, "r") as file:
            user_details = json.load(file)
            client_id = user_details.get("dhan_client_id")
            access_token = user_details.get("access_token")

            if not client_id or not access_token:
                raise ValueError("Incomplete user details in JSON file.")

            return client_id, access_token
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)

if len(sys.argv) < 2:
    print("Error: UID argument missing.")
    sys.exit(1)

uid = sys.argv[1]
# Load credentials
client_id, access_token = load_user_credentials(uid)
print(f"client_id={client_id}, access_token={access_token}")



version = "v2"

print("Starting data collection...")
data = marketfeed.DhanFeed(client_id, access_token, instruments, version)
data.run_forever()  # Assuming this is non-blocking or runs in a separate thread

# -----------------------
# MAIN LIVE FEED PROCESSING LOOP
# -----------------------
while True:
    response = data.get_data()
    print(response)
