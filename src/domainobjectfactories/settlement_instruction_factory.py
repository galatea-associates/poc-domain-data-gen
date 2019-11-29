import random
from datetime import datetime, timezone, timedelta

from domainobjectfactories.creatable import Creatable


class SettlementInstructionFactory(Creatable):
    FUNCTIONS = ['CANCEL', 'NEW']
    LINKAGE_TYPE = ['BEFORE', 'AFTER', 'WITH', 'INFO']
    ACCOUNT_TYPE = ['SAFE', 'CASH']
    INSTRUCTION_TYPE = ['DVP', 'RVP', 'DELIVERY FREE', 'RECEIVABLE FREE']
    STATUS = ['MATCHED', 'UNMATCHED']
    message_reference_list = []

    def create(self, record_count, start_id):
        """ Create a set number of settlement instructions

        Parameters
        ----------
        record_count : int
            Number of settlement instructions to create
        start_id : int
            Starting id to use when creating message references

        Returns
        -------
        List
            Containing 'record_count' settlement instructions
        """

        message_reference_beginning = self.create_random_string(10)

        records = []

        for i in range(start_id, record_count + start_id):
            record = self.__create_record(i, message_reference_beginning)
            records.append(record)

        return records

    def __create_record(self, id, message_reference_beginning):
        """ Create a single instrument

        Returns
        -------
        dict
            A single back office position object
        """

        instrument = self.get_random_instrument()

        message_reference = self.__create_message_reference(
            message_reference_beginning, id)
        function = self.__get_function()
        message_creation_timestamp = datetime.now(timezone.utc)
        linked_message = \
            self.__get_linked_message(self.message_reference_list)
        # message_reference is added to message_reference_list after
        # generating linked_message, otherwise the linked_message
        # could be this settlement instruction's own message reference
        self.message_reference_list.append(message_reference)
        linkage_type = self.__get_linkage_type()
        place_of_trade = self.__get_place_of_trade()
        trade_datetime = datetime.now(timezone.utc)
        deal_price = self.__get_deal_price()
        currency = self.create_currency()
        isin = self.__get_isin(instrument)
        place_of_listing = self.__get_place_of_listing(instrument)
        quantity = self.create_random_integer()
        party_bic = self.create_random_string(10)
        party_iban = self.__get_party_iban()
        account_type = self.__get_account_type()
        safekeeper_bic = self.create_random_string(10)
        settlement_type = self.__get_settlement_type()
        counterparty_bic = self.create_random_string(10)
        counterparty_iban = self.__get_counterparty_iban()
        settlement_date = self.__get_settlement_date()
        instruction_type = self.__get_instruction_type()
        status = self.__get_status()

        record = {
            'message_reference': message_reference,
            'function': function,
            'message_creation_timestamp': message_creation_timestamp,
            'linked_message': linked_message,
            'linkage_type': linkage_type,
            'place_of_trade': place_of_trade,
            'trade_datetime': trade_datetime,
            'deal_price': deal_price,
            'currency': currency,
            'isin': isin,
            'place_of_listing': place_of_listing,
            'quantity': quantity,
            'party_bic': party_bic,
            'party_iban': party_iban,
            'account_type': account_type,
            'safekeeper_bic': safekeeper_bic,
            'settlement_type': settlement_type,
            'counterparty_bic': counterparty_bic,
            'counterparty_iban': counterparty_iban,
            'settlement_date': settlement_date,
            'instruction_type': instruction_type,
            'status': status
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def __create_message_reference(self, message_reference_beginning, id):
        """The 10 character string generated will have id appended to it
        to ensure Message Reference is unique"""
        return message_reference_beginning + str(id)

    def __get_function(self):
        """Randomly select a function

        Returns
        -------
        String
            A randomly chosen function
        """
        return random.choice(self.FUNCTIONS)

    @staticmethod
    def __get_linked_message(message_reference_list):
        """ 50/50 chance of returning EMPTY or the message reference of
        a previously generated settlement instruction

        Returns
        -------
        String
            EMPTY or the message reference of
            a previously generated settlement instruction
        """
        if not message_reference_list:
            return "EMPTY"
        else:
            return random.choice(
                ["EMPTY", random.choice(message_reference_list)])

    def __get_linkage_type(self):
        """ Randomly select a linkage type

        Returns
        -------
        String
            A randomly chosen linkage type
        """
        return random.choice(self.LINKAGE_TYPE)

    def __get_place_of_trade(self):
        """ Select a random exchange code

        Returns
        -------
        String
            Select exchange code from a randomly selected row
            of the exchanges table
        """
        return self.get_random_row('exchanges')['exchange_code']

    def __get_deal_price(self):
        """ Create random decimal between 1 and 100,000

        Returns
        -------
        float
            Randomly created value between 1 and 100,000
        """
        return self.create_random_decimal(min=1, max=100000)

    @staticmethod
    def __get_isin(instrument):
        """ Get isin from instrument passed in

        Returns
        -------
        String
            isin from instrument passed in
        """
        return instrument['isin']

    @staticmethod
    def __get_place_of_listing(instrument):
        """ Get market from instrument passed in

        Returns
        -------
        String
            market from instrument passed in
        """
        return instrument['market']

    def __get_party_iban(self):
        # TODO We're using the existing
        #  get_random_record_with_valid_attribute method but we should
        #  replace this with one that is opt-in rather than opt-out because
        #  the best description of this field is any account where the type
        #  IS Client or Firm

        """ Get iban value from randomly chosen account
        with account type Firm or Client

        Returns
        -------
        String
            iban value from randomly chosen account
            with account type Firm or Client
        """
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Counterparty', 'Depot']
        )

        return account['iban']

    def __get_account_type(self):
        """Randomly select an account type

        Returns
        -------
        String
            A randomly chosen account type
        """
        return random.choice(self.ACCOUNT_TYPE)

    @staticmethod
    def __get_settlement_type():
        """ Get settlement type
        Returns
        -------
        String
            Hardcoded to always return string 'Beneficial Ownership'
        """
        return 'Beneficial Ownership'

    def __get_counterparty_iban(self):
        # TODO We're using the existing
        #  get_random_record_with_valid_attribute method but we should
        #  replace this with one that is opt-in rather than opt-out because
        #  the best description of this field is any account where the type
        #  IS Counterparty

        """ Get iban value from randomly chosen account with
        account type Counterparty

        Returns
        -------
        String
            iban value from randomly chosen account with
            account type Counterparty
        """
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Client', 'Firm', 'Depot']
        )

        return account['iban']

    @staticmethod
    def __get_settlement_date():
        """ Gets the date in two days' time

        Returns
        -------
        Date
            Date in two days' time
        """
        return datetime.now(timezone.utc).date() + timedelta(days=2)

    def __get_instruction_type(self):
        """Randomly select an instruction type

        Returns
        -------
        String
            A randomly chosen instruction type
        """
        return random.choice(self.INSTRUCTION_TYPE)

    def __get_status(self):
        """Randomly select a status

        Returns
        -------
        String
            A randomly chosen status
        """
        return random.choice(self.STATUS)
