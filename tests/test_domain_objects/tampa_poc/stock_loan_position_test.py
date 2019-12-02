import sys

import pytest

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


@pytest.mark.skip(reason="Object being tested belongs to Tampa PoC and is "
                         "not mentioned in the one-pager")
def test_stock_loan_positions():
    records, domain_obj = helper.set_up_stock_loan_position_tests()
    shared.unique_ids(records, 'stock_loan_contract')
    for record in records:
        shared.attribute_quantity_valid('stock_loan_position', record, 17)
        shared.ric_exists(record)
        shared.knowledge_date_valid(record)
        shared.settlement_position_effective_date_valid(record)
        shared.purpose_valid(record, domain_obj.STOCK_LOAN_POSITION_PURPOSES)
        td_quantity_valid(record)
        sd_quantity_valid(record)
        collateral_type_valid(record, domain_obj.COLLATERAL_TYPES)
        haircut_valid(record)
        collateral_margin_valid(record)
        rebate_rate_valid(record)
        borrow_fee_valid(record)
        # termination_date_valid(record)
        shared.account_valid(record, domain_obj.ACCOUNT_TYPES)
        is_callable_valid(record)
        return_type_valid(record, domain_obj.RETURN_TYPES)


def td_quantity_valid(record):
    quantity = record['td_qty']
    assert 1 <= quantity <= 10000


def sd_quantity_valid(record):
    quantity = record['sd_qty']
    assert 1 <= quantity <= 10000


def collateral_type_valid(record, collateral_types):
    collateral_type = record['collateral_type']
    assert collateral_type in collateral_types


def haircut_valid(record):
    collateral_type = record['collateral_type']
    haircut = record['haircut']
    if collateral_type == 'Non Cash':
        assert haircut == '2.00%'
    else:
        assert haircut is None


def collateral_margin_valid(record):
    collateral_type = record['collateral_type']
    collateral_margin = record['collateral_margin']
    if collateral_type == 'Cash':
        assert collateral_margin == '140.00%'
    else:
        assert collateral_margin is None


def rebate_rate_valid(record):
    collateral_type = record['collateral_type']
    rebate_rate = record['rebate_rate']
    if collateral_type == 'Cash':
        assert rebate_rate == '5.75%'
    else:
        assert rebate_rate is None


def borrow_fee_valid(record):
    collateral_type = record['collateral_type']
    borrow_fee = record['borrow_fee']
    if collateral_type == 'Non Cash':
        assert borrow_fee == '4.00%'
    else:
        assert borrow_fee is None


def is_callable_valid(record):
    assert record['is_callable'] in [True, False]


def return_type_valid(record, return_types):
    return_type = record['return_type']
    assert return_type in return_types
