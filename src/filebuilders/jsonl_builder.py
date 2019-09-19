from filebuilders.file_builder import FileBuilder
import ujson
import os

class JSONLBuilder(FileBuilder):

    def build(self, file_number, data):
        output_dir = self.get_output_directory()
        file_name = self.get_file_name()

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        file_path = os.path.join(output_dir, file_name.format(f'{file_number:03}'))

        with open(file_path, 'w') as output_file:
            to_output = [ujson.dumps(record) for record in data]
            formatted_output = "\n".join(to_output)
            output_file.write(formatted_output)

        # TODO: REMOVE THIS LINE
        # Only here to save space requirements on AWS        
        os.unlink(file_path)
        print("File num",file_number)
