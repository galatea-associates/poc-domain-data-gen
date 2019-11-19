default_gen_arguments = [
    {
        'instrument': {
            'max_objects_per_file': 50,
            'file_name': 'instruments',
            'output_file_type': 'CSV',
            'output_directory': 'out',
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

default_domain_objects = [
    {
        'instrument': {
            'module_name': 'instrument',
            'class_name': 'Instrument'
        }
    }
]
default_shared_arguments = {
    'generator_pool_size': 1,
    'writer_pool_size': 1,
    'pool_job_size': 10000
}

default_file_builders = [
    {
        'CSV': {
            'module_name': 'csv_builder',
            'class_name': 'CSVBuilder',
            'file_extension': '.csv'
        }
    }
]
