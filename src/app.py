import argparse
import importlib
import json
import os
import timeit
import sqlite3
import logging
import pandas as pd
import psutil
from cache import Cache
from sqlite_database import Sqlite_Database

def process_domain_object(domain_obj_config, cache, dependency_db,file_builder):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class(cache, dependency_db, file_builder)
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
    return parser.parse_args()

def initialise_cache(cache):
    cache.persist_to_cache('currencies', ['USD', 'CAD', 'EUR', 'GBP'])
    cache.persist_to_cache('tickers', pd.read_csv('tickers.csv')['Symbol'].drop_duplicates().values.tolist())
    cache.persist_to_cache('exchange_codes', ['L', 'N', 'OQ', 'SI', 'AL', 'VI', 'BB', 'BM', 'BR', 'BG', 'TC', 'TO', 'HK', 'SS',
                                    'FR', 'BE', 'DE', 'JA', 'DE', 'IL', 'VX', 'MFM', 'PA', 'ME', 'NZ'])
    cache.persist_to_cache('cois', ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP'])


def main():
    cache = Cache()
    initialise_cache(cache)
    process = psutil.Process(os.getpid())
    dependency_db = Sqlite_Database()
    
    args = get_args()  

    with open(args.config) as config_file:
        config = json.load(config_file)

    domain_objects = config['domain_objects']
    file_builders = config['file_builders']

    for domain_object in domain_objects:     
        start = timeit.default_timer()
        file_builder_config = get_file_builder_config(file_builders, domain_object['file_builder_name'])      
        file_builder = get_file_builder(file_builder_config)(None, domain_object['output_directory'], domain_object['file_name'], file_builder_config['file_extension']) 
        domain_obj_result = process_domain_object(domain_object, cache, dependency_db, file_builder)     
        print("Memory pre build of: "+domain_object['class_name']+" is: "+str(process.memory_info().rss))
        file_builder.build(file_builder_config['file_extension'], domain_obj_result, domain_object)
        print("Memory post build of: "+domain_object['class_name']+" is: "+str(process.memory_info().rss))
        end = timeit.default_timer()
        print("Time to generate "+domain_object['class_name']+": "+str(end-start))
  
    dependency_db.commit_changes()

if __name__ == '__main__':   
    main()