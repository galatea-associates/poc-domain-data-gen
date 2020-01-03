from generators.generator import Generator
from random import randint, choice, choices
from string import ascii_uppercase, digits
from itertools import combinations
from datetime import datetime, timezone


class InstrumentGenerator(Generator):

    @classmethod
    def instantiate_generator(cls, quantity, database, lock, start_id):
        batch = []
        for record_number in range(quantity):
            record = cls.__get_record(start_id, record_number, database)
            batch.append(
                {
                    key: record[key]
                    for key in {"instrument_id", "cusip", "isin", "market"}
                }
            )
            if len(batch) == min(5000, quantity):
                cls.__persist_batch(database, batch, lock)
                batch = []
            yield record

    @classmethod
    def __get_record(cls, start_id, record_number, database=None):
        instrument_id = start_id + record_number
        ticker = database.get_random_value("tickers", "symbol")
        random_exchanges_row = database.get_random_value("exchanges")
        country_of_issuance = random_exchanges_row[0]
        exchange_code = random_exchanges_row[1]
        ric = f"{ticker}.{exchange_code}"
        cusip = randint(100000000, 999999999)
        isin = f"{country_of_issuance}{cusip}4"
        sedol = randint(1000000, 9999999)
        valoren = randint(100000, 999999999)
        quick = randint(1000, 9999)
        sicovam = randint(100000, 999999)
        asset_class = choice(("Equity", "Fund", "Derivative"))
        asset_subclass = choice(
            {
                'Equity': ('Common', 'Preferred'),
                'Fund': ('ETF', 'Mutual Fund'),
                'Derivative': ('Right', 'Warrant')
            }[asset_class]
        )
        primary_market = database.get_random_value(
            "exchanges", "exchange_code"
        )
        market = database.get_random_value(
            "exchanges", "exchange_code"
        )
        is_primary_listing = primary_market == market
        figi = cls.__get_figi()
        issuer_name = "".join(choices(ascii_uppercase + digits, k=16))
        industry_classification = choice(
            ('MANUFACTURING', 'TELECOMS', 'FINANCIAL SERVICES', 'GROCERIES')
        )
        created_timestamp = datetime.now(timezone.utc)
        last_updated_timestamp = datetime.now(timezone.utc)
        record = {
            'instrument_id': instrument_id,
            'ric': ric,
            'isin': isin,
            'sedol': sedol,
            'ticker': ticker,
            'cusip': cusip,
            'valoren': valoren,
            'quick': quick,
            'sicovam': sicovam,
            'asset_class': asset_class,
            'asset_subclass': asset_subclass,
            'country_of_issuance': country_of_issuance,
            'primary_market': primary_market,
            'market': market,
            'is_primary_listing': is_primary_listing,
            'figi': figi,
            'issuer_name': issuer_name,
            'industry_classification': industry_classification,
            'created_timestamp': created_timestamp,
            'last_updated_time_stamp': last_updated_timestamp
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
        instrument_id = record["instrument_id"]
        cusip = record["cusip"]
        isin = record["isin"]
        market = record["market"]
        query = "INSERT INTO instruments " + \
                "(instrument_id, cusip, isin, market) VALUES " + \
                f"('{instrument_id}', '{cusip}', '{isin}', '{market}')"
        database.execute_query(query)

    @staticmethod
    def __get_figi():
        consonants = "BCDFGHJKLMNPQRSTUVWYZ"
        consonants_and_digits = "BCDFGHJKLMNPQRSTUVWYZ123456789"
        invalid_combinations = {'BS', 'BM', 'GG', 'GB', 'GH', 'KY', 'VG'}
        # consonants is concatenated to itself to ensure same-character
        # combinations are created eg. 'BB', 'GG' etc
        valid_combinations = {
            "".join(combination)
            for combination in combinations(2 * consonants, 2)
            if "".join(combination) not in invalid_combinations
        }

        start = choice(list(valid_combinations))
        middle = "".join(choices(consonants_and_digits, k=8))
        end = choice(range(10))

        return f"{start}G{middle}{end}"

