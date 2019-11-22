from domainobjectfactories.creatable import Creatable
import random

class AccountFactory(Creatable):
    """ Class to create accounts. Create method creates a set amount
    of records. Other creation methods included where accounts are the
    only domain object requiring these.
    """
    ACCOUNT_TYPES = ['Client', 'Firm', 'Counterparty', 'Depot']
    ACCOUNT_PURPOSES = ['Fully Paid', 'Financed', 'Stock Loan',
                        'Rehypo', 'Collateral']
    ACCOUNT_STATUSES = ['Open', 'Closed']

    def create(self, record_count, start_id):
        """ Create a set number of accounts

        Parameters
        ----------
        record_count : int
            Number of accounts to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' accounts
        """

        records = []

        for i in range(start_id, start_id + record_count):
            record = self.create_record(i)
            records.append(record)
            self.persist_record(
                [
                    str(record['account_id']),
                    record['account_type'],
                    record['iban']
                ]
            )

        self.persist_records('accounts')
        return records

    def create_record(self, id):
        """ Create a single account

        Parameters
        ----------
        id : int
            Current id of the account to create

        Returns
        -------
        dict
            A single account record
        """

        opening_date = self.create_opening_date()

        record = {
            'account_id': id,
            'account_type': self.create_account_type(),
            'account_purpose': self.create_account_purpose(),
            'account_description': self.create_account_description(),
            'account_status': self.create_account_status(),
            'iban': self.create_iban(),
            'account_set_id': self.create_account_set_id(),
            'legal_entity_id': self.create_legal_entity_id(),
            'opening_date': opening_date,
            'closing_date': self.create_closing_date(opening_date)
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def create_account_type(self):
        """ Return an account type for from a collection of valid strings

        Returns
        -------
        String
            randomly selected account type
        """
        return random.choice(self.ACCOUNT_TYPES)

    def create_account_purpose(self):
        """ Return an account purpose for from a collection of valid strings

        Returns
        -------
        String
            randomly selected account purpose
        """
        return random.choice(self.ACCOUNT_PURPOSES)

    def create_account_description(self):
        """ Return an account purpose dummy string

        Returns
        -------
        String
            randomly generated 10 character dummy string
        """
        return self.create_random_string(10)

    def create_account_status(self):
        """ Return an account status for from a collection of valid strings

        Returns
        -------
        String
            randomly selected account status
        """
        return random.choice(self.ACCOUNT_STATUSES)

    def create_iban(self):
        """
        Returns an IBAN representative of the format from either the UK (GB),
        Switzerland (CH), France (FR), Germany (DE), or Saudi Arabia (SA).
        TODO: use an external module to generate valid IBANs
        Returns
        -------
        String
           representative IBAN string
        """
        country = random.choice(['GB', 'CH', 'FR', 'DE', 'SA'])
        check_digits = str(self.create_random_integer(length=2))
        if country == 'GB':
            bban = self.create_random_string(4, include_numbers=False).upper()\
                   + str(self.create_random_integer(length=14))
        elif country == 'CH':
            bban = str(self.create_random_integer(length=17))
        elif country == 'FR':
            bban = str(self.create_random_integer(length=20)) +\
                   self.create_random_string(1, include_numbers=False).upper()\
                   + str(self.create_random_integer(length=2))
        elif country == 'DE':
            bban = str(self.create_random_integer(length=18))
        elif country == 'SA':
            bban = str(self.create_random_integer(length=20))
        return country + check_digits + bban

    def create_account_set_id(self):
        """ Return an account set id dummy string

        Returns
        -------
        String
            randomly generated 10 character dummy string
        """
        return self.create_random_string(10)

    def create_legal_entity_id(self):
        """ Return a legal entity id dummy string

        Returns
        -------
        String
            randomly generated 10 character dummy string
        """
        return self.create_random_string(10)

    def create_opening_date(self):
        """ Return a randomly generated date as a string in format YYYYMMDD

        Returns
        -------
        String
            randomly generated date in YYYYMMDD format
        """
        return self.create_random_date().strftime('%Y%m%d')

    def create_closing_date(self, opening_date):
        """ Return a randomly generated date as a string in format YYYYMMDD

        Parameters
        ----------
        opening_date : string
            string representing the account opening date in format YYYYMMDD,
            used as an earliest feasible closing date for date creation

        Returns
        -------
        String
            randomly generated date in YYYYMMDD format
        """
        from_year = int(opening_date[:4])
        from_month = int(opening_date[4:6])
        from_day = int(opening_date[6:])
        return self.create_random_date(from_year=from_year,
                                       from_month=from_month,
                                       from_day=from_day).strftime('%Y%m%d')

