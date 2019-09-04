import abc
import os
from datetime import datetime


class FileBuilder(abc.ABC):

    def __init__(self, google_drive_connector, domain_object_config):
        file_name = domain_object_config['file_name']
        file_extension = domain_object_config['file_builder_name'].lower()

        self.__google_drive_connector = google_drive_connector
        self.__file_name = file_name + '_{}.' + file_extension  
        self.__output_dir = domain_object_config['output_directory']     
        self.__root_element_name = domain_object_config['root_element_name']   
        self.__item_name = domain_object_config['item_name']

    @abc.abstractmethod
    def build(self, file_number, data, upload_to_google_drive):      
        pass

    def upload_to_google_drive(self, local_folder_name, file_name):        
        root_folder_id = self.__google_drive_connector.root_folder_id
        todays_date = datetime.today().strftime('%Y-%m-%d')

        # Check if a folder for today's date exists, create if it doesn't
        folder_id = self.__google_drive_connector.get_folder_id(todays_date, root_folder_id)
        if folder_id == None:
            folder_id = self.__google_drive_connector.create_folder(todays_date, root_folder_id)    

        # Check if the file already exists, create if it doesn't, update if it does
        file_id = self.__google_drive_connector.get_file_id(file_name, folder_id)
        if file_id == None:
            self.__google_drive_connector.create_file(local_folder_name, file_name, folder_id)
        else:
            self.__google_drive_connector.update_file(local_folder_name, file_name, file_id)

    def open_file(self):
        self.file = open(os.path.join(self.__output_dir, self.__file_name), 'a+')

    def close_file(self):
        self.file.close()
   
    def get_output_directory(self):
        return self.__output_dir

    def get_file_name(self):
        return self.__file_name

    def get_google_drive_connector(self):
        return self.__google_drive_connector

    def get_root_element_name(self):
        return self.__root_element_name

    def get_item_name(self):
        return self.__item_name
