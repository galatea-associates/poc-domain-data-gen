import sys
sys.path.insert(0, 'tests/')
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper


def test_counterparty():
    records = helper.set_up_counterparty_tests()
    shared.unique_ids(records, 'counterparty')
    for record in records:
        shared.attribute_quantity_valid(record, 13)
        book_valid(record)
        shared.dummy_fields_valid(record, 'counterparty')


def book_valid(record):
    book = record['book']
    assert shared.is_length(5, book) and\
        not shared.contains_numbers(book)
