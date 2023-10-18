import requests
import json
import os
from dotenv import load_dotenv


auth_url = "https://carapi.app/api/auth/login"
auth_headers = {
    "Accept": "text/plain",
    "Content-Type": "application/json"
}

# Load environment variables from .env file
load_dotenv()

# Fetch the environment variables
api_token = os.getenv("CARAPI_API_TOKEN")
api_secret = os.getenv("CARAPI_API_SECRET")

auth_payload = {
    "api_token": api_token,
    "api_secret": api_secret
}

auth_response = requests.post(auth_url, headers=auth_headers, json=auth_payload)

if auth_response.status_code == 200:
    token = auth_response.text
else:
    print(f"Failed to authenticate. Status code: {auth_response.status_code}, Response: {auth_response.text}")

import requests
import json
import time  # If you decide to use sleep to rate-limit

def fetch_data_from_endpoint(token, endpoint, sort="id", direction="asc", year="2020", verbose=None):
    url = f"https://carapi.app/api/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "sort": sort,
        "direction": direction,
        "year": year
    }
    if verbose is not None:
        params["verbose"] = verbose

    all_data = []
    current_page = 1
    max_pages = None  # Will be set later

    while True:
        # print(f"Fetching data for page {current_page}")  # Debugging statement

        params["page"] = current_page  # Update the page number in the query parameters

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to get data for page {current_page}. Status code: {response.status_code}, Response: {response.text}")
            break

        response_json = response.json()
        if max_pages is None:
            max_pages = response_json['collection']['pages']
            # print(f"Total pages to fetch: {max_pages}")  # Debugging statement

        all_data.extend(response_json['data'])

        print(f"Successfully fetched data for page {current_page}. Total records: {len(all_data)}")  # Debugging statement

        if 'next' in response_json['collection'] and response_json['collection']['next']:
            current_page += 1
        else:
            print("Reached the end of the data.")  # Debugging statement
            break

        if current_page > max_pages:
            print("Breaking out of loop, fetched all pages.")  # Debugging statement
            break

        # Uncomment the next line if you want to introduce a delay between requests to prevent rate-limiting
        # time.sleep(1)

    return all_data


# Usage
endpoint = "engines"  # Replace this with any endpoint you're targeting

data = fetch_data_from_endpoint(token, endpoint, sort="id", direction="asc", year="2020", verbose="yes")

# Save to a file with a dynamic name based on the endpoint
filename = f"./data/{endpoint}_data.json"
with open(filename, 'w') as f:
    json.dump(data, f)