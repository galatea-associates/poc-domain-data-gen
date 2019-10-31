import sys

sys.path.insert(0, 'tests/')
from test_domain_objects import helper_methods as helper
from test_domain_objects import shared_tests as shared


def test_populate_exchange_table():
    table_name = "exchanges"
    database = helper.create_db()

    database_rows = database.retrieve(table_name)
    rows = []
    for row in database_rows:
        rows.append([row['country_of_issuance'], row['exchange_code'],
                     row['currency']])

    expected_rows = [['US', 'DI', 'USD'], ['GB', 'LN', 'GBP'],
                     ['CA', 'TS', 'CAD'], ['FR', 'GEX', 'EUR'],
                     ['DE', 'FF', 'EUR'], ['CH', 'SWX', 'CHF'],
                     ['SG', 'SG', 'SGD'], ['JP', 'TO', 'JPY']]

    row_count = database.get_table_size(table_name)
    expected_row_count = 8

    shared.actual_contains_expected(expected_rows, rows)
    shared.expected_value(expected_row_count, row_count)


def test_populate_tickers_table():
    table_name = "tickers"
    database = helper.create_db()

    database_rows = database.retrieve(table_name)
    rows = []
    for row in database_rows:
        rows.append(row['symbol'])

    expected_rows = ['YI', 'PIH', 'PIHPP', 'TURN', 'FLWS']

    row_count = database.get_table_size(table_name)
    expected_row_count = 3434

    shared.actual_contains_expected(expected_rows, rows)
    shared.expected_value(expected_row_count, row_count)
