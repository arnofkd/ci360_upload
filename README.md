#  SAS Customer Intelligence 360 Upload Client: Python

## Overview
This Python script / Notebook enables you to upload local data to CI360 tables.
 

This topic contains the following sections:
* [Configuration](#configuration)
* [Using the Download Script](#using-the-upload/import-script)
    * [Considerations](#considerations)
    * [Running the script](#running-the-script)
* [Contributing](#contributing)
* [License](#license)
* [Additional Resources](#additional-resources)



## Configuration
1. Install Python (version 3 or later) from https://www.python.org/.

   **Tip:** Select the option to add Python to your PATH variable. If you choose the advanced installation option, make sure to install the pip utility.
   
2. Make sure the following modules are installed for Python: `json`, `os`, `PyJWT`, `requests`, `sys`

     In most cases, many of the modules are installed by default. To list all packages that are installed with Python 
     (through pip or by default), use this command:  
     ```python -c help('modules')```
     
     **Tip:** In most situations, you can install the non-default packages with this command:  
     ```pip install backoff pandas PyJWT requests tqdm```
  

3. Create an access point in SAS Customer Intelligence 360.
    1. From the user interface, navigate to **General Settings** > **External Access** > **Access Points**.
    2. Create a new access point if one does not exist.
    3. Get the following information from the access point:  
       ```
        External gateway address: e.g. https://extapigwservice-<server>/marketingGateway  
        Name: ci360_agent  
        Tenant ID: abc123-ci360-tenant-id-xyz  
        Client secret: ABC123ci360clientSecretXYZ  
       ```
4. Download the Python script from this repository and save it to your local machine.

5. In the `config.py` file, set the following variables for your tenant:
   ```
    server = "<servername>"

    tenantId = "<tenantId>"

    secret = "<secret>"

    TableId = "<table/descriptor_id>"

    filename = "<actual_filename.csv>"  
    importName = "<custom_name_of_importjob>"
   ```


## Using the Upload/Import Script

### Considerations
Before starting an upload/import, make a note of the following things:
* The script reads a file that must exist in the import_ready_file folder. If you want to reference a different path, you have to edit the variable "abs_file_path" in the import_job.
* By default, the script is set to read a csv file. You can customize it by editing the variable "json_payload" inside import_job.

### Running the Script

1. Open a command prompt.
2. cd into the directory /python_version
3. run the command $ python import_job
---
**Note:** On Unix-like environments and Macs, the default `py` or `python` command might default to Python 2 if that version is installed. Uninstall earlier versions of Python, or explicitly call Python 3 when you run the script like this example:
```
python3 import_job
```

You can verify which version runs by default with the following command: `python --version`

---


## Contributing

You are welcome to contribute! 


## License

This project is licensed under the MIT (LICENSE).



## Additional Resources
For more information, see [Import Data through the REST API](https://go.documentation.sas.com/doc/en/cintcdc/production.a/cintag/dat-import-rest-toc.html) in the Help Center for SAS Customer Intelligence 360.
