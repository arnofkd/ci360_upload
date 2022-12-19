# %%
import base64
import jwt
import requests
import json
import os
import config
import time


MAX_RETRIES = 3
# %% [markdown]
# Create jwtToken

# %%
encodedSecret = base64.b64encode(bytes(config.secret, 'utf-8'))
token = jwt.encode({'clientID': config.tenantId},
                   encodedSecret, algorithm='HS256')
# print('\nJWT token: ', token)

# %% [markdown]
# Get presigned S3 URL for file upload

api_url = f"https://extapigwservice-{config.server}/marketingData/fileTransferLocation"
headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {token}"}

for retry in range(MAX_RETRIES):
    try:
        response = requests.post(api_url, headers=headers)
        if (response.status_code < 400):
            print(response.status_code)
            signedURL = response.json()['signedURL']
            break

    except requests.exceptions.Timeout:
        # request timed out, retry the request
        print(
            f"Request timed out. Retrying (attempt {retry+1} of {MAX_RETRIES})")
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        # some other error occurred, break out of the loop
        print(f"{response.status_code} | Request failed with error: {e}")
        break


# %% [markdown]
# Upload file to S3

data = open(config.filepath, 'rb')
import_headers = {"Content-Type": "text/csv"}

for retry in range(MAX_RETRIES):
    try:
        response = requests.put(signedURL, headers=import_headers, data=data)
        if (response.status_code < 400):
            print(response.status_code)
            break

    except requests.exceptions.Timeout:
        # request timed out, retry the request
        print(
            f"Request timed out. Retrying (attempt {retry+1} of {MAX_RETRIES})")
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        # some other error occurred, break out of the loop
        print(f"{response.status_code} | Request failed with error: {e}")
        break


# %% [markdown]
# Submit an Import Request Job | https://go.documentation.sas.com/doc/en/cintcdc/production.a/cintag/dat-import-rest-submit.htm

config.json_payload['fileLocation'] = f"{signedURL}"

api_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs"

for retry in range(MAX_RETRIES):
    try:
        response = requests.post(
            api_url, json=config.json_payload, headers=headers)
        if (response.status_code < 400):
            print(response.status_code)
            importId = response.json()['id']
            break

    except requests.exceptions.Timeout:
        # request timed out, retry the request
        print(
            f"Request timed out. Retrying (attempt {retry+1} of {MAX_RETRIES})")
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        # some other error occurred, break out of the loop
        print(f"{response.status_code} | Request failed with error: {e}")
        break

# %% [markdown]
# Get status of upload

status_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs/{importId}"

for retry in range(MAX_RETRIES):
    try:
        response = requests.get(status_url, headers=headers)
        if (response.status_code < 400):
            print(response.status_code)
            print(response.json()["statusDescription"])

            break

    except requests.exceptions.Timeout:
        # request timed out, retry the request
        print(
            f"Request timed out. Retrying (attempt {retry+1} of {MAX_RETRIES})")
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        # some other error occurred, break out of the loop
        print(f"{response.status_code} | Request failed with error: {e}")
        break
# %%
