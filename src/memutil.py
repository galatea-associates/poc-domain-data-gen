import psutil
import os
import sys

class MemUtil(object):

    @classmethod
    def get_file_size_MB(cls, file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return cls.convert_bytes_to_MB(file_info.st_size)

    @classmethod
    def get_process_memory_MB(cls):
        process = psutil.Process(os.getpid())
        process_mem_bytes = process.memory_info().rss
        process_mem_MB = cls.convert_bytes_to_MB(process_mem_bytes)
        return process_mem_MB
    
    @staticmethod
    def convert_bytes_to_MB(num):
        return num/1000000
    
    @staticmethod
    def get_object_size(obj):
        return sys.getsizeof(obj)