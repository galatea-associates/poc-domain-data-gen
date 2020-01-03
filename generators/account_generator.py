from generators.generator import Generator
from random import choice, choices, randint, getrandbits
from string import ascii_uppercase, digits
from datetime import datetime, timezone, timedelta


class AccountGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        batch = []
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            batch.append(
                {
                    key: record[key]
                    for key in {"account_id", "account_type", "iban"}
                }
            )
            if len(batch) == min(1000, quantity):
                cls.__persist_batch(database, batch, lock)
                batch = []
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        account_id = start_id + record_number
        account_type = choice(("Client", "Firm", "Counterparty", "Depot"))
        account_purpose = choice(
            ('Fully Paid', 'Financed', 'Stock Loan', 'Rehypo', 'Collateral')
        )
        account_description = "".join(choices(ascii_uppercase + digits, k=10))
        account_status = choice(('Open', 'Closed'))
        iban = cls.__get_iban()
        account_set_id = "".join(choices(ascii_uppercase + digits, k=10))
        legal_entity_set_id = "".join(choices(ascii_uppercase + digits, k=10))
        opening_date = (
                datetime(2016, 1, 1).date() +
                timedelta(
                    days=randint(
                        0,
                        (datetime.now(timezone.utc).date() -
                         datetime(2016, 1, 1).date()).days
                    )
                )
        ).strftime('%Y%m%d')
        closing_date = (
            "Empty",
            (
                    datetime.strptime(opening_date, "%Y%m%d").date() +
                    timedelta(
                        days=randint(
                            0,
                            (
                                    datetime.now(timezone.utc).date() -
                                    datetime.strptime(
                                        opening_date, "%Y%m%d"
                                    ).date()
                            ).days
                        )
                    )
            ).strftime('%Y%m%d')
        )[getrandbits(1)]
        record = {
            "account_id": account_id,
            "account_type": account_type,
            "account_purpose": account_purpose,
            "account_description": account_description,
            "account_status": account_status,
            "iban": iban,
            "account_set_id": account_set_id,
            "legal_entity_id": legal_entity_set_id,
            "opening_date": opening_date,
            "closing_date": closing_date
        }
        return record

    @classmethod
    def __persist_batch(cls, database, batch, lock):
        lock.acquire()
        for record in batch:
            cls.__persist_record(database, record)
        database.commit()
        lock.release()

    @staticmethod
    def __persist_record(database, record):
        account_id = record["account_id"]
        account_type = record["account_type"]
        iban = record["iban"]
        query = "INSERT INTO accounts " + \
                "(account_id, account_type, iban) VALUES " + \
                f"('{account_id}', '{account_type}', '{iban}')"
        database.execute_query(query)

    @staticmethod
    def __get_iban():
        country = choice(('GB', 'CH', 'FR', 'DE', 'SA'))
        check_digits = str(randint(10, 99))
        if country == 'GB':
            bban = "".join(choices(ascii_uppercase, k=4)) + str(
                randint(1000000000000, 99999999999999)
            )
        elif country == 'CH':
            bban = str(randint(1000000000000000, 99999999999999999))
        elif country == 'FR':
            bban = str(randint(1000000000000000000, 99999999999999999999)) +\
                   choice(ascii_uppercase) + str(randint(10, 99))
        elif country == 'DE':
            bban = str(randint(10000000000000000, 999999999999999999))
        elif country == 'SA':
            bban = str(randint(1000000000000000000, 99999999999999999999))
        return country + check_digits + bban
