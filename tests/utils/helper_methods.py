import os
import sys
import ujson

sys.path.insert(0, 'src/')
from database.sqlite_database import Sqlite_Database
from domainobjects import back_office_position_factory, cash_balance_factory, cashflow_factory
from domainobjects import counterparty_factory, depot_position_factory, front_office_position_factory
from domainobjects import instrument_factory, order_execution_factory, price_factory
from domainobjects import stock_loan_position_factory, swap_contract_factory, swap_position_factory


# Helper Methods
def delete_local_database():
    if os.path.exists('dependencies.db'):
        os.remove('dependencies.db')


def get_configuration():
    file_path = 'src/config.json'
    with open(file_path, 'r+') as file:
        return ujson.load(file)


def create_db():
    return Sqlite_Database()


def create_test_table(database, table_name, attribute_dict):
    database.create_table_from_dict(table_name, attribute_dict)


def drop_test_table(database, table_name):
    database.get_connection().execute("DROP TABLE IF EXISTS " + table_name)


def query_db(table_name, attribute=None):
    db = Sqlite_Database()
    result = db.retrieve(table_name)
    if attribute is not None:
        returning = [row[attribute] for row in result]
        return returning
    else:
        return result


# Generation Methods
def generate_back_office_position(amount=1):
    obj = back_office_position_factory.BackOfficePositionFactory(None, None)
    return obj.generate(amount, 0)


def generate_cash_balance(amount=1):
    obj = cash_balance_factory.CashBalanceFactory(None, None)
    return obj.generate(amount, 0)


def generate_cashflow(amount=1):
    config = get_configuration()
    cashflow_config = config['domain_objects'][11]
    obj = cashflow_factory.CashflowFactory(cashflow_config)
    return obj.generate(amount, 0)


def generate_counterparty(amount=1):
    obj = counterparty_factory.CounterpartyFactory(None, None)
    return obj.generate(amount, 0)


def generate_depot_position(amount=1):
    obj = depot_position_factory.DepotPositionFactory(None, None)
    return obj.generate(amount, 0)


def generate_front_office_position(amount=1):
    obj = front_office_position_factory.FrontOfficePositionFactory(None, None)
    return obj.generate(amount, 0)


def generate_instrument(amount=1):
    obj = instrument_factory.InstrumentFactory(None, None)
    return obj.generate(amount, 0)


def generate_order_execution(amount=1):
    obj = order_execution_factory.OrderExecutionFactory(None, None)
    return obj.generate(amount, 0)


def generate_price(amount=1):
    obj = price_factory.PriceFactory(None, None)
    return obj.generate(amount, 0)


def generate_stock_loan_position(amount=1):
    obj = stock_loan_position_factory.StockLoanPositionFactory(None, None)
    return obj.generate(amount, 0)


def generate_swap_contract(amount=1):
    config = get_configuration()
    swap_contract_config = config['domain_objects'][9]
    obj = swap_contract_factory.SwapContractFactory(swap_contract_config, None)
    return obj.generate(amount, 0)


def generate_swap_position(amount=1):
    config = get_configuration()
    swap_position_config = config['domain_objects'][10]
    obj = swap_position_factory.SwapPositionFactory(swap_position_config, None)
    return obj.generate(amount, 0)


# Set-up Methods
def set_up_back_office_position_tests():
    delete_local_database()
    generate_instrument(50)
    records = generate_back_office_position(50)
    domain_obj = back_office_position_factory.BackOfficePositionFactory(None, None)
    return records, domain_obj


def set_up_cash_balance_tests():
    domain_obj = cash_balance_factory.CashBalanceFactory(None, None)
    records = generate_cash_balance(50)
    return records, domain_obj


def set_up_cashflow_tests():
    delete_local_database()
    generate_instrument(50)
    generate_counterparty(20)
    generate_swap_contract(20)
    generate_swap_position(40)
    return generate_cashflow(20)


def set_up_counterparty_tests():
    return generate_counterparty(50)


def set_up_depot_position_tests():
    delete_local_database()
    generate_instrument(50)
    records = generate_depot_position(50)
    domain_obj = depot_position_factory.DepotPositionFactory(None, None)
    return records, domain_obj


def set_up_front_office_position_tests():
    delete_local_database()
    generate_instrument(50)
    records = generate_front_office_position(50)
    domain_obj = front_office_position_factory.FrontOfficePositionFactory(None, None)
    return records, domain_obj


def set_up_instrument_tests():
    delete_local_database()
    return generate_instrument(50)


def set_up_order_execution_tests():
    delete_local_database()
    generate_instrument(50)
    return generate_order_execution(50)


def set_up_price_tests():
    delete_local_database()
    generate_instrument(50)
    return generate_price(50)


def set_up_stock_loan_position_tests():
    delete_local_database()
    generate_instrument(50)
    records = generate_stock_loan_position(50)
    domain_obj = stock_loan_position_factory.StockLoanPositionFactory(None, None)
    return records, domain_obj


def set_up_swap_contract_tests():
    delete_local_database()
    generate_counterparty(20)
    records = generate_swap_contract(20)
    domain_obj = swap_contract_factory.SwapContractFactory(None, None)
    return records, domain_obj


def set_up_swap_position_tests():
    generate_instrument(50)
    generate_counterparty(20)
    generate_swap_contract(20)
    records = generate_swap_position(50)
    domain_obj = swap_position_factory.SwapPositionFactory(None, None)
    return records, domain_obj
