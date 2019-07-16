from filebuilders.file_builder import FileBuilder
from json.encoder import JSONEncoder
import jsonlines
import os

class JSONLBuilder(FileBuilder):

    def build(self, output_dir, file_name, file_extension, data, max_objects_per_file, root_element_name):
        file_name = file_name + '_{0}' + file_extension

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        start = 0
        max_objects_per_file = int(max_objects_per_file)
        file_count = max(int(len(data) / max_objects_per_file), 1)

        encoder = JSONEncoder(default=str)
        for i in range(0, file_count):
            current_slice = data[start : start + max_objects_per_file]
            with jsonlines.open(os.path.join(output_dir, file_name.format(f'{i+1:03}')), mode='w', dumps=encoder.encode) as output_file:                
                output_file.write_all(current_slice)
            
            start += max_objects_per_file
        