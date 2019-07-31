import sys
import math
import gzip
import psutil
import importlib
import csv
import io
import random
from memutil import MemUtil
from compressor import Compressor

class DataAssembler(object):

    @staticmethod
    def process_domain_object(domain_obj_config, cache, domain_obj_id):
        domain_obj_class = getattr(importlib.import_module('domainobjects.' + domain_obj_config['module_name']), domain_obj_config['class_name'])
        domain_obj = domain_obj_class(cache)
        record_count = int(domain_obj_config['record_count'])
        custom_args = domain_obj_config['custom_args']
        return domain_obj.generate(custom_args, domain_obj_id)

    @staticmethod
    def get_predicted_mem_for_single_record(domain_obj_sample, output_formatter):
        '''
        Method used to obtain an estimate for the size of the output file (uncompressed), 
        in order to select the optimum number of batches for compression so that the 
        allocated RAM is not exceeded
        '''
        output_string = output_formatter.format(domain_obj_sample)
        size_of_object = MemUtil.get_object_size(output_string) 
        return MemUtil.convert_bytes_to_MB(size_of_object)

    @staticmethod
    def create_output_file(file_name):
        '''
        Create the file based upon the number of batches and the number of objects per file
        '''
        f = gzip.open(file_name, 'w').close() # Overwrite previous existing file of same name

    @classmethod
    def fill_batch(cls, cache, output_formatter, assigned_RAM_MB, num_records, single_record_mem, domain_obj_config, domain_obj_id, returns_list_of_records):
        curr_batch = []
        remaining_num_records = 0
        pre_batch_filled_RAM = MemUtil.get_process_memory_MB()
        list_of_dicts = cls.process_domain_object(domain_obj_config, cache, domain_obj_id) # Unused if returns only single record

        for curr_record in range(num_records):
            if (returns_list_of_records == True):
                domain_obj_dict = list_of_dicts[curr_record]
            else:
                domain_obj_dict = cls.process_domain_object(domain_obj_config, cache, domain_obj_id)
            domain_obj_id += 1

            record = output_formatter.format(domain_obj_dict)
            curr_batch.append(record) 
            batch_size = len(curr_batch)

            if (cls.__check_batch_size(batch_size, curr_record, assigned_RAM_MB, num_records, single_record_mem, remaining_num_records) == True):
                remaining_num_records = num_records - (curr_record+1) 

            if (remaining_num_records != 0):
                break # Remaining num records only changes when the memory allocated is expected to be exceeded within the next 1000 records generated 

        return curr_batch, remaining_num_records, domain_obj_id


    @classmethod
    def __check_batch_size(cls, batch_size, curr_record, assigned_RAM_MB, num_records, single_record_mem, remaining_num_records):
        if (batch_size % 1000 == 0):
                process_mem = MemUtil.get_process_memory_MB()
                predicted_RAM = single_record_mem * 1005 # 5 gives 5 files worth of tolerance with the randomly fluctiations in bits of data 
                toleranced_mem = predicted_RAM + process_mem

                if cls.__is_toleranced_mem_excessive(toleranced_mem, assigned_RAM_MB) == True:
                    remaining_num_records = num_records - (curr_record+1)

        return remaining_num_records        
                    
    @staticmethod
    def __is_toleranced_mem_excessive(toleranced_mem, assigned_RAM_MB):
        if (toleranced_mem > assigned_RAM_MB):
            return True
        else: 
            return False
        
    @staticmethod
    def write_csv_header(domain_obj_dict, file_name, output_directory):
        output = io.StringIO()    
        dict_writer = csv.DictWriter(output, restval="-", fieldnames=domain_obj_dict.keys(), delimiter=',')
        dict_writer.writeheader()
        output.seek(0)
        output_string = output.read()
        Compressor.compress(output_string, file_name, output_directory)






