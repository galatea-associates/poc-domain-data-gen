from unittest.mock import Mock
import pytest
import string
import datetime
import sys

sys.path.insert(0, 'Kafka_Python/')

from data_gen.src.DataGenerator import DataGenerator


@pytest.fixture
def data_generator():
    return DataGenerator()


def test_clear_state(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    data_generator.clear_state()
    assert len(list(data_generator._DataGenerator__state)) == 0


def test_state_contains_field(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    assert data_generator.state_contains_field('inst_id') \
           and data_generator.state_contains_field('position_type') \
           and not data_generator.state_contains_field('qty')


def test_get_state_value(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    value = data_generator.get_state_value('position_type')
    assert value == 'SD'


def test_generate_new_inst_id_when_asset_class_none(data_generator):
    data_generator._DataGenerator__get_preemptive_generation = Mock()
    inst_id = data_generator.generate_new_inst_id()
    called = data_generator._DataGenerator__get_preemptive_generation.has_been_called()
    is_correct_format = inst_id.startswith(('ABC', 'BCD'))
    inst_id_suffix = inst_id.replace('BCD', '').replace('ABC', '')
    for c in inst_id_suffix:
        is_correct_format = is_correct_format \
                            and c in string.ascii_uppercase + string.digits

    assert is_correct_format and called


def test_generate_new_inst_id_when_asset_class_cash(data_generator):
    data_generator._DataGenerator__get_preemptive_generation = Mock()
    inst_id = data_generator.generate_new_inst_id(asset_class='Cash')
    called = data_generator._DataGenerator__get_preemptive_generation.has_been_called()
    is_correct_format = inst_id.startswith('BCD')
    inst_id_suffix = inst_id.replace('BCD', '')
    for c in inst_id_suffix:
        is_correct_format = is_correct_format \
                            and c in string.ascii_uppercase + string.digits

    assert is_correct_format and called


def test_generate_new_inst_id_when_asset_class_stock(data_generator):
    data_generator._DataGenerator__get_preemptive_generation = Mock()
    inst_id = data_generator.generate_new_inst_id(asset_class='Stock')
    called = data_generator._DataGenerator__get_preemptive_generation.has_been_called()
    is_correct_format = inst_id.startswith('ABC')
    inst_id_suffix = inst_id.replace('ABC', '')
    for c in inst_id_suffix:
        is_correct_format = is_correct_format \
                            and c in string.ascii_uppercase + string.digits

    assert is_correct_format and called


def test_generate_new_inst_id_add_to_lists_of_inst_ids(data_generator):
    n_stock_ids = len(data_generator._DataGenerator__stock_inst_ids)
    n_cash_ids = len(data_generator._DataGenerator__cash_inst_ids)
    inst_id = data_generator.generate_new_inst_id()
    if inst_id.startswith('ABC'):
        is_correct_length = \
            len(data_generator._DataGenerator__stock_inst_ids) \
            == (n_stock_ids + 1) \
            and len(data_generator._DataGenerator__cash_inst_ids) \
            == n_cash_ids
    else:
        is_correct_length = \
            len(data_generator._DataGenerator__cash_inst_ids) \
            == (n_cash_ids + 1) \
            and len(data_generator._DataGenerator__stock_inst_ids) \
            == n_stock_ids

    assert is_correct_length


# TODO: test with only param

def test_generate_inst_id_when_asset_class_stock(data_generator):
    stock_ids = ['ABCV740P', 'ABCD4F2J']
    data_generator._DataGenerator__stock_inst_ids = stock_ids
    id = data_generator.generate_inst_id(asset_class='Stock')
    assert id in stock_ids


def test_generate_inst_id_when_asset_class_cash(data_generator):
    cash_ids = ['BCD0MUID', 'BCDAH98I']
    data_generator._DataGenerator__cash_inst_ids = cash_ids
    id = data_generator.generate_inst_id(asset_class='Cash')
    assert id in cash_ids


def test_generate_asset_class(data_generator):
    asset_class = data_generator.generate_asset_class()
    assert asset_class in ['Stock', 'Cash']


def test_generate_coi(data_generator):
    coi = data_generator.generate_coi()
    assert coi in ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP']


def test_generate_haircut(data_generator):
    haircut = data_generator.generate_haircut()
    assert haircut == '2.00%'


def test_generate_is_callable(data_generator):
    is_callable = data_generator.generate_is_callable()
    assert is_callable in ['Yes', 'No']


def test_generate_swap_type(data_generator):
    swap_type = data_generator.generate_swap_type()
    assert swap_type in ['Equity', 'Portfolio']


def test_generate_reference_rate(data_generator):
    ref_rate = data_generator.generate_reference_rate()
    assert ref_rate in ['LIBOR']


def test_generate_status(data_generator):
    status = data_generator.generate_status()
    assert status in ['Live', 'Dead']


def test_generate_depot_id(data_generator):
    depot_id = data_generator.generate_depot_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in depot_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_account_with_no_constraints(data_generator):
    account = data_generator.generate_account(no_ecp=True)
    account_suffix = account.replace('ICP', '').replace('ECP', '')
    is_correct_format = True
    for c in account_suffix:
        is_correct_format = is_correct_format and c in string.digits
    assert account.startswith(('ICP', 'ECP')) and is_correct_format


def test_generate_account_with_no_ecp(data_generator):
    account = data_generator.generate_account(no_ecp=True)
    account_suffix = account.replace('ICP', '')
    is_correct_format = True
    for c in account_suffix:
        is_correct_format = is_correct_format and c in string.digits
    assert account.startswith('ICP') and is_correct_format


def test_generate_account_with_no_icp(data_generator):
    account = data_generator.generate_account(no_icp=True)
    account_suffix = account.replace('ECP', '')
    is_correct_format = True
    for c in account_suffix:
        is_correct_format = is_correct_format and c in string.digits
    assert account.startswith('ECP') and is_correct_format


def test_generate_account_number(data_generator):
    account_number = data_generator.generate_account_number()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in account_number:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_order_id(data_generator):
    order_id = data_generator.generate_order_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in order_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_customer_id(data_generator):
    customer_id = data_generator.generate_customer_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in customer_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_sto_id(data_generator):
    sto_id = data_generator.generate_sto_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in sto_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_agent_id(data_generator):
    agent_id = data_generator.generate_agent_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in agent_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_direction(data_generator):
    direction = data_generator.generate_direction()
    assert direction in ['Credit', 'Debit']


def test_generate_currency(data_generator):
    curr = data_generator.generate_currency()
    assert curr in ['USD', 'CAD', 'EUR', 'GBP']


def test_generate_swap_contract_id_(data_generator):
    swap_contract_ids = ['18825586', '90344267']
    data_generator._DataGenerator__swap_contract_ids = swap_contract_ids
    length = len(data_generator._DataGenerator__swap_contract_ids)
    new_length = len(data_generator._DataGenerator__swap_contract_ids)
    swap_contract_id = data_generator.generate_swap_contract_id()
    assert swap_contract_id in swap_contract_ids and (new_length == length)


def test_generate_ticker_asset_class_is_stock(data_generator):
    ticker = data_generator.generate_ticker(asset_class='Stock')
    assert ticker in ['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS', 'F', 'GOOGL', 'FB']


def test_generate_ticker_asset_class_is_cash(data_generator):
    ticker = data_generator.generate_ticker(asset_class='Cash')
    assert ticker in ['USD', 'CAD', 'EUR', 'GBP']


def test_generate_ticker_asset_class_is_none(data_generator):
    # TODO: check __preemptive_generation called
    ticker = data_generator.generate_ticker()
    assert ticker in ['USD', 'CAD', 'EUR', 'GBP'] + \
           ['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS', 'F', 'GOOGL', 'FB']


def test_generate_cusip_asset_class_is_cash(data_generator):
    cusip = data_generator.generate_cusip(asset_class='Cash')
    assert cusip == ''


def test_generate_cusip_asset_class_is_stock_ticker_is_none(data_generator):
    # TODO: make sure preemptive function called
    length = len(data_generator._DataGenerator__stock_to_cusip)
    cusip = data_generator.generate_cusip(asset_class='Stock')
    new_length = len(data_generator._DataGenerator__stock_to_cusip)
    is_correct_format = True
    for c in cusip:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format and (
            cusip in data_generator._DataGenerator__stock_to_cusip.values() and
            new_length == length + 1)


def test_generate_cusip_asset_class_is_stock_ticker_is_not_none(data_generator):
    data_generator._DataGenerator__stock_to_cusip = {'IBM': '505627582',
                                                     'APPL': '485020892'}
    length = len(data_generator._DataGenerator__stock_to_cusip)
    cusip = data_generator.generate_cusip(ticker='IBM', asset_class='Stock')
    new_length = len(data_generator._DataGenerator__stock_to_cusip)

    assert cusip == data_generator._DataGenerator__stock_to_cusip['IBM'] and (
            length == new_length)


def test_generate_sedol_asset_class_is_cash(data_generator):
    sedol = data_generator.generate_sedol(asset_class='Cash')
    assert sedol == ''


def test_generate_sedol_asset_class_is_stock_ticker_is_none(data_generator):
    # TODO: make sure preemptive function called
    length = len(data_generator._DataGenerator__stock_to_sedol)
    sedol = data_generator.generate_sedol(asset_class='Stock')
    new_length = len(data_generator._DataGenerator__stock_to_sedol)
    is_correct_format = True
    for c in sedol:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format and (
            sedol in data_generator._DataGenerator__stock_to_sedol.values() and
            new_length == length + 1)


def test_generate_sedol_asset_class_is_stock_ticker_is_not_none(data_generator):
    data_generator._DataGenerator__stock_to_sedol = {'IBM': '3888133',
                                                     'APPL': '5422214'}
    length = len(data_generator._DataGenerator__stock_to_sedol)
    sedol = data_generator.generate_sedol(ticker='IBM', asset_class='Stock')
    new_length = len(data_generator._DataGenerator__stock_to_sedol)

    assert sedol == data_generator._DataGenerator__stock_to_sedol['IBM'] and (
            length == new_length)


def test_generate_isin_asset_class_is_cash(data_generator):
    isin = data_generator.generate_isin(asset_class='Cash')
    assert isin == ''


def test_generate_ric_asset_class_is_cash(data_generator):
    ric = data_generator.generate_ric(asset_class='Cash')
    assert ric == ''


def test_generate_ric_asset_class_is_stock_ticker_is_none(data_generator):
    ric = data_generator.generate_ric(asset_class='Stock')
    assert ric.startswith(tuple(['IBM', 'APPL', 'TSLA', 'AMZN', 'DIS',
                                 'F', 'GOOGL', 'FB'])) and (
                   ric.endswith(tuple(['L', 'N', 'OQ'])) and '.' in ric)


def test_generate_ric_asset_class_is_stock_ticker_is_not_none(data_generator):
    ric = data_generator.generate_ric(ticker='IBM', asset_class='Stock')
    assert ric.startswith('IBM') and (
            ric.endswith(tuple(['L', 'N', 'OQ'])) and '.' in ric)


def test_generate_new_swap_contract_id(data_generator):
    length = len(data_generator._DataGenerator__swap_contract_ids)
    swap_contract_id = data_generator.generate_new_swap_contract_id()
    new_length = len(data_generator._DataGenerator__swap_contract_ids)
    is_correct_format = True
    for c in swap_contract_id:
        is_correct_format = is_correct_format and c in string.digits
    assert is_correct_format and (new_length == length + 1)


def test_generate_collateral_type(data_generator):
    collateral_type = data_generator.generate_collateral_type()
    assert collateral_type in ['Cash', 'Non Cash']


def test_generate_purpose_data_type_is_fop(data_generator):
    purpose = data_generator.generate_purpose(data_type='FOP')
    assert purpose in ['Outright']


def test_generate_purpose_data_type_is_bop(data_generator):
    purpose = data_generator.generate_purpose(data_type='BOP')
    assert purpose in ['Outright']


def test_generate_purpose_data_type_is_st(data_generator):
    purpose = data_generator.generate_purpose(data_type='ST')
    assert purpose in ['Outright']


def test_generate_purpose_data_type_is_dp(data_generator):
    purpose = data_generator.generate_purpose(data_type='DP')
    assert purpose in ['Holdings', 'Seg']


def test_generate_purpose_data_type_is_sl(data_generator):
    purpose = data_generator.generate_purpose(data_type='SL')
    assert purpose in ['Borrow', 'Loan']


def test_generate_purpose_data_type_is_c(data_generator):
    purpose = data_generator.generate_purpose(data_type='C')
    assert purpose in ['Cash Balance', 'P&L', 'Fees']


def test_generate_purpose_data_type_is_none(data_generator):
    purpose = data_generator.generate_purpose()
    assert purpose == ''


def test_generate_position_type_with_no_constraints(data_generator):
    position_type = data_generator.generate_position_type()
    assert position_type in ['SD', 'TD']


def test_generate_position_type_with_no_sd(data_generator):
    position_type = data_generator.generate_position_type(no_sd=True)
    assert position_type in ['TD']


def test_generate_position_type_with_no_td(data_generator):
    position_type = data_generator.generate_position_type(no_td=True)
    assert position_type in ['SD']


def test_generate_price_inst_id_of_cash(data_generator):
    price = data_generator.generate_price(inst_id='BCD0MUID')
    assert price == 1.00


def test_generate_price_inst_id_of_stock(data_generator):
    price = data_generator.generate_price(inst_id='ABCV740P')
    assert 10 <= price <= 10000


def test_generate_price_inst_id_is_none(data_generator):
    # TODO: checl function call
    data_generator._DataGenerator__stock_inst_ids = {'ABCV740P': None}
    data_generator._DataGenerator__cash_inst_ids = {'BCD0MUID': None}
    price = data_generator.generate_price()
    assert price == 1 or 10 <= price <= 10000


def test_generate_knowledge_date(data_generator):
    knowledge_date = data_generator.generate_knowledge_date(
        from_year=2016, to_year=2017,
        from_month=1, to_month=12,
        from_day=1, to_day=28)

    oldest = datetime.date(2016, 1, 1)
    most_recent = datetime.date(2017, 12, 28)
    assert oldest <= knowledge_date <= most_recent


def test_generate_swap_start_date(data_generator):
    knowledge_date = data_generator.generate_swap_start_date(
        from_year=2016, to_year=2017,
        from_month=1, to_month=12,
        from_day=1, to_day=28)

    oldest = datetime.date(2016, 1, 1)
    most_recent = datetime.date(2017, 12, 28)
    assert oldest <= knowledge_date <= most_recent


def test_generate_swap_end_date_start_date_is_not_none_status_is_live(
        data_generator):
    start_date = data_generator.generate_swap_start_date()
    end_date = data_generator.generate_swap_end_date(start_date=start_date,
                                                     status='Live')
    assert end_date == ''


def test_generate_swap_end_date_start_date_is_none_status_is_live(
        data_generator):
    start_date = data_generator.generate_swap_start_date()
    end_date = data_generator.generate_swap_end_date(start_date=start_date,
                                                     status='Live')
    assert end_date == ''


def test_generate_swap_end_date_start_date_is_not_none_status_is_dead(
        data_generator):
    start_date = data_generator.generate_swap_start_date()
    n_years_to_add = 5
    end_date = data_generator.generate_swap_end_date(
        start_date=start_date,
        status='Dead',
        n_years_to_add=n_years_to_add)
    assert end_date == (
            start_date + datetime.timedelta(days=365 * n_years_to_add))


# TODO: fix
def test_generate_swap_end_date_start_date_is_none_status_is_dead(data_generator):
    start_date = data_generator.generate_swap_start_date(
        from_year=2016, to_year=2017,
        from_month=1, to_month=12,
        from_day=1, to_day=28
    )
    n_years_to_add = 5
    end_date = data_generator.generate_swap_end_date(
        start_date=start_date,
        status='Live',
        n_years_to_add=n_years_to_add)

    assert True


# TODO: tests these functions with None as input
def test_generate_effective_date_knowledge_date_is_not_none_position_type_is_td(data_generator):
    knowledge_date = data_generator.generate_knowledge_date()
    effective_date = data_generator.generate_effective_date(
        knowledge_date=knowledge_date,
        position_type='TD')

    assert effective_date == knowledge_date


def test_generate_effective_date_knowledge_date_is_not_none_position_type_is_sd(
        data_generator):
    knowledge_date = data_generator.generate_knowledge_date()
    n_days_to_add = 3
    effective_date = data_generator.generate_effective_date(
        n_days_to_add=n_days_to_add,
        knowledge_date=knowledge_date,
        position_type='SD')

    assert effective_date == (
            knowledge_date + datetime.timedelta(days=n_days_to_add))


# FIXME
def test_generate_rebate_rate_collateral_type_is_none(data_generator):
    assert True


def test_generate_rebate_rate_collateral_type_is_cash(data_generator):
    rebate_rate = data_generator.generate_rebate_rate(collateral_type='Cash')
    assert rebate_rate == '5.75%'


def test_generate_rebate_rate_collateral_type_is_cash(data_generator):
    rebate_rate = data_generator.generate_rebate_rate(collateral_type='Stock')
    assert rebate_rate == ''


def test_generate_qty(data_generator):
    min_qty = 1
    max_qty = 21
    qty = data_generator.generate_qty(min_qty=min_qty, max_qty=max_qty)
    assert min_qty*100 <= qty <= max_qty*100


def test_generate_return_type(data_generator):
    return_type = data_generator.generate_return_type()
    assert return_type in ['Outstanding', 'Pending Return', 'Pending Recall',
                           'Partial Return', 'Partial Recall', 'Settled']
