import argparse
import importlib
import json
import os
import timeit
import sqlite3
import logging
from cache import Cache
from sqlite_database import Sqlite_Database

# Return a specified class from package.module
def get_class(package_name, module_name, class_name):
    return getattr(importlib.import_module(package_name+'.'+module_name), class_name)

# Create a list comprehension of the file builder configuration which matches the provided name
def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(lambda file_builder: file_builder['name'] == file_builder_name, file_builders))[0]

# Facillitate the domain object generation procedure
def process_domain_object(domain_obj_config, cache, dependency_db,file_builder):
    domain_obj_class = get_class('domainobjects', domain_obj_config['module_name'], domain_obj_config['class_name'])
    domain_obj = domain_obj_class(cache, dependency_db, file_builder)
    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    domain_obj.generate(record_count, custom_args, domain_obj_config)

# Configure a parser for command line argument retrieval, and retrieve said arguments 
def get_args():
    parser = argparse.ArgumentParser(description='Generate Random Data for Various Domain Objects')
    parser.add_argument('--config', default='src/config.json', help='JSON Config File Location')
    cl_args = parser.parse_args()
    return cl_args

def main():
    start_time = timeit.default_timer()
    logging.basicConfig(filename='generator.log', filemode='w', format='%(levelname)s : %(message)s', level=logging.INFO)

    cache = Cache()                     # Stores global generation attributes, i.e: tickers, countries of issuance, exchange codes etc.
    dependency_db = Sqlite_Database()   # Stores global generation dependencies, i.e instrument RICs. 
    args = get_args()                   # Stores command line arguments TODO: CHECK THIS IS RIGHT

    with open(args.config) as config_file:
        config = json.load(config_file)
    
    domain_object_configs = config['domain_objects']
    file_builder_configs = config['file_builders']

    for domain_object_config in domain_object_configs:
        logging.info("Now Generating Domain Object: "+domain_object_config['class_name'])
        gen_start_time = timeit.default_timer()
        file_builder_config = get_file_builder_config(file_builder_configs, domain_object_config['file_builder_name'])      
        file_builder = get_class('filebuilders', file_builder_config['module_name'], file_builder_config['class_name']) 
        process_domain_object(domain_object_config, cache, dependency_db, file_builder)
        gen_end_time = timeit.default_timer()
        logging.info("Domain Object: "+domain_object_config['class_name']+" took "+str(gen_end_time-gen_start_time)+" seconds to generate.")

    end_time = timeit.default_timer()
    logging.info("Overall runtime: "+str(end_time-start_time))

if __name__ == '__main__':   
    main()