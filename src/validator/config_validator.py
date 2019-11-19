""" verify that the user-provided config will execute the generation process
correctly. Should a given argument be invalid, strings are appended to a list
of errors.

Error list to be returned, and used as a basis to feedback to the user that
the configuration as-is is insufficient for successful operation.
"""
from validator.validation_result import Validation_Result


def validate(configurations):
    """ Entry point. Build a list of errors based on a number of tests, when
    returned can be used to feedback to the user what requires changing.

    Parameters
    ----------
    config : dict
        Parsed json of the user-input configuration

    Returns
    validation_result : Validation_Result
        An object containing a boolean flag for success or fail, as well as
        a list of any errors on the case of failure.
    """

    domain_objects = {}
    for domain_object in configurations['generation_arguments']:
        domain_objects.update(domain_object)

    file_builders = {}
    for file_builder in configurations['file_builders']:
        file_builders.update(file_builder)

    shared_args = configurations['shared_arguments']

    errors = [
        validate_record_counts(domain_objects),
        validate_max_file_size(domain_objects),
        validate_output_file_extensions(file_builders, domain_objects),
        validate_pool_sizes_non_zero(shared_args),
        validate_job_size_non_zero(shared_args)
    ]

    # Remove instances of None or empty lists from error list
    errors = [error for error in errors if error]
    # Flatten list of lists to single list
    errors = [error for sub_error in errors for error in sub_error]

    # boolean coercion evaluates 'errors' as True if not empty
    if errors:
        return Validation_Result(False, errors)
    else:
        return Validation_Result(True, None)


def validate_record_counts(domain_object_configs):
    """ Ensure the record count for each domain object is zero or above.

    Parameters
    ----------
    domain_object_configs : dict
        List of dictionaries, each dictionary containing the configuration
        settings for a single domain object.

    Returns
    -------
    List
        List of strings detailing each domain object where record
        count is erroneous. Empty where there are no errors to be found.
    """

    errors = []
    for domain_object, config in domain_object_configs.items():
        record_count = config['fixed_args']['record_count']
        if record_count < 0:
            errors.append(f'- Record count for domain object ' +
                          f'\'{domain_object}\' is less than 0')
    return errors


def validate_max_file_size(domain_object_configs):
    """ Ensure the maximum file size for each object is greater than 0.

    Parameters
    ----------
    domain_object_configs : dict
        List of dictionaries, each dictionary containing the configuration
        settings for a single domain object.

    Returns
    -------
    List
        List of strings detailing each domain object where maximum file
        size is erroneous. Empty where there are no errors to be found.
    """

    errors = []

    for domain_object, config in domain_object_configs.items():
        file_size = config['max_objects_per_file']
        if file_size < 0:
            errors.append(f'- File size for domain object ' +
                          f'\'{domain_object}\' is less than 0')
    return errors


def validate_output_file_extensions(file_builder_configs,
                                    domain_object_configs):
    """ Ensure the file extension for each object is valid as per the defined
    file builders.

    Parameters
    ----------

    Returns
    -------
    List
        List of strings detailing each domain object where the specified file
        extension
    """

    errors = []
    file_extensions = get_file_extensions(file_builder_configs)

    for domain_object, config in domain_object_configs.items():
        file_extension = config['output_file_type']
        if file_extension not in file_extensions:
            errors.append(f'- File type \'{file_extension}\' for ' +
                          f'domain object \'{domain_object}\' does not ' +
                          'have a file builder defined')
    return errors


def get_file_extensions(file_builder_configs):
    """ Retrieve the file extensions currently supported as per their config
    definitions.

    Parameters
    ----------
    file_builder_configs: list
        List of dictionaries, each dictionary being the description of a
        single file builder type/extension.

    Returns
    -------
    List
        List containing all supported file types.
    """

    return list(file_builder_configs.keys())


def validate_pool_sizes_non_zero(shared_config):
    """ Verifies that pool sizes for both generation and writing pools are
    non-zero and positive.

    Parameters
    ----------
    shared_config : dict
        Dictionary of the "shared_config" section of the config file

    Returns
    -------
    List
        Errors where relevant, or empty if none found
    """

    errors = []

    gen_pool_size = shared_config['generator_pool_size']
    write_pool_size = shared_config['writer_pool_size']
    if gen_pool_size <= 0:
        errors.append("- Generation pool size must be a positive value.")
    if write_pool_size <= 0:
        errors.append("- Writing pool size must be a positive value.")
    return errors


def validate_job_size_non_zero(shared_config):
    """ Ensure the specified job size is a non-zero numbers.

    Parameters
    ----------
    shared_config : dict
        Dictionary of the "shared_config" section of the config file

    Returns
    -------
    list
        List of a single object, an error message, if job size strictly
        less than zero, contains nothing otherwise.
    """

    error = []
    job_size = shared_config['pool_job_size']
    if job_size <= 0:
        error = ["- Pool job size must be a positive value"]
    return error
