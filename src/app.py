import argparse
import importlib
import json
import os
import timeit
import sqlite3
import logging
from cache import Cache
from sqlite_database import Sqlite_Database

def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(lambda file_builder: file_builder['name'] == file_builder_name, file_builders))[0]

def get_file_builder(file_builder_config):
    return getattr(importlib.import_module('filebuilders.' + file_builder_config['module_name']), file_builder_config['class_name'])    

# Configure a parser for command line argument retrieval, and retrieve said arguments 
def get_args():
    parser = argparse.ArgumentParser(description='Generate Random Data for Various Domain Objects')
    parser.add_argument('--config', default='src/config.json', help='JSON Config File Location')
    cl_args = parser.parse_args()
    return cl_args

def process_domain_object(domain_obj_config, cache, dependency_db,file_builder):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class(cache, dependency_db, file_builder)
    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    domain_obj.generate(record_count, custom_args, domain_obj_config, file_builder)

def main():
    start_time = timeit.default_timer()
    
    
    cache = Cache()                     # Stores global generation attributes, i.e: tickers, countries of issuance, exchange codes etc.
    dependency_db = Sqlite_Database()   # Stores global generation dependencies, i.e instrument RICs. 
    args = get_args()                   # Stores command line arguments TODO: CHECK THIS IS RIGHT

    with open(args.config) as config_file:
        config = json.load(config_file)

    domain_object_configs = config['domain_objects']
    file_builder_configs = config['file_builders']

    for domain_object_config in domain_object_configs:
        file_builder_config = get_file_builder_config(file_builder_configs, domain_object_config['file_builder_name'])      
        file_builder = get_file_builder(file_builder_config)(None, domain_object_config['output_directory'], domain_object_config['file_name'], file_builder_config['file_extension']) 
        process_domain_object(domain_object_config, cache, dependency_db, file_builder)
        dependency_db.commit_changes()
    
    end_time = timeit.default_timer()
    print("Run time: ", end_time-start_time)

if __name__ == '__main__':   
    main()