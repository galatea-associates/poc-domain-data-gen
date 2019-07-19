import abc
from datetime import datetime


class FileBuilder(abc.ABC):

    def __init__(self, google_drive_connector): 
        self.google_drive_connector = google_drive_connector

    @abc.abstractmethod
    def build(self, file_extension, data, domain_object):      
        pass

    def upload_to_google_drive(self, local_folder_name, file_name):        
        root_folder_id = self.google_drive_connector.root_folder_id
        todays_date = datetime.today().strftime('%Y-%m-%d')

        # Check if a folder for today's date exists, create if it doesn't
        folder_id = self.google_drive_connector.get_folder_id(todays_date, root_folder_id)
        if folder_id == None:
            folder_id = self.google_drive_connector.create_folder(todays_date, root_folder_id)    

        # Check if the file already exists, create if it doesn't, update if it does
        file_id = self.google_drive_connector.get_file_id(file_name, folder_id)
        if file_id == None:
            self.google_drive_connector.create_file(local_folder_name, file_name, folder_id)
        else:
            self.google_drive_connector.update_file(local_folder_name, file_name, file_id)

    
   
