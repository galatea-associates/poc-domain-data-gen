""" verify that the user-provided config will execute the generation process
correctly. Should a given argument be invalid, strings are appended to a list
of errors.

Error list to be returned, and used as a basis to feedback to the user that
the configuration as-is is insufficient for successful operation.
"""
from validator.validation_result import Validation_Result


def validate(config):
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
    # TODO: refactor for new configurations
    domain_objects = config['domain_objects']
    file_builders = config['file_builders']
    shared_args = config['shared_args']

    errors = []
    errors.append(validate_record_counts(domain_objects))
    errors.append(validate_max_file_size(domain_objects))
    errors.append(validate_google_drive_flag(domain_objects))
    errors.append(validate_output_file_extensions(file_builders,
                                                  domain_objects))

    errors.append(validate_pool_sizes_non_zero(shared_args))
    errors.append(validate_job_size_non_zero(shared_args))

    # Remove instances of None from error list
    errors = [error for error in errors if error is not None]
    # Remove instances of empty lists from error list
    errors = [error for error in errors if error != []]
    # Flatten list of lists to single list
    errors = [error for sub_error in errors for error in sub_error]

    if len(errors) != 0:
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
    for config in domain_object_configs:
        current_object = config['class_name']
        record_count = int(config['record_count'])
        if record_count < 0:
            error = "- Record count for " + current_object + \
                    " is less than 0."
            errors.append(error)
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
    for config in domain_object_configs:
        current_object = config['class_name']
        file_size = int(config['max_objects_per_file'])
        if file_size < 0:
            error = "- File size for " + current_object + \
                    " is less than 0."
            errors.append(error)
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

    for config in domain_object_configs:
        current_object = config['class_name']
        file_extension = config['file_builder_name']
        if file_extension not in file_extensions:
            error = "- File Builder, " + file_extension + ", for " + \
                    current_object + " doesn't exist."
            errors.append(error)
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

    file_extensions = []
    for config in file_builder_configs:
        file_extensions.append(config['name'])
    return file_extensions

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

    gen_pool_size = shared_config['gen_pools']
    write_pool_size = shared_config['write_pools']
    if gen_pool_size <= 0:
        errors.append("- Generation Pool size must be a positive value.")
    if write_pool_size <= 0:
        errors.append("- Writing Pool size must be a positive value.")
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

    error = None
    job_size = shared_config['job_size']
    if job_size <= 0:
        error = ["- Job_Size in shared arguments must be a positive value"]
    return error


def validate_google_drive_flag(domain_object_configs):
    """ Ensure the google drive flag for each domain object is valid
    (either 'true' or 'false').

    Parameters
    ----------
    domain_object_configs : dict
        List of dictionaries, each dictionary containing the configuration
        settings for a single domain object.

    Returns
    -------
    List
        List of strings detailing each domain object where google drive flag
        is erroneous. Empty where there are no errors to be found.
    """
    errors = []
    for config in domain_object_configs:
        current_object = config['class_name']
        google_drive_flag = config['upload_to_google_drive']
        if google_drive_flag.upper() not in ("TRUE", "FALSE"):
            error = f"- Invalid Google Drive Flag \'{google_drive_flag}\'" \
                    f"for domain object {current_object}"
            errors.append(error)
    return errors

