import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_trades():
    records = helper.set_up_trades()
    shared.unique_ids(records, 'order')
    for record in records:
        shared.attribute_quantity_valid('trade', record, 10)
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
