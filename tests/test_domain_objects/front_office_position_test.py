import sys
import pytest
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper


sys.path.insert(0, 'tests/')


def test_front_office_position():
    records, domain_obj = helper.set_up_front_office_position_tests()
    for record in records:
        shared.ric_exists(record)
        shared.position_type_valid(record)
        shared.knowledge_date_valid(record)
        if record['position_type'] == 'TD':
            shared.trade_position_effective_date_valid(record)
        else:
            shared.settlement_position_effective_date_valid(record)
        shared.account_valid(record, domain_obj.ACCOUNT_TYPES)
        shared.direction_valid(record)
        shared.quantity_valid(record)
        shared.purpose_valid(record,
            domain_obj.FRONT_OFFICE_POSITION_PURPOSES)
