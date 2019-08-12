from filebuilders.file_builder import FileBuilder
import json
import os

class JSONLBuilder(FileBuilder):

    def build(self, file_extension, file_number, data, domain_object):                   
        file_name = domain_object['file_name']+'_{}'+file_extension
        output_dir = domain_object['output_directory']
        if not os.path.exists(output_dir): 
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name.format(f'{file_number:03}')), 'w') as output_file:
            to_output = [json.dumps(record, default=str) for record in data]
            formatted_output = "\n".join(to_output)
            output_file.write(formatted_output)