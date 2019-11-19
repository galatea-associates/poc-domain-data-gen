import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_cashflows():
    """ Ensure all generated cashflow attributes adhere to their
    specification. Dependent on Swap Positions """
    pass  # TODO: implement after variable generation
    """
    records = helper.set_up_cashflow_tests()
    for record in records:
        shared.attribute_quantity_valid('cashflow', record, 8)
        shared.swap_contract_id_exists(record)
        shared.ric_exists(record)
        cashflow_type_exists(record)
        # pay_date_valid(record)
        effective_date_exists(record)
        shared.currency_valid(record)
        shared.amount_valid(record)
        shared.long_short_valid(record)
    """


def effective_date_exists(record):
    formatted_effective_date = record['effective_date'].strftime("%Y-%m-%d")
    shared.attribute_exists(formatted_effective_date,
                            'effective_date', 'swap_positions')


def pay_date_valid(record):
    """ TODO: Confirm test implementation approach """


def cashflow_type_exists(record):
    cashflow_types = []
    config = helper.get_configuration()
    cashflow_config = config['domain_objects'][11]
    cashflow_args = cashflow_config['custom_args']['cashflow_generation']
    for arg in cashflow_args:
        cashflow_types.append(arg['cashFlowType'])
    cashflow_type = record['cashflow_type']
    assert cashflow_type in cashflow_types
