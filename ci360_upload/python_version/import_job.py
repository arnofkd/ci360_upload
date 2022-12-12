# %%
import base64
import jwt
import requests
import json
import os
import config

# %% [markdown]
# Create jwtToken

# %%
encodedSecret = base64.b64encode(bytes(config.secret, 'utf-8'))
token = jwt.encode({'clientID': config.tenantId}, encodedSecret, algorithm='HS256')
# print('\nJWT token: ', token)

# %% [markdown]
# Get presigned S3 URL for file upload
# 

# %%
api_url = f"https://extapigwservice-{config.server}/marketingData/fileTransferLocation"
headers =  {"Content-Type":"application/json","Authorization": f"Bearer {token}"}
response = requests.post(api_url,headers=headers)
if (response.status_code < 400):
    print(response.status_code)
    signedURL = response.json()['signedURL']
else:
    print(response.status_code)
    print(response.reason)


# %% [markdown]
# Upload file to S3

# %%
#get current directory of where script is executed
script_dir = os.path.abspath('')

#create file path
path = f"import_ready_file/{config.filename}"
abs_file_path = os.path.join(script_dir, path)

#create payload
data = open(abs_file_path,'rb')

import_headers = {"Content-Type":"text/csv"}

response = requests.put(signedURL,headers=import_headers,data=data)
if (response.status_code < 400):
        print(response.status_code)
else:
    print(response.status_code)
    print(response.reason)

# %% [markdown]
# Submit an Import Request Job | https://go.documentation.sas.com/doc/en/cintcdc/production.a/cintag/dat-import-rest-submit.htm

# %%
json_payload= {
  "contentName":f"{config.importName}",
  "dataDescriptorId":"9dc18870-f423-4d87-aeca-b7981f0891f7",
  "fieldDelimiter":",",
  "fileLocation":f"{signedURL}",
  "fileType":"CSV",
  "headerRowIncluded": "true",
  "recordLimit":0,
  "updateMode":"upsert"  
}


# %%
api_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs"
response = requests.post(api_url,json=json_payload,headers=headers)
if (response.status_code < 400):
        print(response.status_code)
        importId = response.json()['id']
else:
    print(response.status_code)
    print(response.reason)

# %% [markdown]
# Get status of upload

# %%
status_url = f"https://extapigwservice-{config.server}/marketingData/importRequestJobs/{importId}"
response = requests.get(status_url,headers=headers)
if (response.status_code < 400):
    print(response.status_code)
    print(response.json()["statusDescription"])
else:
    print(response.status_code)
    print(response.reason)

# %%



