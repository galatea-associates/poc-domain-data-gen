from filebuilders.file_builder import FileBuilder
import csv
import os
import dicttoxml
import logging

class XMLBuilder(FileBuilder):
    """ A class to generate an XML file from records. Uses the dicttoxml
    library to achieve this. """

    def build(self, file_number, data, upload_to_google_drive=False):
        output_dir = self.get_output_directory()
        file_name = self.get_file_name()
        root_element_name = self.get_root_element_name()

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir,
                  file_name.format(f'{file_number:03}')),
                  'w', newline='') as output_file:

            # convert data to bytes
            xml = dicttoxml.dicttoxml(
                data, custom_root=root_element_name, 
                ids=False, item_func=item_function
            )

            # convert from bytes into string
            xml = str(xml, 'utf-8')
            xml = xml.replace(' type=\"str\"', '')\
                .replace(' type=\"dict\"', '')\
                .replace(' type=\"int\"', '')
            output_file.write(xml)

    def item_function(self):
        return self.get_item_name()