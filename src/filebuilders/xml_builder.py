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
                ids=False, item_func=XMLBuilder.get_item_name
            )

            # convert from bytes into string
            xml = str(xml, 'utf-8')
            xml = xml.replace(' type=\"str\"', '')\
                .replace(' type=\"dict\"', '')\
                .replace(' type=\"int\"', '')
            output_file.write(xml)

    @staticmethod
    def get_item_name(parent_element_name):
        item_names = {
            "instruments": "instrument",
            "prices": "price",
            "counterparties": "counterparty",
            "back_office_positions": "back_office_position",
            "front_office_positions": "front_office_position",
            "depot_positions": "depot_position",
            "cash_balances": "cash_balance",
            "order_executions": "order_execution",
            "stock_loan_positions": "stock_loan_position",
            "swap_contracts": "swap_contract",
            "swap_positions": "swap_position",
            "cashflows": "cashflow"
        }
        item_name = item_names[parent_element_name]
        return item_name
