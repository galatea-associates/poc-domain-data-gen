import argparse
import importlib
import ujson
import timeit
import logging
import random
from cache import Cache
from sqlite_database import Sqlite_Database
# from GoogleDriveAccessor import GoogleDriveAccessor


# Return a specified class from package.module
def get_class(package_name, module_name, class_name):
    return getattr(importlib.import_module(package_name+'.'+module_name),
           class_name)

# Create list comprehension of the file builder config which matches a name
def get_file_builder_config(file_builders, file_builder_name):
    return list(filter(
            lambda file_builder: file_builder['name'] == file_builder_name,
            file_builders
            ))[0]

# Facillitate the domain object generation procedure
def process_domain_object(domain_obj_config, cache,
                          dependency_db, file_builder):

    domain_obj_class = get_class('domainobjects',
                                 domain_obj_config['module_name'],
                                 domain_obj_config['class_name'])

    domain_obj = domain_obj_class(cache, dependency_db, file_builder,
                                  domain_obj_config)

    record_count = int(domain_obj_config['record_count'])
    custom_args = domain_obj_config['custom_args']
    domain_obj.generate(record_count, custom_args)

# Configure a parser for command line argument retrieval, and retrieve arguments
def get_args():
    parser = argparse.ArgumentParser(description='''Generate Random Data for
                                      various Domain Objects''')
    parser.add_argument('--config', default='src/config.json',
                        help='JSON Config File Location')
    cl_args = parser.parse_args()
    return cl_args

def main():

    # TODO: Random seeding for consistency in tests, REMOVE THIS IN RELEASES
    # random.seed(100)

    start_time = timeit.default_timer()
    logging.basicConfig(filename='generator.log', filemode='w',
                        format='%(levelname)s : %(message)s',
                        level=logging.INFO)

    cache = Cache()                     # Store global generation attributes
    dependency_db = Sqlite_Database()   # Store global generation dependencies
    args = get_args()                   # Stores command line arguments
    # google_drive_accessor = GoogleDriveAccessor(args.g_drive_root)

    with open(args.config) as config_file:
        config = ujson.load(config_file)

    domain_object_configs = config['domain_objects']
    file_builder_configs = config['file_builders']

    for domain_object_config in domain_object_configs:

        logging.info("Now Generating Domain Object: "
                     + domain_object_config['class_name'])

        gen_start_time = timeit.default_timer()

        file_builder_name = domain_object_config['file_builder_name']
        file_builder_config = get_file_builder_config(file_builder_configs, 
                                                      file_builder_name)

        file_builder_class =\
            get_class('filebuilders', file_builder_config['module_name'],
                      file_builder_config['class_name'])

        file_builder = file_builder_class(None, domain_object_config)

        process_domain_object(domain_object_config, cache,
                              dependency_db, file_builder)

        gen_end_time = timeit.default_timer()
        logging.info("Domain Object: " + domain_object_config['class_name']
                     + " took " + str(gen_end_time-gen_start_time)
                     + " seconds to generate.")

    end_time = timeit.default_timer()
    logging.info("Overall runtime: "+str(end_time-start_time))

if __name__ == '__main__':   
    main()