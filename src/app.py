import argparse
import importlib
import json
import os
import logging
import pandas as pd
from cache import Cache
import gzip
import psutil
from output_data_assembler import OutputDataAssembler
import io
import csv
import sys

def process_domain_object(domain_obj_config, cache, domain_obj_id):
    domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
    domain_obj = domain_obj_class(cache)
    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    return domain_obj.generate(custom_args, domain_obj_id)

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

def main():
    cache = Cache()
    output_data_assembler = OutputDataAssembler()
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

        #domain_obj_result = process_domain_object(domain_object_config, cache)
        domain_obj_result = []
        curr_process_mem = get_process_memory()
        if (curr_process_mem > assigned_RAM_MB):
            print("Warning, RAM allocated exceeded")

        #sample_record = domain_obj_result[0]
        sample_record = process_domain_object(domain_object_config, cache, 0)
        storage_used_for_single_record = output_data_assembler.get_predicted_mem_usage(num_records, assigned_RAM_MB, sample_record, output_formatter, file_extension)
        
        remaining_num_records = num_records

        file_no = 1
        remainder = 0
        domain_obj_id = 1
        while (True): 
            output_file_name = setup_file_output(file_name, file_extension, file_no, output_directory, sample_record, output_data_assembler)
            print(output_file_name)
            if (remaining_num_records > max_objects_per_file):
                remainder = remaining_num_records - max_objects_per_file
                remaining_num_records = max_objects_per_file
                
            # Single file loop
            while (True):
                print("Remaining num records: ", remaining_num_records, "/", num_records)
                curr_partition, remaining_num_records, domain_obj_id = output_data_assembler.fill_partition(cache, output_formatter, assigned_RAM_MB, remaining_num_records, storage_used_for_single_record, domain_object_config, domain_obj_id)
                output_data_assembler.compress_partition(curr_partition, output_file_name, output_directory)
                curr_partition.clear()
                if remaining_num_records == 0: break
            
            storage_used_for_file = file_size(output_file_name) 
            print("Storage used for current file: ", storage_used_for_file , "MB")
            
            remaining_num_records = remainder
            remainder = 0
            print("domain_obj_id ", domain_obj_id)
            
            if (remaining_num_records == 0): break
            file_no = file_no + 1
            
        size_of_cache = __convert_bytes_to_MB(sys.getsizeof(cache))
        print("Size of cache: ", size_of_cache, "MB")
        print()

    print("Process Complete")

def setup_file_output(file_name, file_extension, file_no, output_directory, domain_obj_dict, output_data_assembler):
    output_file_name = file_name + '_{0}' + file_extension + '.gz'
    output_file_name = output_file_name.format(f'{file_no:03}')
    f = gzip.open(output_file_name, 'w').close()

    if (file_extension == ".csv"):
        write_header_csv(domain_obj_dict, output_file_name)

    return output_file_name

def write_header_csv(domain_obj_dict, output_file_name):
    output = io.StringIO()    
    dict_writer = csv.DictWriter(output, restval="-", fieldnames=domain_obj_dict.keys(), delimiter=',')
    dict_writer.writeheader()
    output.seek(0)
    output_string = output.read()
    open_file = gzip.open(output_file_name, 'a')
    f = io.BufferedWriter(open_file)
    try:
        f.write(str(output_string).encode('utf-8'))
    finally:
        f.close()

def get_process_memory():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss/1000000 # MB

def file_size(file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return __convert_bytes_to_MB(file_info.st_size)

def __convert_bytes_to_MB(num):
        return num/1000000

if __name__ == '__main__':   
    main()