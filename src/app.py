import argparse
import importlib
import json
import os
import logging
import pandas as pd
from cache import Cache
from memutil import MemUtil
from output_data_assembler import OutputDataAssembler
from compressor import Compressor
import time

def get_output_formatter_config(output_formatters, output_formatter_name):
    return list(filter(lambda output_formatter: output_formatter['name'] == output_formatter_name, output_formatters))[0]

def get_output_formatter(output_formatter_config):
    output_formatter_class = getattr(importlib.import_module('outputformatters.' + output_formatter_config['module_name']), output_formatter_config['class_name'])
    return output_formatter_class()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=r'src\config.json', help='JSON config file location')
    return parser.parse_args()

def initialise_cache(cache):
    cache.persist_to_cache('currencies', ['USD', 'CAD', 'EUR', 'GBP'])
    cache.persist_to_cache('tickers', pd.read_csv('tickers.csv')['Symbol'].drop_duplicates().values.tolist())
    cache.persist_to_cache('exchange_codes', ['L', 'N', 'OQ', 'SI', 'AL', 'VI', 'BB', 'BM', 'BR', 'BG', 'TC', 'TO', 'HK', 'SS',
                                    'FR', 'BE', 'DE', 'JA', 'DE', 'IL', 'VX', 'MFM', 'PA', 'ME', 'NZ'])
    cache.persist_to_cache('cois', ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP'])

def get_file_name(domain_object_config, output_formatter_config, file_no):
    config_file_name = domain_object_config['file_name']
    output_directory = domain_object_config['output_directory']
    file_extension = output_formatter_config['file_extension']
    output_file_name = config_file_name + '_{0}' + file_extension + '.gz'
    output_file_name = output_file_name.format(f'{file_no:03}')

    return output_file_name

def setup_file_output(file_extension, domain_obj_dict, file_name, output_directory):
    OutputDataAssembler.create_output_file(file_name) 
    if (file_extension == ".csv"): 
        OutputDataAssembler.write_csv_header(domain_obj_dict, file_name, output_directory)

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def main():
    cache = Cache()
    args = get_args()  
    initialise_cache(cache)
    
    with open(args.config) as config_file:
        config = json.load(config_file)

    domain_objects = config['domain_objects']
    file_builders = config['file_builders']
    output_formatters = config['output_formatters']
    shared_domain_obj_args = config['shared_domain_object_args']
    assigned_RAM_MB = float(config['assigned_RAM_MB'])

    for domain_object_config in domain_objects:                  
        max_objects_per_file = int(domain_object_config['max_objects_per_file'])
        num_records =  int(domain_object_config['record_count'])

        if ( num_records == 0 ): continue

        output_formatter_config = get_output_formatter_config(output_formatters, domain_object_config['file_builder_name'])
        output_formatter = get_output_formatter(output_formatter_config)

        file_name = domain_object_config['file_name']
        output_directory = domain_object_config['output_directory']
        file_extension = output_formatter_config['file_extension']

        print(file_name)
        records_returned_as_list = str_to_bool(domain_object_config['returns_list'])
        print("Records returned as list: ", records_returned_as_list)

        sample_record = OutputDataAssembler.process_domain_object(domain_object_config, cache, 0)
        if (records_returned_as_list == True): # This needs tidying
            sample_record = sample_record[0]

        storage_used_for_single_record = OutputDataAssembler.get_predicted_mem_for_single_record(sample_record, output_formatter)
        
        remaining_num_records = num_records
        file_no = 1
        remainder = 0
        domain_obj_id = 1
        while (True):# Loop to cover all files for a single domain object 
            file_name = get_file_name(domain_object_config, output_formatter_config, file_no) 
            setup_file_output(file_extension, sample_record, file_name, output_directory)
            
            if (remaining_num_records > max_objects_per_file):
                remainder = remaining_num_records - max_objects_per_file
                remaining_num_records = max_objects_per_file
                
            while (True): # Loop for each individual file of a single domain object
                start_time = time.time()
                print("Remaining num records: ", remaining_num_records, "/", num_records)
                curr_batch, remaining_num_records, domain_obj_id = OutputDataAssembler.fill_batch(cache, output_formatter, assigned_RAM_MB, remaining_num_records, storage_used_for_single_record, domain_object_config, domain_obj_id, records_returned_as_list)
                Compressor.compress(curr_batch, file_name, output_directory)
                end_time = time.time()
                time_elapsed = end_time - start_time
                print("Time to write batch: ", time_elapsed)
                curr_batch.clear()
                if remaining_num_records == 0: break
            
            storage_used_for_file = MemUtil.get_file_size_MB(file_name) 
            print("Storage used for current file: ", storage_used_for_file , "MB")
            
            remaining_num_records = remainder
            remainder = 0
            if (remaining_num_records == 0): break
            file_no += 1
            
        print()

    print("Process Complete")

if __name__ == '__main__':   
    main()