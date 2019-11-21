from filebuilders.file_builder import FileBuilder
import ujson
import os


class JSONBuilder(FileBuilder):
    """ A class to generate a JSON file from records. Uses ujson to process
    each dictionary into JSON. """

    def build(self, file_number, data):
        output_dir = self.get_output_directory()
        file_name = self.get_file_name().format(f'{file_number:03}')

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name), 'w') as output_file:
            ujson.dump(data, output_file)

        if self.google_drive_connector_exists():
            self.upload_to_google_drive(output_dir, file_name)

    def append_data(self, data):
        self.file.write(ujson.dumps(data) + ',')
