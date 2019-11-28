import random
from datetime import datetime, timezone, timedelta

from domainobjectfactories.creatable import Creatable


class TradeFactory(Creatable):
    """ Class to create trades. Create method will create a
    set amount of executions. """

    TRADE_LEGS = ["EMPTY", "1", "2"]
    DIRECTIONS = ["BUY", "SELL"]

    def create(self, record_count, start_id):
        """ Create a set number of trades

        Parameters
        ----------
        record_count : int
            Number of order executions to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' order executions
        """

        records = []

        for i in range(start_id, start_id+record_count):
            records.append(self.create_record(i))

        return records

    def create_record(self, id):
        """ Create a single trade

        Parameters
        ----------
        id : int
            ID of this creation

        Returns
        -------
        dict
            A single trade object
        """

        booking_datetime, trade_datetime, value_datetime = \
            self.__create_trade_lifecycle_dates()
        isin, market = self.__get_instrument_details()
        quantity = self.__create_quantity()

        record = {
            'trade_id': id,
            'contract_id': self.__create_contract_id(),
            'booking_datetime': booking_datetime,
            'trade_datetime': trade_datetime,
            'value_datetime': value_datetime,
            'order_id': self.__create_order_id(),
            'account_id': self.__get_account_id(),
            'counterparty_id': self.__get_counterparty_id(),
            'trader_id': self.__create_trader_id(),
            'price': self.__create_price(quantity),
            'currency': self.create_currency(),
            'isin': isin,
            'market': market,
            'trade_leg': self.__create_trade_leg(),
            'is_otc': self.create_random_boolean(),
            'direction': self.__create_direction(),
            'quantity': quantity,
            'created_timestamp': self.__create_created_timestamp()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def __get_instrument_details(self):
        instrument = self.get_random_instrument()
        isin = instrument['isin']
        market = instrument['market']
        return isin, market

    def __create_contract_id(self):
        return self.create_random_string(10)

    @staticmethod
    def __create_trade_lifecycle_dates():
        booking_datetime = trade_datetime = datetime.now(timezone.utc)
        day_after_tomorrow = datetime.now(timezone.utc) + timedelta(days=2)
        value_datetime = day_after_tomorrow.replace(
            hour=0, minute=1, second=0, microsecond=0
        )
        return booking_datetime, trade_datetime, value_datetime

    def __create_order_id(self):
        return self.create_random_integer()

    def __get_account_id(self):
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Counterparty', 'Depot']
        )
        return account['account_id']

    def __get_counterparty_id(self):
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Client', 'Firm', 'Depot']
        )
        return account['account_id']

    def __create_trader_id(self):
        return self.create_random_string(10)

    def __create_price(self, quantity):
        unit_price = self.create_random_decimal()
        return round(unit_price * quantity, 2)

    def __create_trade_leg(self):
        return random.choice(self.TRADE_LEGS)

    def __create_direction(self):
        return random.choice(self.DIRECTIONS)

    def __create_quantity(self):
        return self.create_random_integer()

    @staticmethod
    def __create_created_timestamp():
        return datetime.now(timezone.utc)
