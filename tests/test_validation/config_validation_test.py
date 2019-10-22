""" The approach used in each of these tests hinges on a pre-written config
file. This file will either be set up to pass all validation, or fail a single
point of validation.

The validator returns a "Validation_Result" object, which contains a boolean
flag on whether the validation failed or succeeded. This value is what is
asserted against. Where tests are set up to fail, assert that the result is
False. Where tests are due to succeed, assert against True. """
import sys
sys.path.insert(0, 'src/')
from validator import config_validator as validator 
import json


def test_record_count_success():
    """ Ensure a positive integer for record count succeeds """

    config_location = \
        "tests/resources/config_files/record_count_success.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is True


def test_record_count_failure():
    """ Ensure a negative integer for record count fails """

    config_location = \
        "tests/resources/config_files/record_count_failure.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is False


def test_file_size_success():
    """ Ensure a positive integer for file size succeeds """

    config_location = \
        "tests/resources/config_files/file_size_success.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is True


def test_file_size_failure():
    """ Ensure negative integer for file size fails """

    config_location = \
        "tests/resources/config_files/file_size_failure.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is False


def test_file_extension_success():
    """ Ensure a valid file extension succeeds """

    config_location = \
        "tests/resources/config_files/file_extension_success.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is True


def test_file_extension_failure():
    """ Ensure an invalid file extension fails """

    config_location = \
        "tests/resources/config_files/file_extension_failure.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is False


def test_pool_size_success():
    """ Ensure a positive integer for pool sizes succeeds """

    config_location = \
        "tests/resources/config_files/pool_size_success.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is True


def test_pool_size_failure():
    """ Ensure a negative integer for pool sizes fails """

    config_location = \
        "tests/resources/config_files/pool_size_failure.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is False


def test_job_size_success():
    """ Ensure a positive integer for job size succeeds """

    config_location = \
        "tests/resources/config_files/job_size_success.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is True


def test_job_size_failure():
    """ Ensure a negative integer for job size fails """

    config_location = \
        "tests/resources/config_files/job_size_failure.json"
    with open(config_location) as file:
        config = json.load(file)
    success = validator.validate(config).check_success()
    assert success is False
