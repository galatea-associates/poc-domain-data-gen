import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():  
    creds = build_creds()
    service = build('drive', 'v3', credentials=creds) 
    folder_id = get_folder_id(service, 'test2')

    if folder_id == None:
        folder_id = create_folder(service, 'test2')
    upload_file(service, 'out', 'instruments_001.xml', 'text/xml', folder_id)

def build_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def create_folder(service, folder_name):   
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def get_folder_id(service, folder_name):
    folders = service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='" + folder_name + "' and trashed=false",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          ).execute().get('files', [])

    return folders[0].get('id') if len(folders) > 0 else None

def upload_file(service, file_path, file_name, mime_type, google_folder_id):
    file_location = os.path.join(file_path, file_name)
    file_metadata = {
        'name': file_name,
        'parents': [google_folder_id]
        }
    media = MediaFileUpload(file_location, mimetype=mime_type, resumable=True)    
    request = service.files().create(media_body=media, body=file_metadata)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")


if __name__ == '__main__':
    main()