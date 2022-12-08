# gdrive-interact

Python script to enable users to easily upload/download files/folders to/from their Google Drive via Google Drive API.

## Requirements
- Python 
- pip modules
	- pydrive
- Google Drive API credentials file 


## Usage

```py
import gdrive_pyinteract as gdi

# Specify path to credentials file of Google Drive API
gdi.set_client_config_path("client_secrets.json")

# Authenticate 
client = gdi.authenticate_client("creds.txt") # Saves access token credentials to creds.txt. If file does not exist, one-time manual sign-in is done via browser and the file is auto-generated.

# Get id of file/folder
folder_id = gdi.get_id(client, "<drive_folder_name>/<drive_folder_name>/.../<folder_or_file_name>")

# Get list of files in a folder
file_list = gdi.list_files(client, folder_id)

# Upload a file
gdi.upload_file(client, '<drive_folder_name>/<drive_folder_name>/.../<drive_file_name>', "C:/.../<system_directory_name>", "<system_file_name>")

# Upload a folder
gdi.upload_folder(client, '<drive_folder_name>/<drive_folder_name>/.../<drive_folder_name>',rf"C:/.../<system_folder_name>")

# Download a file
gdi.download_file(client, "<drive_folder_name>/<drive_folder_name>/.../<drive_file_name>", "C:/.../<system_directory_name>")

# Download a folder
gdi.download_folder(client, "<drive_folder_name>/<drive_folder_name>/.../<drive_folder_name>", "C:/.../<system_directory_name>", files_only=False) # Set files_only = True if you only want the files within, and not the folder itself
```

## How to create a credentials file
In order to contact and successfully authenticate with your Drive account, you must have a credentials file. In the above example, it is `client_secrets.json`. To create one, see [Google's API Console](console.developers.google.com). Create a project and enable Google Drive API. Download the credentials file.
