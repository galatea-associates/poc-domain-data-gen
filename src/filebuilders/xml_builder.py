from filebuilders.file_builder import FileBuilder
import csv
import os
import dicttoxml
from xml.dom.minidom import parseString

class XMLBuilder(FileBuilder):

    def build(self, output_dir, file_name, file_extension, data, objects_per_file):
        file_name = file_name + '_{0}' + file_extension

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        start = 0
        objects_per_file = int(objects_per_file)
        file_count = int(len(data) / objects_per_file)

        for i in range(0, file_count):
            current_slice = data[start : start + objects_per_file]
            with open(os.path.join(output_dir, file_name.format(f'{i+1:03}')), 'w', newline='') as output_file:     

                # Remove '*' from the key names
                new_list = []
                for individual_dict in current_slice:
                    new_dict = {}
                    for k,v in individual_dict.items():
                        new_key = k.strip('*')
                        new_dict.update({new_key : v})
                    new_list.append(new_dict)
                
                xml = dicttoxml.dicttoxml(new_list, custom_root='root', item_func=my_item_func, ids=False) # Outputs to Bytes
                xml = str(xml, 'utf-8') # Bytes to String
                xml = xml.replace(' type=\"str\"', '').replace(' type=\"dict\"', '').replace(' type=\"int\"', '')
                output_file.write(xml)

            start += objects_per_file


def my_item_func(value):
        return 'list_item'