""" verify that the user-provided config will execute the generation process
correctly. Should a given argument be invalid, strings are appended to a list
of errors.

Error list to be returned, and used as a basis to feedback to the user that
the configuration as-is is insufficient for successful operation.
"""


import sys


def validate(config):
    """ Entry point. Build a list of errors based on a number of tests, when
    returned can be used to feedback to the user what requires changing.

    Parameters
    ----------
    config : dict
        Parsed json of the user-input configuration

    Raises
    ------
    ConfigError
        Where an validation of the provided configuration has failed.
        Raised only at the end of all checks such that all errors can be
        reported at once.
    """

    # Temporarily remove traceback as all raised errors are from config #
    sys.tracebacklimit = 0

    domain_objects = config['domain_objects']
    file_builders = config['file_builders']
    shared_args = config['shared_args']

    swap_contract_config = domain_objects[9]
    swap_position_config = domain_objects[10]
    cash_flow_config = domain_objects[11]

    try:
        errors = []
        errors.append(validate_record_counts(domain_objects))
        errors.append(validate_max_file_size(domain_objects))
        errors.append(validate_output_file_extensions(file_builders, 
                                                      domain_objects))

        errors.append(validate_swap_contract_range(swap_contract_config))

        errors.append(validate_swap_position_date_range(swap_position_config))
        errors.append(validate_swap_position_range(swap_position_config))

        errors.append(validate_cash_flow_defined(cash_flow_config))
        errors.append(validate_cash_flow_definitions(cash_flow_config))

        errors.append(validate_pool_sizes_non_zero(shared_args))
        errors.append(validate_job_size_non_zero(shared_args))

        # Remove instances of None from error list
        errors = [error for error in errors if error != None]
        # Remove instances of empty lists from error list
        errors = [error for error in errors if error != []]
        # Flatten list of lists to single list
        errors = [error for sub_error in errors for error in sub_error]

        if len(errors) is not 0:
            raise ConfigError()

    except ConfigError:
        print("Issue(s) within Config:")
        for error in errors:
            print(error)
        raise

    else:
        print("No issues within Config")


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
            error = "- Record count for "+current_object+\
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
            error = "- File size for "+current_object+\
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
            error = "- File Builder, "+file_extension+", for "+\
                    current_object+" doesn't exist."
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

def validate_swap_contract_range(swap_contract_config):
    """ Ensure the swap contract "swaps per counterparty" is a valid range

    Parameters
    ----------
    swap_contract_config : dict
        The configuration section for the swap contract object only

    Returns
    -------
    List
        An error where the range is invalid, None otherwise
    """

    error = None

    custom_args = swap_contract_config['custom_args']
    swaps_per_counterparty = custom_args['swap_per_counterparty']
    swap_min = swaps_per_counterparty['min']
    swap_max = swaps_per_counterparty['max']

    if swap_max < swap_min:
        error = ["- Swap contract's swap minimum value greater"+\
                    " than swap maximum"]
    return error


def validate_swap_position_date_range(swap_position_config):
    """ Ensure the swap position date range is valid where both start and
    end date have been user-provided. 

    Parameters
    ----------
    swap_position_config: dict
        The configuration section for the swap position object only

    Returns
    -------
    List
        An error where the range is invalid, None otherwise
    """
    
    return


def validate_swap_position_range(swap_position_config):
    return


def validate_cash_flow_defined(cash_flow_config):
    return


def validate_cash_flow_definitions(cash_flow_config):
    return


def validate_pool_sizes_non_zero(shared_config):
    return


def validate_job_size_non_zero(shared_config):
    return


class ConfigError(Exception):
    """ Raised when there is an issue with the user-defined configuration.
    Due to prior checks compiling a list of these, all are returned and
    displayed to the user.
    """

    def __init__(self):
        pass