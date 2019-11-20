from filebuilders.file_builder import FileBuilder
import csv
import os


class CSVBuilder(FileBuilder):
    """ A class to generate a CSV file from records. Uses the csv library to
    achieve this. """

    def build(self, file_number, data):
        output_dir = self.get_output_directory()
        file_name = self.get_file_name().format(f'{file_number:03}')

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, file_name),
                  'w+', newline='') as output_file:

            fieldnames = data[0][0].keys()  # get keys from first dict
            data = data[0]  # remove redundant outer list
            dict_writer = csv.DictWriter(output_file, restval="-",
                                         fieldnames=fieldnames,
                                         delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(data)

        if self.get_google_drive_flag():
            self.upload_to_google_drive(output_dir, file_name)
