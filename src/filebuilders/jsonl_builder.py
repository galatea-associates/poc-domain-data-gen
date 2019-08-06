from filebuilders.file_builder import FileBuilder
from json.encoder import JSONEncoder
import jsonlines
import os

class JSONLBuilder(FileBuilder):

    def build(self, file_extension, file_number, data, domain_object):                   
        file_name = domain_object['file_name']+'_{}'+file_extension
        output_dir = domain_object['output_directory']
        if not os.path.exists(output_dir): 
            os.mkdir(output_dir)

        encoder = JSONEncoder(default = str)
        with jsonlines.open(os.path.join(output_dir, file_name.format(f'{file_number:03}')), mode='w', dumps=encoder.encode) as output_file:
            output_file.write_all(data)