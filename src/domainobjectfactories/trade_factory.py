import random
import datetime

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
        isin, market, unit_price = self.__create_instrument_details()
        quantity = self.__create_quantity()

        record = {
            'trade_id': id,
            'contract_id': self.__create_contract_id(),
            'booking_datetime': booking_datetime,
            'trade_datetime': trade_datetime,
            'value_datetime': value_datetime,
            'order_id': self.__create_order_id(),
            'account_id': self.__create_account_id,
            'counterparty_id': self.__create_counterparty_id(),
            'trader_id': self.__create_trader_id(),
            'price': self.__create_price(unit_price, quantity),
            'currency': self.create_currency(),
            'isin': isin,
            'market': market,
            'trade_leg': self.__create_trade_leg(),
            'is_otc': self.create_random_boolean(),
            'direction': self.__create_direction(),
            'quantity': quantity,
            'created_timestamp': self.__created_timestamp()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def __create_instrument_details(self):
        # TODO: add get_random_price and get_instrument_from_id to Creatable
        price = self.get_random_price()
        instrument_id = price['instrument_id']
        unit_price = price['price']
        instrument = self.get_instrument_from_id(instrument_id)
        isin = instrument['isin']
        market = instrument['market']
        return isin, market, unit_price

    def __create_contract_id(self):
        return self.create_random_string(10)

    @staticmethod
    def __create_trade_lifecycle_dates():
        # TODO: fix correct dates
        booking_datetime = datetime.date.today()
        trade_datetime = datetime.date.today()
        value_datetime = datetime.date.today()
        return booking_datetime, trade_datetime, value_datetime

    def __create_order_id(self):
        return self.get_random_integer()

    def __create_account_id(self):
        account = self.get_random_account()
        while account['account_type'] not in ['Client', 'Firm']:
            account = self.get_random_account()
        return account['account_id']

    def __create_counterparty_id(self):
        account = self.get_random_account()
        while account['account_type'] != 'Counterparty':
            account = self.get_random_account()
        return account['account_id']

    def __create_trader_id(self):
        return self.create_random_string(10)

    @staticmethod
    def __create_price(unit_price, quantity):
        return unit_price * quantity

    def __create_trade_leg(self):
        return random.choice(self.TRADE_LEGS)

    def __create_direction(self):
        return random.choice(self.DIRECTIONS)

    def __create_quantity(self):
        return self.create_random_integer()

    @staticmethod
    def __created_timestamp():
        return datetime.date.today()
