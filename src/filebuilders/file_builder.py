import abc
import os
from datetime import datetime


class FileBuilder(abc.ABC):

    def __init__(self, google_drive_connector, output_dir, file_name, file_extension): 
        self.google_drive_connector = google_drive_connector
        self.file_name = file_name + file_extension  
        self.output_dir = output_dir        

    @abc.abstractmethod
    def build(self, file_extension, output_dir, data, domain_object_config, upload_to_google_drive):      
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

    def open_file(self):
        self.file = open(os.path.join(self.output_dir, self.file_name), 'a+')

    def close_file(self):
        self.file.close()

    
   
