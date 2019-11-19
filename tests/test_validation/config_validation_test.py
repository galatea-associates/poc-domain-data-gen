import copy
from configuration import configuration
from validator import config_validator as validator
from tests.resources.config_files.configuration_objects \
    import default_gen_arguments, default_domain_objects, \
    default_shared_arguments, default_file_builders
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

The validator returns a "Validation_Result" object, which contains a boolean
flag on whether the validation failed or succeeded. This value is what is
asserted against. Where tests are set up to fail, assert that the result is
False. Where tests are due to succeed, assert against True. """


def test_record_count_success():
    """ Ensure a valid configuration succeeds"""

    configurations = configuration.Configuration({
        "generation_arguments": default_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": default_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is True


def test_record_count_failure():
    """ Ensure a negative integer for record count fails """

    invalid_gen_arguments = copy.deepcopy(default_gen_arguments)
    invalid_gen_arguments[0]['instrument']['fixed_args']['record_count'] = -1

    configurations = configuration.Configuration({
        "generation_arguments": invalid_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": default_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False


def test_file_size_failure():
    """ Ensure negative integer for file size fails """

    invalid_gen_arguments = copy.deepcopy(default_gen_arguments)
    invalid_gen_arguments[0]['instrument']['max_objects_per_file'] = -1

    configurations = configuration.Configuration({
        "generation_arguments": invalid_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": default_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False


def test_file_extension_failure():
    """ Ensure an invalid file extension fails """

    invalid_gen_arguments = copy.deepcopy(default_gen_arguments)
    invalid_gen_arguments[0]['instrument']['output_file_type'] = 'invalid'

    configurations = configuration.Configuration({
        "generation_arguments": invalid_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": default_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False


def test_generator_pool_size_failure():
    """ Ensure a negative integer for pool sizes fails """

    invalid_shared_arguments = copy.deepcopy(default_shared_arguments)
    invalid_shared_arguments['generator_pool_size'] = -1

    configurations = configuration.Configuration({
        "generation_arguments": default_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": invalid_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False


def test_writer_pool_size_failure():
    """ Ensure a negative integer for pool sizes fails """

    invalid_shared_arguments = copy.deepcopy(default_shared_arguments)
    invalid_shared_arguments['writer_pool_size'] = -1

    configurations = configuration.Configuration({
        "generation_arguments": default_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": invalid_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False


def test_job_size_failure():
    """ Ensure a negative integer for job size fails """

    invalid_shared_arguments = copy.deepcopy(default_shared_arguments)
    invalid_shared_arguments['pool_job_size'] = -1

    configurations = configuration.Configuration({
        "generation_arguments": default_gen_arguments,
        "domain_objects": default_domain_objects,
        "shared_arguments": invalid_shared_arguments,
        "file_builders": default_file_builders
    })

    success = validator.validate(configurations).check_success()
    assert success is False
