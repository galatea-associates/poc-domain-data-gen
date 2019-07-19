from filebuilders.file_builder import FileBuilder
from json.encoder import JSONEncoder
import jsonlines
import os

class JSONLBuilder(FileBuilder):

    def build(self, file_extension, data, domain_object):                       
        file_name = domain_object['file_name'] + '_{0}' + file_extension
        output_dir = domain_object['output_directory']

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        start = 0
        max_objects_per_file = int(domain_object['max_objects_per_file'])
        file_count = max(int(len(data) / max_objects_per_file), 1)
        upload_to_google_drive = domain_object['upload_to_google_drive']

        encoder = JSONEncoder(default=str)
        for i in range(0, file_count):
            current_slice = data[start : start + max_objects_per_file]
            file_name = file_name.format(f'{i+1:03}')
            with jsonlines.open(os.path.join(output_dir, file_name), mode='w', dumps=encoder.encode) as output_file:                
                output_file.write_all(current_slice)

            if upload_to_google_drive.upper() == 'TRUE':
                self.upload_to_google_drive(output_dir, file_name)
            
            start += max_objects_per_file
        