from src.utils.google_drive_connector import GoogleDriveConnector
from src.filebuilders.csv_builder import CSVBuilder
from src.filebuilders.json_builder import JSONBuilder
from src.filebuilders.xml_builder import XMLBuilder
from src.filebuilders.jsonl_builder import JSONLBuilder
from tests.resources.drive_files.config_stub import csv_config, xml_config, \
    json_config, jsonl_config
from tests.resources.drive_files.data_stub import data
from datetime import datetime, timezone
import pytest

folder_creation_timestamp = '000000'


@pytest.fixture(scope='module', autouse=True)
def gd_conn():
    """This is a setup/teardown function (called a fixture in pytest)
    All code before the yield statement is setup, and any test that is
    passed this function name as a parameter will have access to the object
    from the yield statement.

    All code after 'yield' is teardown, executed once at
    the end of the last test in the module.

    Useful documentation: https://docs.pytest.org/en/latest/fixture.html
    """
    # SETUP:
    gd_conn = GoogleDriveConnector("root", folder_creation_timestamp)
    yield gd_conn

    # TEAR DOWN:
    delete_folder(gd_conn)


def get_folder_id(gd_conn):
    """ get the ID for the folder that test files have been uploaded into"""
    today = datetime.now(timezone.utc).date().strftime('%Y-%m-%d')
    date_folder_id = gd_conn.get_folder_id(today, 'root')
    return gd_conn.get_folder_id(folder_creation_timestamp, date_folder_id)


def upload(gd_conn, fb_class, fb_config):
    fb = fb_class(gd_conn, fb_config)
    # build file locally and upload to google drive
    fb.build(1, data)


def file_exists(gd_conn, file_name):
    folder_id = get_folder_id(gd_conn)
    if folder_id is None:
        return False
        # no folder created - upload failed
    else:
        file_id = gd_conn.get_file_id(file_name, folder_id)
        return file_id is not None


def delete_folder(gd_conn):
    """ for tear down - deletes drive folder and all contents"""
    folder_id = get_folder_id(gd_conn)
    gd_conn.delete_folder(folder_id)


def test_csv_upload(gd_conn):
    upload(gd_conn, CSVBuilder, csv_config)
    file_name = 'csv_test_file_001.csv'
    assert file_exists(gd_conn, file_name)


def test_xml_upload(gd_conn):
    upload(gd_conn, XMLBuilder, xml_config)
    file_name = 'xml_test_file_001.xml'
    assert file_exists(gd_conn, file_name)


def test_json_upload(gd_conn):
    upload(gd_conn, JSONBuilder, json_config)
    file_name = 'json_test_file_001.json'
    assert file_exists(gd_conn, file_name)


def test_jsonl_upload(gd_conn):
    upload(gd_conn, JSONLBuilder, jsonl_config)
    file_name = 'jsonl_test_file_001.jsonl'
    assert file_exists(gd_conn, file_name)
