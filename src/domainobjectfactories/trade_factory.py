import random
from datetime import datetime, timezone, timedelta

from domainobjectfactories.creatable import Creatable


class TradeFactory(Creatable):
    """ Class to create trades. Create method will create a
    set amount of trades. """

    TRADE_LEGS = ["EMPTY", "1", "2"]
    DIRECTIONS = ["BUY", "SELL"]

    def create(self, record_count, start_id):
        """ Create a set number of trades

        Parameters
        ----------
        record_count : int
            Number of trades to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' trades
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
        """ Return the isin and market of an instrument persisted in the
        local database.

        Returns
        -------
        String
            isin of instrument from local database
        String
            market of instrument from local database
        """
        instrument = self.get_random_instrument()
        isin = instrument['isin']
        market = instrument['market']
        return isin, market

    def __create_contract_id(self):
        """ Return id of the trade contract
        Returns
        -------
        String
            10 character random string representing trade contract id
        """
        return self.create_random_string(10)

    @staticmethod
    def __create_trade_lifecycle_dates():
        """ return datetime objects representing when the trade was booked,
        executed and due to be settled respectively. These are currently hard
        coded to be the current date for booking and executing, and 2 days in
        the future for settlement. Datetimes are in UTC, and value date is set
        to 1 minute past midnight on the morning of T+2

        Returns
        -------
        Datetime
            Datetime object in UTC representing booking datetime - set to use
            current datetime
        Datetime
            Datetime object in UTC representing trade datetime - set to use
            current datetime
        Datetime
            Datetime object in UTC representing expected value datetime - set
            to 1 minute past midgnight on the morning of T+2, where the
            current date is T
        """
        booking_datetime = trade_datetime = datetime.now(timezone.utc)
        day_after_tomorrow = datetime.now(timezone.utc) + timedelta(days=2)
        value_datetime = day_after_tomorrow.replace(
            hour=0, minute=1, second=0, microsecond=0
        )
        return booking_datetime, trade_datetime, value_datetime

    def __create_order_id(self):
        """ Return id of the order
        Returns
        -------
        Integer
            random integer between 1 and 10000
        """
        return self.create_random_integer()

    def __get_account_id(self):
        """ Return the account id value of an account persisted in the
        database that is type 'Client' or 'Firm'

        Returns
        -------
        String
            account id of 'Client' or 'Firm' type account from database
        """
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Counterparty', 'Depot']
        )
        return account['account_id']

    def __get_counterparty_id(self):
        """ Return the account id value of an account persisted in the
        database that is type 'Counterparty'

        Returns
        -------
        String
            account id of 'Counterparty' type account from database
        """
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Client', 'Firm', 'Depot']
        )
        return account['account_id']

    def __create_trader_id(self):
        """ Return id of the trader
        Returns
        -------
        String
            10 character random string representing trader id
        """
        return self.create_random_string(10)

    def __create_price(self, quantity):
        """ Return total value of the trade, found by multiplying instrument
        quantity by a randomly generated unit price. Unit price is generated
        to represent the trade being done at a different price to the market
        price that might be given by a Price domain object
        Returns
        -------
        Float
            Total trade price to 2 decimal places
        """
        unit_price = self.create_random_decimal(min=1, max=10)
        return round(unit_price * quantity, 2)

    def __create_trade_leg(self):
        """ Return trade leg
        Returns
        -------
        String
            one of "1", "2" or "EMPTY"
        """
        return random.choice(self.TRADE_LEGS)

    def __create_direction(self):
        """ Return direction
        Returns
        -------
        String
            one of "BUY", "SELL"
        """
        return random.choice(self.DIRECTIONS)

    def __create_quantity(self):
        """ Return quantity of instruments in the trade
        Returns
        -------
        Integer
            random integer between 1 and 10000
        """
        return self.create_random_integer()

    @staticmethod
    def __create_created_timestamp():
        """ return datetime representing when the trade was entered into the
        system in UTC
        Returns
        -------
        Datetime
            Datetime object in UTC
        """
        return datetime.now(timezone.utc)
