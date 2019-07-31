import io
import gzip
from memutil import MemUtil

class Compressor(object):

    @staticmethod
    def compress(concatenated_records, file_name, output_directory):
        print("Pre-compression process memory: ", MemUtil.get_process_memory_MB(), " MB")

        open_file = gzip.open(file_name, 'a')
        f = io.BufferedWriter(open_file)
        try:
            for record in concatenated_records:
                #f.write(str(record +'\n').encode('utf-8'))
                f.write(str(record).encode('utf-8'))
        finally:
            f.close()
            
        print("Post compression process memory: ", MemUtil.get_process_memory_MB(), " MB")
