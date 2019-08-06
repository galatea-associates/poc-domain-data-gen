from filebuilders.file_builder import FileBuilder
import csv
import os
import dicttoxml
from xml.dom.minidom import parseString

class XMLBuilder(FileBuilder):

    def build(self, file_extension, file_number, data, domain_object):                       
        file_name = domain_object['file_name'] + '_{}' + file_extension
        output_dir = domain_object['output_directory']              
        root_element_name = domain_object['root_element_name']              

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        item_name_func = lambda x: domain_object['item_name']

        with open(os.path.join(output_dir, file_name.format(f'{file_number:03}')), 'w', newline='') as output_file:                               
            xml = dicttoxml.dicttoxml(data, custom_root=root_element_name, item_func=item_name_func, ids=False) # Outputs to Bytes
            xml = str(xml, 'utf-8') # Bytes to String
            xml = xml.replace(' type=\"str\"', '').replace(' type=\"dict\"', '').replace(' type=\"int\"', '')
            output_file.write(xml)