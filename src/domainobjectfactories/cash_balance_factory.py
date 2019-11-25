import random
import datetime

from domainobjectfactories.creatable import Creatable


class CashBalanceFactory(Creatable):
    """ Class to create cash balances. Create method will create a set
    amount of balances. Other creation methods included where cash balances
    are the only domain object requiring them. """

    CASH_BALANCE_PURPOSES = ['Cash Balance', 'P&L', 'Fees',
                             'Collateral Posted', 'Collateral Received']

    def create(self, record_count, start_id):
        """ Create a set number of cash balances

        Parameters
        ----------
        record_count : int
            Number of cash balances to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' cash balances
        """

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.create_record())

        return records

    def create_record(self):
        """ Create a single cash balance

        Returns
        -------
        dict
            A single cash balance object
        """

        account_id, account_owner = self.create_account_details()

        record = {
            'as_of_date': self.create_as_of_date(),
            'amount': self.create_amount(),
            'currency': self.create_currency(),
            'account_id': account_id,
            'account_owner': account_owner,
            'purpose': self.create_purpose()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    @staticmethod
    def create_as_of_date():
        """ Return an 'as of date', being either the current date or the date
        in 2 days time

        Returns
        -------
        Date
            Date object representing either the current date, or the date in
            2 days time
        """
        today = datetime.date.today()
        day_after_tomorrow = today + datetime.timedelta(days=2)
        return random.choice((today, day_after_tomorrow))

    def create_amount(self):
        """ Return cash balance amount, being a positive or negative integer
        with absolute value not greater than 10000

        Returns
        -------
        int
            positive or negative integer with magnitude < 10000
        """
        return self.create_random_integer(negative=
                                          random.choice(self.TRUE_FALSE))

    @staticmethod
    def account_valid(account_row):
        """ Return boolean indicating if a row from the 'accounts' table in
        the database represents a 'Client' or 'Firm' account

        Returns
        -------
        bool
            boolean representing if account is either 'Client' or 'Firm'
        """
        return account_row['account_type'] in ('Client', 'Firm')

    def create_account_details(self):
        """ Return valid account id and type from the 'accounts' table in the
        database - account is valid if type is 'Client' or 'Firm'.

        Returns
        -------
        string
            account id

        string
            account type
        """
        account_row = random.choice(
            list(
                filter(self.account_valid, self.retrieve_records('accounts'))
            )
        )
        return account_row['account_id'], account_row['account_type']

    def create_purpose(self):
        """ Create a purpose for a cash balance

        Returns
        -------
        String
            One of the possible purposes relevant for cash balances
        """

        return random.choice(self.CASH_BALANCE_PURPOSES)
