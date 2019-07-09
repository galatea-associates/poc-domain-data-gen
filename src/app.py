import argparse
import csv
import datetime
import importlib
import json
import os
import logging
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from functools import partial
from common_data_generator import CommonDataGenerator

common_data_generator = CommonDataGenerator()

def process_domain_object(domain_obj_config):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class()
    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    return domain_obj.generate(common_data_generator, record_count, custom_args)

def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(lambda file_builder: file_builder['name'] == file_builder_name, file_builders))[0]

def get_file_builder(file_builder_config):
    file_builder_class = getattr(importlib.import_module('filebuilders.' + file_builder_config['module_name']), file_builder_config['class_name'])
    return file_builder_class()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=r'src\config.json', help='JSON config file location')
    return parser.parse_args()

def main():
    args = get_args()
    date = datetime.datetime.utcnow() - datetime.timedelta(days=4)
    common_data_generator.set_date(date)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    with open(args.config) as config_file:
        config = json.load(config_file)

    domain_objects = config['domain_objects']
    file_builders = config['file_builders']
    shared_domain_obj_args = config['shared_domain_object_args']

    for domain_object in domain_objects:     
        logging.info("Generating %s object(s) of Domain Object %s",domain_object['record_count'],domain_object['module_name'])           
        domain_obj_result = process_domain_object(domain_object)
        file_builder_config = get_file_builder_config(file_builders, domain_object['file_builder_name'])      
        file_builder = get_file_builder(file_builder_config)      
        file_builder.build(domain_object['output_directory'], domain_object['file_name'], file_builder_config['file_extension'], 
            domain_obj_result, domain_object['max_objects_per_file']) 
        logging.info("Generated %s object(s) of Domain Object %s",domain_object['record_count'],domain_object['module_name'])    

if __name__ == '__main__':   
    main()