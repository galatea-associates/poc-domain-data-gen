import sys
sys.path.insert(0, 'tests/')
import pytest
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper

def test_back_office_positions():
    """ Ensure all generated back office position attributes adhere to their
    specification. Dependencies on instruments. """

    records, domain_obj = helper.set_up_back_office_position_tests()
    for record in records:
        shared.cusip_exists(record)
        shared.position_type_valid(record)
        shared.knowledge_date_valid(record)
        if (record['position_type'] == 'SD'):
            shared.settlement_position_effective_date_valid(record)
        else:
            shared.trade_position_effective_date_valid(record)
        shared.account_valid(record, domain_obj.ACCOUNT_TYPES)
        shared.direction_valid(record)
        shared.quantity_valid(record)
        shared.purpose_valid(record, domain_obj.BACK_OFFICE_PURPOSES)