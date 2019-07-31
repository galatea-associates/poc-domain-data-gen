import argparse
import importlib
import json
import os
import logging
import pandas as pd
from datetime import datetime
from cache import Cache
from google_drive_connector import GoogleDriveConnector

def process_domain_object(domain_obj_config, cache):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class(cache)
    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    return domain_obj.generate(record_count, custom_args)

def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(lambda file_builder: file_builder['name'] == file_builder_name, file_builders))[0]

def get_file_builder(file_builder_config):
    return getattr(importlib.import_module('filebuilders.' + file_builder_config['module_name']), file_builder_config['class_name'])    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=os.path.join('src', 'config.json'), help='JSON config file location')    
    parser.add_argument('--file-builder-name', default='JSON', help='Name of the file builder module to use')
    parser.add_argument('--output-directory', default='out', help='Local output directory')
    parser.add_argument('--upload-to-gdrive', default='false', help='Upload to Google Drive (true/false)')
    parser.add_argument('--gdrive-root', default='root', help='Google Drive root folder ID')
    return parser.parse_args()

def initialise_cache(cache):
    cache.persist_to_cache('currencies', ['USD', 'CAD', 'EUR', 'GBP'])
    cache.persist_to_cache('tickers', pd.read_csv('tickers.csv')['Symbol'].drop_duplicates().values.tolist())
    cache.persist_to_cache('exchanges_countries', [('L', 'UK'), ('N', 'US'),  ('O', 'US'), ('SI', 'SG'), ('VI', 'AT'), 
        ('BM', 'DE'), ('BR', 'BE'), ('TO', 'CA'), ('HK', 'HK'), ('SS', 'CN'), ('F', 'DE'), ('BE', 'DE'), ('PA', 'FR'), ('NZ', 'NZ')])

def main():
    args = get_args()  
    cache = Cache()    
    initialise_cache(cache)
    google_drive_connector = GoogleDriveConnector(args.gdrive_root)

    with open(args.config) as config_file:
        config = json.load(config_file)

    domain_object_configs = config['domain_objects']
    file_builders = config['file_builders']
    shared_domain_obj_args = config['shared_domain_object_args']

    logging.basicConfig(level=logging.INFO)

    for domain_object_config in domain_object_configs: 
        # Get file builder, out dir and G drive flag from domain obj config if it exists, otherwise use the command line args
        file_builder_name = domain_object_config.get('file_builder_name', args.file_builder_name)
        output_dir = domain_object_config.get('output_directory', args.output_directory)
        upload_to_google_drive = domain_object_config.get('upload_to_google_drive', args.upload_to_gdrive)

        domain_obj_result = process_domain_object(domain_object_config, cache)
        file_builder_config = get_file_builder_config(file_builders, file_builder_name)
        file_builder = get_file_builder(file_builder_config)(google_drive_connector)     
        file_builder.build(file_builder_config['file_extension'], output_dir, domain_obj_result, domain_object_config, upload_to_google_drive)  

        logging.info("Generated %s Object(s) of Domain Object %s in %s Format",len(domain_obj_result),
            domain_object_config['module_name'],file_builder_name)        

if __name__ == '__main__':   
    main()