from filebuilders.file_builder import FileBuilder
import csv
import os

class CSVBuilder(FileBuilder):

    def build(self, file_number, data):
        output_dir = self.get_output_directory()
        file_name = self.get_file_name()

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name.format(f'{file_number:03}')),
                 'w+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=data[0].keys(), delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(data)