# Import libraries and variables from local config file

import base64
import jwt
import requests
import json
import os
import config
import time
import logging

# Create jwtToken

encoded_secret = base64.b64encode(bytes(config.secret, 'utf-8'))
token = jwt.encode({'clientID': config.tenantId},
                   encoded_secret, algorithm='HS256')

# Define a helper function to make requests with retries using exponential backoff (wait_time 3,6,12s)

MAX_NETWORK_RETRIES = 3


def make_request(method, url, **kwargs):
    wait_time = 3
    for retry in range(MAX_NETWORK_RETRIES):
        try:
            response = method(url, **kwargs)
            if (response.status_code < 400):
                print(response.status_code)
                return response
        except requests.exceptions.Timeout:
            print(
                f"Request timed out. Retrying (attempt {retry+1} of {MAX_NETWORK_RETRIES}) in {wait_time} seconds")
            time.sleep(wait_time)
            wait_time *= 2
        except requests.exceptions.RequestException as e:
            print(f"{response.status_code} | Request failed with error: {e}")
            logging.error(f"Request failed with error: {e}")
            raise


# Use a session to persist the HTTP connection

with requests.Session() as session:
    # Set the authorization header for all requests made through the session
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Content-Type"] = "application/json"

    # Make a POST request to get a signed URL for file upload
    api_url = f"https://extapigwservice-{config.server}/marketingData/fileTransferLocation"
    response = make_request(session.post, api_url)
    signed_url = response.json()['signedURL']

    # Read the file and upload it to the signed URL | Using manual header
    with open(config.filepath, 'rb') as file:
        import_headers = {"Content-Type": "text/csv"}
        make_request(requests.put, signed_url,
                     headers=import_headers, data=file)

    # Import the uploaded file to your CI360 table
    config.json_payload['fileLocation'] = f"{signed_url}"
    api_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs"
    response = make_request(session.post, api_url, json=config.json_payload)
    import_id = response.json()['id']

    # Check status of the import request
    status_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs/{import_id}"
    response = make_request(session.get, status_url)
    status = response.json()['status']
    statusDesc = response.json()['statusDescription']
    print(f"Current status: {status}. Description:{statusDesc}")
