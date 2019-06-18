from filebuilders.file_builder import FileBuilder
import json
import os

class JSONBuilder(FileBuilder):

    def build(self, output_dir, file_name, file_extension, data, objects_per_file):
        file_name = file_name + '_{0}' + file_extension

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        start = 0
        objects_per_file = int(objects_per_file)
        file_count = int(len(data) / objects_per_file)

        for i in range(0, file_count):
            current_slice = data[start : start + objects_per_file]
            with open(os.path.join(output_dir, file_name.format(f'{i+1:03}')), 'w', newline='') as output_file:
                json.dump(current_slice, output_file)
            
            start += objects_per_file
        