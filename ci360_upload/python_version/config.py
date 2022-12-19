import os

server = "<servername>"

tenantId = "<tenantId>"

secret = "<secret>"

TableId = "<table/descriptor_id>"

filename = "<actual_filename.csv>"

# default: current dir of where script is executed and append custom path and file
filepath = os.path.join(os.path.abspath(''), f"import_ready_file/{filename}")

json_payload = {
    "contentName": "Import_Job_1",
    "dataDescriptorId": f"{TableId}",
    "fieldDelimiter": ",",
    "fileLocation": "S3_signed_url_placeholder",
    "fileType": "CSV",
    "headerRowIncluded": "true",
    "recordLimit": 0,
    "updateMode": "upsert"
}
