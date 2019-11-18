import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_swap_contracts():
    pass  # TODO: implement after variable generation
    """
    records, domain_obj = helper.set_up_swap_contract_tests()
    for record in records:
        shared.attribute_quantity_valid('swap_contract', record, 11)
        shared.attribute_exists(record['counterparty_id'],
                                'id', 'counterparties')
        uuid_valid(record)
        swap_mnemonic_valid(record)
        is_short_mtm_financed_valid(record)
        accounting_area_valid(record)
        status_valid(record)
        # start_date_valid(record)
        # ABOVE: Random date from a range of potential start dates
        # end_date_valid(record)
        # ABOVE: Five years on from the chosen start date
        swap_type_valid(record, domain_obj.SWAP_TYPES)
        reference_rate_valid(record, domain_obj.REFERENCE_RATES)
        shared.dummy_fields_valid(record, 'swap_contract')
    """


def uuid_valid(record):
    uuid = record['swap_contract_id']
    assert shared.is_length(36, uuid)


def swap_mnemonic_valid(record):
    mnemonic = record['swap_mnemonic']
    assert shared.is_length(10, mnemonic)


def is_short_mtm_financed_valid(record):
    value = record['is_short_mtm_financed']
    assert value in [True, False]


def accounting_area_valid(record):
    accounting_area = record['accounting_area']
    assert shared.is_length(10, accounting_area)


def status_valid(record):
    status = record['status']
    assert status in ['Live', 'Dead']


def swap_type_valid(record, swap_types):
    swap_type = record['swap_type']
    assert swap_type in swap_types


def reference_rate_valid(record, reference_rates):
    reference_rate = record['reference_rate']
    assert reference_rate in reference_rates
