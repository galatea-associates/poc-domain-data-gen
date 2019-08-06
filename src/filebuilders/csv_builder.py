from filebuilders.file_builder import FileBuilder
import csv
import os

class CSVBuilder(FileBuilder):

    def build(self, file_extension, file_number, data, domain_object):                      
        file_name = domain_object['file_name'] + '_{}' + file_extension
        output_dir = domain_object['output_directory']

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name.format(f'{file_number:03}')), 'w+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=data[0].keys(), delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(data)