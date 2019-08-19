from filebuilders.file_builder import FileBuilder
import ujson
import os

class JSONBuilder(FileBuilder):

    def build(self, file_number, data):                       
        output_dir = self.get_output_directory()
        file_name = self.get_file_name() 

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name.format(f'{file_number:03}')), 'w') as output_file:
            ujson.dump(data, output_file, default=str)
        
    def append_data(self, data):        
        self.file.write(ujson.dumps(data, default=str) + ',')