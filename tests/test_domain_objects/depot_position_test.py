import sys
sys.path.insert(0, 'tests/')
import pytest
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper

def test_depot_position():
    records, domain_obj = helper.set_up_depot_position_tests()
    for record in records:
        shared.isin_exists(record)
        shared.knowledge_date_valid(record)
        shared.position_type_valid(record)
        if record['position_type'] == 'TD':
            shared.trade_position_effective_date_valid(record)
        else:
            shared.settlement_position_effective_date_valid(record)
        shared.account_valid(record, domain_obj.ACCOUNT_TYPES)
        shared.quantity_valid(record)
        shared.purpose_valid(record, domain_obj.DEPOT_POSITION_PURPOSES)
        depot_id_valid(record)

def depot_id_valid(record):
    id = record['depot_id']
    assert shared.is_int(id) and\
        shared.is_length(5, id)