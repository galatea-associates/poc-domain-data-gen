import argparse
import csv
import datetime
import importlib
import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from functools import partial
from shared_data_generator import SharedDataGenerator

data_generator = DataGenerator()

def process_domain_object(domain_obj_config):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class()
    total_record_count = int(domain_obj_config['file_count']) * int(domain_obj_config['objects_per_file'])
    return domain_obj.generate(data_generator, total_record_count)

def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(lambda file_builder: file_builder['name'] == file_builder_name, file_builders))[0]

def get_file_builder(file_builder_config):
    file_builder_class = getattr(importlib.import_module('filebuilders.' + file_builder_config['module_name']), file_builder_config['class_name'])
    return file_builder_class()

def __authenticate_gdrive(creds):
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(creds)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(creds)
    return gauth

def __generate_data_file(output_filename, args, domain_object_count, drive, data_type):
    self.__create_data_file(os.path.join('out', output_filename), domain_object_count, data_type)
    if args.save_to_google_drive == 'true':
        self.__upload_to_gdrive(args.folder_id, drive, output_filename)

def __generate_data_files(args):         
    #gauth = self.__authenticate_gdrive(args.creds)
    #drive = GoogleDrive(gauth)
    drive = None

  

def __upload_to_gdrive(self, folder_id, drive, file_name):
    self.__delete_existing_file(folder_id, drive, file_name)
    self.__add_file(folder_id, drive, file_name)

def __add_file(self, folder_id, drive, file_name):
    file = drive.CreateFile({
        "parents": [{"kind": "drive#fileLink", "id": folder_id}]
    })
    file.SetContentFile('out/' + file_name)
    file['title'] = file_name
    file['mimeType'] = 'text/x-csv'
    file.Upload()

def __delete_existing_file(self, folder_id, drive, file_name):
    file_list = self.__get_all_files_in_folder(folder_id, drive)
    for f in file_list:
        if f['title'] == file_name:
            f.Delete()

def __get_all_files_in_folder(self, folder_id, drive):
    return drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()

# file_name corresponds to the name of the CSV file the function will write
# to n is the number of data entities to write to the CSV file
# data_generator is the function reference that generates the data entity
# of interest
def __create_data_file(self, file_name, n, data_type):
    # w+ means create file first if it does not already exist
    date = datetime.datetime.utcnow() - datetime.timedelta(days=4)
    data_generator.set_date(date)
    with open(file_name, mode='w+', newline='') as file:
      
        # n - 1 because we already wrote to the file once with the entity
        # variable - we do this to get the keys of the dictionary in order
        # to get the field names of the CSV file
        new_date_at = int(n/4)
        counter = 1
        for i in range(1, n):
            if i == counter * new_date_at:
                date += datetime.timedelta(days=1)
                data_generator.set_date(date)
                counter += 1
            entity = self.__generate_data(data_template[data_type])

            writer.writerow(entity)
    data_generator.reset_update_timestamp()

def get_args():
    parser = argparse.ArgumentParser()
    optional_args = {'nargs': '?', 'type': int, 'default': 0}  
    parser.add_argument('--creds', required=True)
    parser.add_argument('--folder-id', required=True)    

    return parser.parse_args()

def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(days=4)
    data_generator.set_date(date)
    with open(r'src\config.json') as config_file:
        config = json.load(config_file)

    domain_objects = config['domain_objects']
    file_builders = config['file_builders']

    for i in range(len(domain_objects)):
        domain_obj_config = domain_objects[i]
        domain_obj_dict = process_domain_object(domain_obj_config)
        file_builder_config = get_file_builder_config(file_builders, domain_obj_config['file_builder_name'])      
        file_builder = get_file_builder(file_builder_config)      
        file_builder.build(domain_obj_config['output_directory'], domain_obj_config['file_name'], file_builder_config['file_extension'], domain_obj_dict, domain_obj_config['objects_per_file'])    

if __name__ == '__main__':   
    main()