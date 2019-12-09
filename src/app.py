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

    The generation coordinator received instruction to generate X number of
    objects over Y number of subprocesses (Pool Size). Once these jobs are
    executed and records returned, they are placed into a writing job queue.
    The writing to file coordinator picks up & formats these tasks before
    assigning them to execute on a second pool

"""

import importlib
import ujson
import os
import sys
from argparse import ArgumentParser
from database.sqlite_database import Sqlite_Database
from multi_processing.coordinator import Coordinator
from exceptions.config_error import ConfigError
from configuration.configuration import Configuration
import validator.config_validator as config_validator
from utils.google_drive_connector import GoogleDriveConnector


def main():
    delete_database()

    configurations = parse_config_files()
    validate_configs(configurations)

    factory_definitions = configurations.get_factory_definitions()
    shared_args = configurations.get_shared_args()
    dev_file_builder_args = configurations.get_dev_file_builder_args()
    dev_factory_args = configurations.get_dev_factory_args()

    for factory_definition in factory_definitions:
        file_builder = instantiate_file_builder(factory_definition,
                                                dev_file_builder_args,
                                                shared_args)
        object_factory = instantiate_object_factory(dev_factory_args,
                                                    factory_definition,
                                                    shared_args)
        process_object_factory(file_builder, object_factory)


def process_object_factory(file_builder, object_factory):
    """ Instantiates generation and file-writing processes. Populates the
    generation job queue & starts both generation and writing coordinators.
    Awaits for both coordinators to terminate before continuing to the next
    domain object, or finishing execution.

    Parameters
    ----------
    file_builder : File_Builder
        An instantiated filebuilder as per this objects required output
        file type
    object_factory : ObjectFactory
        Instantiated object factory for the object to generate. Contains
        generation parameters as well as the multiprocessing shared arguments.
    """

    object_factory.set_batch_size()
    coordinator = Coordinator(file_builder, object_factory)

    coordinator.start_generate_process()
    coordinator.start_write_process()
    coordinator.add_jobs_to_generation_queue()
    coordinator.await_termination()


def instantiate_file_builder(factory_definition,
                             dev_file_builder_args,
                             shared_args):
    """ Returns file builder object from provided configs

    Parameters
    ----------
    factory_definition : dict
        A domain object configuration as provided by user
    dev_file_builder_args: dict
        Developer arguments defining where in the codebase file builder
        classes are defined
    shared_args: dict
        User arguments defining parameters for multiprocessing and google drive
        upload, which are fixed for all object factories and file builders

    Returns
    -------
    File_Builder
        Instantiated file builder as defined by the file builder
        configurations, as per the user specified output type of
        the given object configuration
    """

    factory_name = next(iter(factory_definition))
    factory_args = factory_definition[factory_name]

    file_builder_name = factory_args['output_file_type']
    file_builder_config = get_dev_file_builder_config(dev_file_builder_args,
                                                      file_builder_name)
    file_builder_class = get_class('filebuilders',
                                   file_builder_config['module_name'],
                                   file_builder_config['class_name'])

    google_drive_connector = get_google_drive_connector(factory_definition,
                                                        shared_args)
    return file_builder_class(google_drive_connector, factory_args)


def get_google_drive_connector(factory_definition, shared_args):
    """ Return an instance of the Google Drive Connector object if the
    object factory specified in factory_definition is configured to have
    records uploaded to google drive. The Google Drive root folder id specified
    in shared_args is used as the Drive directory for upload.

    If the factory_definition is not configured to upload to Drive, the method
    will return None.

    Parameters
    ----------
    factory_definition : dict
        A domain object configuration as provided by user
    shared_args: dict
        User arguments defining parameters for multiprocessing and google drive
        upload, which are fixed for all object factories and file builders

    Returns
    -------
    GoogleDriveConnector
        Instantiated connector object for uploading to a pre-defined google
        drive directory.
    """
    google_drive_flag = \
        list(factory_definition.values())[0]['upload_to_google_drive'].upper()

    if google_drive_flag == 'TRUE':
        root_folder_id = shared_args['google_drive_root_folder_id']
        return GoogleDriveConnector(root_folder_id)


def instantiate_object_factory(dev_factory_args,
                               factory_arguments,
                               shared_args):
    """ Returns factory object from provided configs

    Parameters
    ----------
    dev_factory_args: dict
        Developer arguments defining where in the codebase factory classes are
        defined
    factory_arguments: dict
        User arguments defining the parameters which generation will adhere to
    shared_args: dict
        User arguments defining parameters for multiprocessing and google drive
        upload, which are fixed for all object factories and file builders

    Returns
    -------
    Generatable
        Instantiated subclass of generatable as defined by the dev factory
        arguments, as per the user specified object type this factory is to
        generate.
    """

    object_factory_name = next(iter(factory_arguments))
    object_factory_config = get_dev_object_factory_config(dev_factory_args,
                                                          object_factory_name)
    object_factory_class = get_class('domainobjectfactories',
                                     object_factory_config['module_name'],
                                     object_factory_config['class_name'])
    return object_factory_class(factory_arguments[object_factory_name],
                                shared_args)


def get_record_count(obj_config, obj_location):
    """ Returns the number of records to be produced for a given object.
    Where objects are non-dependent on others, the user-provided configuration
    amount is used. Otherwise, the record_count is set to be the number of
    records produced of the domain object the to-generate one is dependent
    on.

    Parameters
    ----------
    obj_config : dict
        A domain objects configuration as provided by user
    obj_location : dict
        domain object location configuration from dev config, specifying
        module and class names within the file system

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


def get_dev_file_builder_config(file_builders, file_extension):
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
    return file_builder_dict[file_extension]


def get_dev_object_factory_config(dev_factory_args, object_factory_name):
    """ Get the developer-set object configuration specifying where in the
    codebase the class sits.

    Parameters
    ----------
    dev_factory_args : dict
        The locations of all object factories within the codebase
    object_factory_name : string
        The name of the object factory due to be used for generation

    Returns
    -------
    dict
        The module/class names where the given object name sits within the
        codebase
    """

    dev_factory_args_dict = dev_factory_args[0]
    return dev_factory_args_dict[object_factory_name]


def get_class(package_name, module_name, class_name):
    """ Return a given class which sits within a specified heirarchy.
    Used to return classes of filebuilders and domainobjectfactories to only
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
    sections from it. Return this information as a Configuration object.

    Returns
    -------
    Configuration
        An object instantiated to contain all 4 configuration types. Has
        retrieval methods defined within.
    """
    args = get_args()
    with open(args.user_config) as user_config:
        parsed_user_config = ujson.load(user_config)
        factory_definitions = parsed_user_config['factory_definitions']
        shared_args = parsed_user_config['shared_args']

    with open(args.dev_config) as dev_config:
        parsed_dev_config = ujson.load(dev_config)
        dev_file_builder_args = parsed_dev_config['dev_file_builder_args']
        dev_factory_args = parsed_dev_config['dev_factory_args']

    return Configuration({
        "factory_definitions": factory_definitions,
        "shared_args": shared_args,
        "dev_file_builder_args": dev_file_builder_args,
        "dev_factory_args": dev_factory_args
    })


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
    configurations : dict
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
        print("Issue(s) within Config:\n")
        for error in validation_result.get_errors():
            print(error)
        sys.exit()


def delete_database():
    """ Remove an existing database if one already exists. Used to ensure
    that subsequent generation is from a valid set of pre-generated
    dependencies.
    """

    if os.path.exists('dependencies.db'):
        os.unlink('dependencies.db')


if __name__ == '__main__':
    main()
