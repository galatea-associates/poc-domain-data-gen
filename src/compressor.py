import io
import os
import gzip
import psutil
import snappy

class Compressor:

    def compress_partition(self, partition, file_name, output_directory):
        '''
        This is the most memory intenstive part of the compression operation,
        as the RAM usage is doubled for a short period, while the list of 
        strings is concatenated into a single string 
        '''
        print("Pre-concatenation process memory: ", self.__get_process_memory(), " MB")  
        concatenated_records = "".join(partition)
        print("Post-concatenation process memory: ", self.__get_process_memory(), " MB")  

        partition.clear() # Garbage Collection
        del partition

        print("Pre-compression process memory: ", self.__get_process_memory(), " MB")
        self.__compression(concatenated_records, file_name, output_directory)
        concatenated_records = "" # Garbage Collection
        del concatenated_records
        print("Post compression process memory: ", self.__get_process_memory(), " MB")
        
        return self.__file_size(file_name)

    def __compression(self, concatenated_records, file_name, output_directory):
        open_file = gzip.open(file_name, 'a')
        f = io.BufferedWriter(open_file)
        try:
            f.write(str(concatenated_records).encode('utf-8'))
        finally:
            f.close()

    def __convert_bytes(self, num):
        return num/1000000

    def __file_size(self, file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return self.__convert_bytes(file_info.st_size)

    def __get_process_memory(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss/1000000 # MB