default_factory_definitions = [
    {
        'instrument': {
            'max_objects_per_file': 50,
            'file_name': 'instruments',
            'output_file_type': 'CSV',
            'output_directory': 'out',
            'upload_to_google_drive': 'false',
            'generation_type': 'fixed',
            'fixed_args': {
                'record_count': 50
            },
            'dummy_fields': [
                {
                    'data_type': 'string',
                    'data_length': 10,
                    'field_count': 10
                },
                {
                    'data_type': 'numeric',
                    'data_length': 10,
                    'field_count': 10
                }
            ],
            'file_type_args': {
                'xml_root_element': 'instruments',
                'xml_item_name': 'instrument'
            }
        }
    }
]

default_dev_factory_args = [
    {
        'instrument': {
            'module_name': 'instrument',
            'class_name': 'Instrument'
        }
    }
]
default_shared_args = {
    'number_of_create_child_processes': 1,
    'number_of_write_child_processes': 1,
    'number_of_records_per_job': 25
}

default_dev_file_builder_args = [
    {
        'CSV': {
            'module_name': 'csv_builder',
            'class_name': 'CSVBuilder',
            'file_extension': '.csv'
        }
    }
]
