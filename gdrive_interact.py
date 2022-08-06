from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
import os 


class client:
	pass



def set_client_config_path(path_to_secrets_file):	
	GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = path_to_secrets_file


def authenticate_client(creds_path):

	client.gauth = GoogleAuth()
	gauth=client.gauth

	# Try to load saved client credentials
	gauth.LoadCredentialsFile(creds_path)

	if gauth.credentials is None:
	    # Authenticate if they're not there
	    gauth.GetFlow()
	    gauth.flow.params.update({'access_type': 'offline'})
	    gauth.flow.params.update({'approval_prompt': 'force'})
	    gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
	    # Refresh them if expired
	    gauth.Refresh()
	else:
	    # Initialize the saved creds
	    gauth.Authorize()

	# Save the current credentials to a file
	gauth.SaveCredentialsFile(creds_path)  #Note that credentials will expire after some time and may not refresh. When this happens, delete the mycreds.txt file and run the program again. A new and valid mycreds.txt will automatically be created.
	client.drive = GoogleDrive(client.gauth)

	return client



def list_files(client, folder_id):

	# authenticate_client()

	return client.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()


def get_id(client, folder_path):

	fileID = None

	try:

		folder_path = folder_path.split('/')

		fileList = client.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

		for file in fileList:
			if file['title']==folder_path[0]:
				fileID = file['id']
				break
		folder_path.pop(0)

		for folder_name in folder_path:
			fileList = client.drive.ListFile({'q': f"'{fileID}' in parents and trashed=false"}).GetList()
			for file in fileList:
				if file['title']==folder_name:
					fileID = file['id']
					break

	except:

		fileID = False

	finally:

		return fileID


def upload_file(client, target_folder_path , home_path, file_name):

	# authenticate_client()

	target_id = get_id(client, target_folder_path)
	if target_id == False:
		print(f"[ ERROR in gprocesses.py ] : {target_folder_path} not found.")
		return False
	home_path = rf"{home_path}"

	f = client.drive.CreateFile({
		'title': file_name, 
		'parents': [{'id': target_id}]
		}) 
	f.SetContentFile(os.path.join(home_path, file_name)) 
	f.Upload()

# Example: upload_file('<drive_folder_name>/<drive_folder_name>/.../<file_name>',rf"C:/.../<system_directory_name>", "<file_name>")



def download_file(client, target_file_path, home_path):

	# authenticate_client()

	target_id = get_id(client, target_file_path)
	if target_id == False:
		print(f"[ ERROR in gprocesses.py ] : {target_file_path} not found.")
		return False
	home_path = rf"{home_path}"

	file = client.drive.CreateFile({'id': target_id})
	working_path = os.getcwd()
	os.chdir(home_path)
	file.GetContentFile(file['title'])
	os.chdir(working_path)


# Example: download_file("<drive_folder_name>/<drive_folder_name>/.../<file_name>", "C:/.../<system_directory_name>")


def download_folder(client, target_folder_path, home_path, files_only = True):
	#If files_only = True, only files will be downloaded. If files_only = False, parent folder containing the files will be downloaded along with its contents.
	# authenticate_client()
	
	working_path = os.getcwd()

	target_id = get_id(client, target_folder_path)

	if target_id == False:
		print(f"[ ERROR in gprocesses.py ] : {target_folder_path} not found.")
		return False
	home_path = rf"{home_path}"

	if files_only == False:
		home_path = os.path.join(home_path,target_folder_path.split('/')[len(target_folder_path.split('/'))-1])
		print(home_path)
		os.mkdir(home_path, 0o666)

	files=list_files(client, target_id)
	for file in files:
		file = client.drive.CreateFile({'id': file['id']})
		os.chdir(home_path)
		file.GetContentFile(file['title'])
		os.chdir(working_path)


# download_folder ("<drive_folder_name>/<drive_folder_name>/.../<drive_folder_name>", "C:/.../<system_directory_name>")