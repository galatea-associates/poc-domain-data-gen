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
            # TODO: remove redundant list in multi processing workflow
            #  before 'data' parameter is passed to build(), then remove
            #  workaround below
            fieldnames = data[0].keys()  # get keys from first dict
            dict_writer = csv.DictWriter(output_file, restval="-",
                                         fieldnames=fieldnames,
                                         delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(data)

        if self.google_drive_connector_exists():
            self.upload_to_google_drive(output_dir, file_name)
