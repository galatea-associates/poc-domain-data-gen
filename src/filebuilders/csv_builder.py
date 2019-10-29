from filebuilders.file_builder import FileBuilder
import csv
import os

class CSVBuilder(FileBuilder):

    def build(self, file_extension, data, domain_object_config):                      
        file_name = domain_object_config['file_name'] + '_{0}' + file_extension
        output_dir = domain_object_config['output_directory']

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        start = 0
        max_objects_per_file = int(domain_object_config['max_objects_per_file'])
        file_count = max(int(len(data) / max_objects_per_file), 1)
        upload_to_google_drive = domain_object_config['upload_to_google_drive']

        for i in range(0, file_count):
            current_slice = data[start : start + max_objects_per_file]
            file_name = file_name.format(f'{i+1:03}')
            with open(os.path.join(output_dir, file_name), 'w+', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=data[0].keys(), delimiter=',')
                dict_writer.writeheader()
                dict_writer.writerows(current_slice)

            if upload_to_google_drive.upper() == 'TRUE':
                self.upload_to_google_drive(output_dir, file_name)
            
            start += max_objects_per_file
