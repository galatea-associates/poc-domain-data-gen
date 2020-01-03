from generators.generator import Generator
from datetime import datetime, timezone, timedelta
from random import choice, randint


class CashBalanceGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        account_row = cls.__get_account_row(database)
        as_of_date = choice(
            (
                datetime.now(timezone.utc).date(),
                datetime.now(timezone.utc).date() + timedelta(days=2)
            )
        )
        amount = randint(1, 10000) * choice((-1, 1))
        currency = choice(('USD', 'CAD', 'EUR', 'GBP', 'CHF', 'JPY', 'SGD'))
        account_id = account_row[0]
        account_owner = account_row[1]
        purpose = choice(
            (
                "Cash Balance",
                "P&L",
                "Fees",
                "Collateral Posted",
                "Collateral Received"
            )
        )
        record = {
            'as_of_date': as_of_date,
            'amount': amount,
            'currency': currency,
            'account_id': account_id,
            'account_owner': account_owner,
            'purpose': purpose
        }
        return record

    @classmethod
    def __get_account_row(cls, database):
        query = "SELECT account_id, account_type FROM accounts WHERE " + \
                "account_type IN ('Client', 'Firm') ORDER BY RANDOM() LIMIT 1"
        account_row = database.execute_query(query)
        return account_row



