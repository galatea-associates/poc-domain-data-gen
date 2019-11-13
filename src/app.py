""" Random Data Generator for Financial-Domain Objects

    Based on a user provided configuration, generate a set of random data
    pertaining to said configuration. Currently supported domain objects are:

        * Back Office Position
        * Cash Balance
        * Cashflow
        * Counterparty
        * Depot Positions
        * Front Office Position
        * Instrument
        * Order Execution
        * Price
        * Stock Loan Position
        * Swap Contract
        * Swap Position

    Each domain object to be generated (record count > 0) is generated in
    turn to account for inter-object dependencies. Generation is
    multiprocessed with a primary coordinator spawning two child process
    coordinators. One of these children handles object generation, and the
    second writing of these to file.

    The generation coordinator recieved instruction to generate X number of
    objects over Y number of subprocesses (Pool Size). Once these jobs are
    executed and records returned, they are placed into a writing job queue.
    The writing to file coordinator picks up & formats these tasks before
    assigning them to execute on a second pool

"""

import importlib
import ujson
import os
from argparse import ArgumentParser
from database.sqlite_database import Sqlite_Database
from multi_processing.coordinator import Coordinator
from exceptions.config_error import ConfigError
import multi_processing.batch_size_calc as batch_size_calc
import validator.config_validator as config_validator


def main():
    # Delete database if one already exists
    if os.path.exists('dependencies.db'):
        os.unlink('dependencies.db')

    configurations = parse_config_files()
    # validate_configs(configurations)

    for generation_arguments in configurations['generation_arguments']:

        shared_config = configurations['shared_arguments']
        file_builders = configurations['file_builders']
        obj_locations = configurations['domain_object_locations']

        obj_name = list(generation_arguments.keys())[0]
        gen_args = generation_arguments[obj_name]
        file_builder = get_file_builder(gen_args, file_builders)
        obj_location = get_object_location(obj_name, obj_locations)

        process_domain_object(gen_args, obj_location,
                              file_builder, shared_config)


def get_object_location(obj_name, obj_locations):
    obj_locations = obj_locations[0]
    return obj_locations[obj_name]


def get_file_builder(obj_config, file_builder_configs):
    """ Retrieves file builder object from provided configs

        Parameters
        ----------
        obj_config : dict
            A domain objects configuration as provided by user
        file_builder_configs: dict
            All possible file builder configurations

        Returns
        -------
        File_Builder
            Instantiated file builder as defined by the file builder
            configurations, as per the user specified output type of
            the given object configuration
    """

    fb_name = obj_config['output_file_type']
    fb_config = get_fb_config(file_builder_configs, fb_name)
    file_builder = get_class('filebuilders', fb_config['module_name'],
                             fb_config['class_name'])
    print(obj_config)
    return file_builder(None, obj_config)


def process_domain_object(obj_config, obj_location,
                          file_builder, shared_config):
    """ Instantiates generation and file-writing processes. Populates the
    generation job queue & starts both generation and writing coordinators.
    Awaits for both coordinators to terminate before continuing to the next
    domain object, or finishing execution.

    Parameters
    ----------
    obj_config : dict
        A domain objects configuration as provided by user
    file_builder : File_Builder
        An instantiated filebuilder as per this objects required output
        file type
    shared_config : dict
        User-provided configuration shared between all objects
    """

    obj_class = get_class('domainobjects', obj_location['module_name'],
                          obj_location['class_name'])
    domain_obj = obj_class(obj_config)

    coordinator = Coordinator(obj_config['max_objects_per_file'], file_builder)

    default_job_size = shared_config['pool_job_size']
    generator_pool_size = shared_config['generator_pool_size']
    writer_pool_size = shared_config['writer_pool_size']

    # Start generation & writing subprocesses for this object
    coordinator.start_generator(domain_obj, generator_pool_size)
    coordinator.start_writer(writer_pool_size)

    obj_name = obj_location['class_name']
    record_count = get_record_count(obj_config, obj_location)
    job_size = batch_size_calc.get(obj_name, default_job_size)

    coordinator.create_jobs(obj_name, record_count, job_size)
    coordinator.await_termination()


def get_record_count(obj_config, obj_location):
    """ Returns the number of records to be generated for a given object.
    Where objects are non-dependent on others, the user-provided configuration
    amount is used. Otherwise, the record_count is set to be the number of
    records generated of the domain object the to-generate one is dependent
    on.

    Parameters
    ----------
    obj_config : dict
        A domain objects configuration as provided by user

    Returns
    -------
    int
        Number of records to generate, or the number of dependent objects
        generated prior where cur object non-deterministic amount to generate
    """

    nondeterministic_objects = ['swap_contract', 'swap_position', 'cashflow']
    object_module = obj_location['module_name']

    if object_module not in nondeterministic_objects:
        return obj_config['fixed_args']['record_count']
    else:
        db = Sqlite_Database()
        if object_module == 'swap_contract':
            return db.get_table_size('counterparties')
        elif object_module == 'swap_position':
            return db.get_table_size('swap_contracts')
        elif object_module == 'cashflow':
            return db.get_table_size('swap_positions')


def get_fb_config(file_builders, file_extension):
    """ Get the configuration of a specified filebuilder. Iterate over the
    set of file builder keys and if one matches the provided file extension
    then return the full configuration of that file builder.

    Parameters
    ----------
    file_builders : dict
        Parsed json of provided configuration containing parameters for
        all possible filebuilders.
    file_extension: string
        The extension of the file builder configuration which should be
        returned

    Returns
    -------
    dict
        The configuration of the required file builder for the output
        type required.
    """
    file_builder_dict = file_builders[0]
    file_builder_dict_keys = file_builder_dict.keys()

    for file_builder in list(file_builder_dict_keys):
        if file_builder == file_extension:
            return file_builder_dict[file_builder]
    # TODO: Raise error if no file builder found for given configuration


def get_class(package_name, module_name, class_name):
    """ Return a given class which sits within a specified heirarchy.
    Used to return classes of filebuilders and domainobjects to only
    instantiate as and when that domainobject/filebuilder is required.

    Parameters
    ----------
    package_name : string
        The package the required class is in
    module_name : string
        The module within the package the required class is in
    class_name : string
        Name of the class

    Returns
    -------
    class
        Uninstantiated requested class
    """
    return getattr(importlib.import_module(package_name+'.'+module_name),
                   class_name)


def parse_config_files():
    """ Retrieve command line arguments, and extract the 4 core configuration
    sections from it. Return this information in a dictionary.

    Returns
    -------
    dict
        A four element dictionary containing all configuration sections from
        both user-facing and dev-facing configuration files.
    """

    command_line_args = get_args()

    with open(command_line_args.user_config) as user_config_file:
        user_config_file = ujson.load(user_config_file)
        domain_object_gen_config =\
            get_domain_object_config(user_config_file)
        shared_config = get_shared_config(user_config_file)

    with open(command_line_args.dev_config) as dev_config_file:
        dev_config_file = ujson.load(dev_config_file)
        file_builder_configs = get_file_builder_configs(dev_config_file)
        domain_object_location_config = \
            get_domain_object_location_config(dev_config_file)

    return {
        "generation_arguments": domain_object_gen_config,
        "domain_object_locations": domain_object_location_config,
        "shared_arguments": shared_config,
        "file_builders": file_builder_configs
    }


def get_args():
    """ Configure a parser to retrieve & parse command-line arguments
    input by the user.

    Returns
    -------
    namespace
        Namespace is populated with observed arguments, unless none observed,
        in which case default values are returned. Access elements via '.'
        convention, i.e. parser.parse_args().config
    """

    parser = ArgumentParser(description='''Random financial data
                                        generation. For more information,
                                        see the README''')
    parser.add_argument('--user_config', default='src/config.json',
                        help='JSON Configuration File Location')
    parser.add_argument('--dev_config', default='src/dev_config.json',
                        help='Developer Configuration File Location')
    return parser.parse_args()


def validate_configs(configurations):
    """ Ensure that the configuration file found adheres to required format
    to ensure correct generation of domain objects.

    Parameters
    ----------
    config : dict
        Parsed json of the user-input configuration

    Excepts
    -------
    ConfigError
        Where an validation of the provided configuration has failed.
        Raised only at the end of all checks such that all errors can be
        reported at once.
    """

    validation_result = config_validator.validate(configurations)
    try:
        if validation_result.check_success():
            print("No errors found in config")
        else:
            raise ConfigError()

    except ConfigError:
        print("Issue(s) within Config:")
        for error in validation_result.get_errors():
            print(error)
        # Re-raised to halt operation
        raise


def get_domain_object_config(config_file):
    """ Return the domain object section of the given configuration file.

    Parameters
    ----------
    config_file : dict
        Dictionary of parsed json configuration file

    Returns
    -------
    dict
        Domain object configuration of given config
    """

    return config_file['domain_objects']


def get_shared_config(config_file):
    """ Return the shared configuration section of the given configuration
    file.

    Parameters
    ----------
    config_file : dict
        Dictionary of parsed json configuration file

    Returns
    -------
    dict
        Shared generation configuration of given config
    """

    return config_file['shared_generation_arguments']


def get_file_builder_configs(config_file):
    """ Return the file builder section of the given configuration file.

    Parameters
    ----------
    config_file : dict
        Dictionary of parsed json configuration file

    Returns
    -------
    dict
        File builder configuration of given config
    """

    return config_file['file_builders']


def get_domain_object_location_config(config_file):
    """ Return the domain object file location in the codebase section of the
    given configuration file.

    Parameters
    ----------
    config_file : dict
        Dictionary of parsed json configuration file

    Returns
    -------
    dict
        Domain object file location in code base section of given config
    """

    return config_file['domain_objects']


if __name__ == '__main__':
    main()
