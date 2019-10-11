import sys
import pytest
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper


sys.path.insert(0, 'tests/')


def test_order_executions():
    records = helper.set_up_order_execution_tests()
    shared.unique_ids(records, 'order')
    for record in records:
        shared.account_number_valid(record)
        shared.direction_valid(record)
        sto_id_valid(record)
        agent_id_valid(record)
        shared.price_valid(record)
        shared.currency_valid(record)
        shared.ric_exists(record)
        shared.quantity_valid(record)


def sto_id_valid(record):
    id = record['sto_id']
    assert shared.is_int(id)\
        and shared.is_length(7, id)


def agent_id_valid(record):
    id = record['agent_id']
    assert shared.is_int(id)\
        and shared.is_length(7, id)
