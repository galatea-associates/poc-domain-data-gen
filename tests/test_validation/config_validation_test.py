import sys
sys.path.insert(0, 'src/')
from validator import config_validator as validator 
import json


def test_record_count():
    run_test("record_count")


def test_file_size():
    run_test("file_size")


def test_file_extension():
    run_test("file_extension")


def test_pool_size():
    run_test("pool_size")


def test_job_size():
    run_test("job_size")


def run_test(test_name):
    success_config = load_file(test_name+"_success.json")
    failure_config = load_file(test_name+"_fail.json")
    success_result = run_validation(success_config).check_success()
    fail_result = run_validation(failure_config).check_success()
    assert success_result and not fail_result


def load_file(file_name):
    file_path = "tests/resources/config_files/" + file_name
    with open(file_path) as file:
        return json.load(file)


def run_validation(config_file):
    return validator.validate(config_file)
