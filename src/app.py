import importlib
import ujson
import os
from argparse import ArgumentParser
from utils.sqlite_database import Sqlite_Database
from multi_processing.coordinator import Coordinator
import multi_processing.batch_size_calc as batch_size_calc


def main():
    # Delete db if one already exists
    if os.path.exists('dependencies.db'):
        os.unlink('dependencies.db')

    args = get_args()

    # Open and retrieve configurations
    with open(args.config) as config_file:
        config = ujson.load(config_file)
    domain_object_configs = config['domain_objects']
    file_builder_configs = config['file_builders']
    shared_config = config['shared_args']

    for obj_config in domain_object_configs:
        # Skip object where no records required
        if (int(obj_config['record_count']) < 1):
            continue
        file_builder = get_file_builder(obj_config, file_builder_configs)
        process_domain_object(obj_config, file_builder, shared_config)


def get_file_builder(obj_config, file_builder_configs):
    # Given an objects configuration and all file_builder descriptions,
    # return an instantiated file builder as per spec in object config
    fb_name = obj_config['file_builder_name']
    fb_config = get_fb_config(file_builder_configs, fb_name)
    file_builder = get_class('filebuilders', fb_config['module_name'],
                             fb_config['class_name'])
    return file_builder(None, obj_config)


def process_domain_object(obj_config, file_builder, shared_config):
    # Starts both data generating & file writing processes & populates the job
    # queue of the coordinator to get both processes underway. Post population
    # of jobs, awaits both generator and writer to terminate before continuing

    obj_class = get_class('domainobjects', obj_config['module_name'],
                          obj_config['class_name'])
    domain_obj = obj_class(file_builder, obj_config)
    custom_args = obj_config['custom_args']

    coordinator = Coordinator(obj_config['max_objects_per_file'], file_builder)

    default_job_size = shared_config['job_size']
    generator_pool_size = shared_config['gen_pools']
    writer_pool_size = shared_config['write_pools']

    # Start generation & writing subprocesses for this object
    coordinator.start_generator(domain_obj, custom_args, generator_pool_size)
    coordinator.start_writer(writer_pool_size)

    obj_name = obj_config['class_name']
    record_count = get_record_count(obj_config)
    job_size = batch_size_calc.get(obj_name, custom_args, default_job_size)

    coordinator.create_jobs(obj_name, record_count, job_size)
    coordinator.await_termination()


def get_record_count(obj_config):
    # Get number of records required to generate OR the size of an objects
    # dependency table from the DB, used to create jobs in queue
    nondeterministic_objects = ['swap_contract', 'swap_position', 'cashflow']
    object_module = obj_config['module_name']

    if object_module not in nondeterministic_objects:
        return obj_config['record_count']
    else:
        db = Sqlite_Database()
        if object_module == 'swap_contract':
            return db.get_table_size('counterparties')
        elif object_module == 'swap_position':
            return db.get_table_size('swap_contracts')
        elif object_module == 'cashflow':
            return db.get_table_size('swap_positions')


def get_args():
    # Configure expected command line args & default values thereof
    parser = ArgumentParser(description='''Random financial data
                                        generation. For more information,
                                        see the README''')
    parser.add_argument('--config', default='src/config.json',
                        help='JSON Configuration File Location')
    return parser.parse_args()


def get_fb_config(file_builders, file_extension):
    # Get file_builder configuration for a given file extension
    return list(filter(
            lambda file_builder: file_builder['name'] == file_extension,
            file_builders))[0]


def get_class(package_name, module_name, class_name):
    # Return a specified class in given package/module heirarchy
    return getattr(importlib.import_module(package_name+'.'+module_name),
                   class_name)


if __name__ == '__main__':
    main()
