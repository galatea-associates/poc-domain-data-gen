import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_back_office_positions():
    """ Ensure all generated back office position attributes adhere to their
    specification. Dependencies on instruments. """

    records, domain_obj = helper.set_up_back_office_position_tests()
    for record in records:
        shared.attribute_quantity_valid('back_office_position', record, 9)
        shared.cusip_exists(record)
        shared.position_type_valid(record)
        shared.knowledge_date_valid(record)
        if record['position_type'] == 'SD':
            shared.settlement_position_effective_date_valid(record)
        else:
            shared.trade_position_effective_date_valid(record)
        shared.account_valid(record, domain_obj.BACK_OFFICE_ACCOUNT_TYPES)
        shared.direction_valid(record)
        shared.quantity_valid(record)
        shared.purpose_valid(record, domain_obj.BACK_OFFICE_PURPOSES)
