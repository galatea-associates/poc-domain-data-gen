from filebuilders.file_builder import FileBuilder
import os
import dicttoxml


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
            item_func = self.get_item_func()
            xml = dicttoxml.dicttoxml(
                data, custom_root=root_element_name,
                ids=False, item_func=item_func
            )

            # convert from bytes into string
            xml = str(xml, 'utf-8')
            xml = xml.replace(' type=\"str\"', '')\
                .replace(' type=\"dict\"', '')\
                .replace(' type=\"int\"', '')
            output_file.write(xml)

    def get_item_func(self):
        """ This is a helper method to create a compatible argument for the
        dicttoxml.dicttoxml method's item_func parameter. This parameter
        expects a callable that takes one parameter (the xml root element name)
        and returns the item name for each XML block nested under that root.
        The callable can only take 1 parameter, but a reference to 'self' is
        needed to retrieve the item name, so this wrapper function is used to
        overcome this."""

        item_name = self.get_item_name()

        def item_func(_):
            """ This function can access the item_name from the local scope
            of the surrounding function, which overcomes the issue of returning
            the item_name without taking in 'self' as a parameter.
            Note the parameter is not used, but provided to comply with the
            calling module"""
            return item_name

        return item_func
