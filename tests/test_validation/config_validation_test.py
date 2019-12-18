import copy
from configuration import configuration
from validator import config_validator as validator
from tests.resources.config_files.configuration_objects\
    import default_factory_definitions, default_shared_args,\
    default_dev_file_builder_args, default_dev_factory_args
"""
In the main method of src/app.py, the user and dev JSON config files are
converted to Python objects using the ujson library prior to validation. The
objects loaded from JSON are then bundled into a dictionary and passed to the
constructor of the Configuration class to create a Configuration object.

The Configuration object is then passed to the validate method of the
validate.py module. This is the method we are testing in these test cases. As
such, a Configuration object is mocked appropriately for each test case.

Test stubs of the Python objects created by ujson are imported from
tests/resources/config_files/configuration_objects.py.
These are valid by default, and represent the use of a single domain object
factory to output to a CSV file. To mock invalid configs, the relevant stub
is deep copied then modified to introduce an invalid parameter.

For more info on deep copying and the copy library see here:
https://www.programiz.com/python-programming/shallow-deep-copy

The validator returns a "ValidationResult" object, which contains a boolean
flag on whether the validation failed or succeeded. This value is what is
asserted against. Where tests are set up to fail, assert that the result is
False. Where tests are due to succeed, assert against True. """


def test_valid_config_success():
    """ Ensure a valid configuration succeeds"""

    configurations = configuration.Configuration(
        {
            "factory_definitions": default_factory_definitions,
            "shared_args": default_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is True


def test_record_count_failure():
    """ Ensure a negative integer for record count fails """

    invalid_factory_definitions = copy.deepcopy(default_factory_definitions)
    invalid_factory_definitions[0]['instrument']['fixed_args']['record_count']\
        = -1

    configurations = configuration.Configuration(
        {
            "factory_definitions": invalid_factory_definitions,
            "shared_args": default_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False


def test_file_size_failure():
    """ Ensure negative integer for file size fails """

    invalid_factory_definitions = copy.deepcopy(default_factory_definitions)
    invalid_factory_definitions[0]['instrument']['max_objects_per_file'] = -1

    configurations = configuration.Configuration(
        {
            "factory_definitions": invalid_factory_definitions,
            "shared_args": default_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False


def test_file_extension_failure():
    """ Ensure an invalid file extension fails """

    invalid_factory_definitions = copy.deepcopy(default_factory_definitions)
    invalid_factory_definitions[0]['instrument']['output_file_type']\
        = 'invalid'

    configurations = configuration.Configuration(
        {
            "factory_definitions": invalid_factory_definitions,
            "shared_args": default_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False


def test_number_of_create_child_processes_failure():
    """ Ensure a negative integer for pool sizes fails """

    invalid_shared_args = copy.deepcopy(default_shared_args)
    invalid_shared_args['number_of_create_child_processes'] = -1

    configurations = configuration.Configuration(
        {
            "factory_definitions": default_factory_definitions,
            "shared_args": invalid_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False


def test_number_of_write_child_processes_failure():
    """ Ensure a negative integer for pool sizes fails """

    invalid_shared_args = copy.deepcopy(default_shared_args)
    invalid_shared_args['number_of_write_child_processes'] = -1

    configurations = configuration.Configuration(
        {
            "factory_definitions": default_factory_definitions,
            "shared_args": invalid_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False


def get_success_for_changed_number_of_records_per_job(
        number_of_records_per_job
):
    """ helper method that returns the validation result for a
    number_of_records_per_job value given as a parameter - used to test values
    either side of the valid range"""
    invalid_shared_args = copy.deepcopy(default_shared_args)
    invalid_shared_args['number_of_records_per_job'] = \
        number_of_records_per_job
    configurations = configuration.Configuration(
        {
            "factory_definitions": default_factory_definitions,
            "shared_args": invalid_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()

    return success


def test_failure_given_negative_number_of_records_per_job():
    """ Ensure negative number of records causes failure"""
    assert get_success_for_changed_number_of_records_per_job(-1) is False


def test_failure_given_excessive_number_of_records_per_job():
    """Ensure a number_of_records_per_job greater than the smallest
    'max_records_per_file' value in the config causes failure"""
    maximum_number_of_records_per_job = \
        default_factory_definitions[0]['instrument']['max_objects_per_file']

    invalid_positive_number_of_records_per_job = \
        maximum_number_of_records_per_job + 1

    assert get_success_for_changed_number_of_records_per_job(
        invalid_positive_number_of_records_per_job
    ) is False


def test_failure_given_invalid_type_for_number_of_records_per_job():
    """ ensure a non-int value for 'number_of_records_per_job' causes
    failure by testing against all basic types and several commonly
    used python types"""
    float_value = 1.5,
    complex_value = 1.5 + 1.5j
    str_value = "1.5"
    nonetype_value = None
    list_value = []
    tuple_value = (1.5,)
    range_value = range(5)
    dict_value = {"value": 1.5}
    set_value = {1.5}
    byte_value = b"1.5"
    invalid_values = (
        float_value, complex_value, str_value, nonetype_value, list_value,
        tuple_value, range_value, dict_value, set_value, byte_value
    )
    success = False
    failing_types = []
    for invalid_value in invalid_values:
        success_for_invalid_value = \
            get_success_for_changed_number_of_records_per_job(invalid_value)
        if success_for_invalid_value:
            failing_types.append(type(invalid_value).__name__)
        success = success or success_for_invalid_value

    assert success is False, f"types causing test to fail: {failing_types}"


def test_google_drive_flag_failure():
    """ Ensure an invalid string for the google drive flag fails"""

    invalid_factory_definitions = copy.deepcopy(default_factory_definitions)
    invalid_factory_definitions[0]['instrument']['upload_to_google_drive']\
        = 'invalid'

    configurations = configuration.Configuration(
        {
            "factory_definitions": invalid_factory_definitions,
            "shared_args": default_shared_args,
            "dev_file_builder_args": default_dev_file_builder_args,
            "dev_factory_args": default_dev_factory_args
        }
    )

    success = validator.validate(configurations).check_success()
    assert success is False
