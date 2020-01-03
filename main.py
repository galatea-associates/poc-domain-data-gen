from os.path import exists
from os import unlink
from argparse import ArgumentParser
from ujson import load
from multiprocessing import Process, Lock
from importlib import import_module
from time import time


# MAIN

def main():
    # SETUP
    delete_database()
    configs = get_configs()
    lock = Lock()

    domain_object_configs = configs["domain_objects"]
    file_builder_args = configs["file_builder_args"]
    generator_args = configs["generator_args"]

    independent_domain_objects = ("instrument", "account")

    # MULTIPROCESS INSTRUMENTS AND ACCOUNTS

    independent_domain_objects = get_independent_domain_objects(
        domain_object_configs,
        independent_domain_objects
    )

    multiprocess(
        independent_domain_objects,
        file_builder_args,
        generator_args,
        lock
    )

    # MULTIPROCESS DEPENDENT DOMAIN OBJECTS

    dependent_domain_objects = get_dependent_domain_objects(
        domain_object_configs,
        independent_domain_objects
    )

    multiprocess(
        dependent_domain_objects,
        file_builder_args,
        generator_args,
        lock
    )


# PRIMARY HELPER FUNCTIONS

def delete_database():
    if exists("dependencies.db"):
        unlink("dependencies.db")


def get_configs():
    args = get_args()
    with open(args.user_config) as user_config:
        parsed_user_config = load(user_config)
        domain_objects = parsed_user_config["domain_objects"]

    with open(args.dev_config) as dev_config:
        parsed_dev_config = load(dev_config)
        generator_args = parsed_dev_config["generator_args"]
        file_builder_args = parsed_dev_config["file_builder_args"]

    configs = {
        "domain_objects": domain_objects,
        "generator_args": generator_args,
        "file_builder_args": file_builder_args
    }

    return configs


def get_independent_domain_objects(
        domain_object_configs, independent_domain_objects
):
    return [
        domain_object_config for domain_object_config in domain_object_configs
        if list(domain_object_config.keys())[0] in independent_domain_objects
    ]


def get_dependent_domain_objects(
        domain_object_configs, independent_domain_objects
):
    return [
        domain_object_config for domain_object_config in domain_object_configs
        if list(domain_object_config.keys())[0]
        not in independent_domain_objects
    ]


def multiprocess(
        domain_object_configs,
        file_builder_args,
        generator_args,
        lock
):
    processes = []

    for domain_object_config in domain_object_configs:

        domain_object, config = list(domain_object_config.items())[0]

        max_objects_per_file = config["max_objects_per_file"]
        record_count = config["record_count"]
        output_directory = config["output_directory"]
        file_name_template = config['file_name']
        file_builder_name = config["output_file_type"]

        number_of_max_capacity_files = record_count // max_objects_per_file
        residual_quantity = record_count % max_objects_per_file

        file_builder_config = file_builder_args[file_builder_name]
        generator_config = generator_args[domain_object]

        process = Process(
            target=write_files, args=(
                max_objects_per_file,
                output_directory,
                number_of_max_capacity_files,
                residual_quantity,
                file_name_template,
                file_builder_config,
                generator_config,
                lock
            )
        )

        process.start()
        processes.append(process)

    for process in processes:
        process.join()


# SECONDARY HELPER FUNCTIONS

def get_args():
    parser = ArgumentParser(description='''Random financial data
                                            generation. For more information,
                                            see the README''')
    parser.add_argument('--user_config', default='config.json',
                        help='JSON Configuration File Location')
    parser.add_argument('--dev_config', default='dev_config.json',
                        help='Developer Configuration File Location')
    return parser.parse_args()


def write_files(
        max_objects_per_file,
        output_directory,
        number_of_max_capacity_files,
        residual_quantity,
        file_name_template,
        file_builder_config,
        generator_config,
        lock
):

    child_processes = []

    if residual_quantity > 0:
        number_of_files = number_of_max_capacity_files + 1
    else:
        number_of_files = number_of_max_capacity_files

    quantity = max_objects_per_file

    for file_number in range(number_of_files):
        file_name = f"{file_name_template}_{file_number:05}"

        file_builder = get_file_builder(file_builder_config)

        if file_number == number_of_max_capacity_files:
            quantity = residual_quantity

        start_id = file_number * max_objects_per_file

        process = Process(
            target=file_builder.build,
            args=(
                output_directory,
                file_name,
                generator_config,
                quantity,
                lock,
                start_id
            )
        )

        process.start()
        child_processes.append(process)

    for process in child_processes:
        process.join()


def get_file_builder(file_builder_config):
    module_name = file_builder_config["module_name"]
    class_name = file_builder_config["class_name"]
    file_builder = get_class("file_builders", module_name, class_name)
    return file_builder


def get_class(package_name, module_name, class_name):
    module = import_module(f"{package_name}.{module_name}")
    return getattr(module, class_name)


if __name__ == '__main__':
    start = time()
    main()
    total = time() - start
    print(f'completed in {total//60} minutes and {total%60} seconds')
