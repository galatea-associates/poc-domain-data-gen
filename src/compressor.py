import io
import gzip
from memutil import MemUtil

class Compressor(object):

    @classmethod
    def compress_batch(cls, batch, file_name, output_directory):
        '''
        This is the most memory intenstive part of the compression operation,
        as the RAM usage is doubled for a short period, while the list of 
        strings is concatenated into a single string 
        '''
        print("Pre-concatenation process memory: ", MemUtil.get_process_memory_MB(), " MB")  
        concatenated_records = "".join(batch)
        print("Post-concatenation process memory: ", MemUtil.get_process_memory_MB(), " MB")  

        batch.clear() # Garbage Collection
        del batch

        print("Pre-compression process memory: ", MemUtil.get_process_memory_MB(), " MB")
        cls.__compression(concatenated_records, file_name, output_directory)
        concatenated_records = "" # Garbage Collection
        del concatenated_records
        print("Post compression process memory: ", MemUtil.get_process_memory_MB(), " MB")
        
        return MemUtil.get_file_size_MB(file_name)

    @staticmethod
    def __compression(concatenated_records, file_name, output_directory):
        open_file = gzip.open(file_name, 'a')
        f = io.BufferedWriter(open_file)
        try:
            f.write(str(concatenated_records).encode('utf-8'))
        finally:
            f.close()
