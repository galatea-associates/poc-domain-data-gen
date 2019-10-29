from abc import abstractmethod

from domain_factory.factory import Factory


class BrokerageAccountFactory(Factory):
    """ Abstract Class to generate brokerage accounts. Generate method will
    generate the attributes shared by all brokerage account factory child
    classes.

       Account [dir]
        ->Brokerage Account [abstract]
          -> Internal Counterparty [conc]
          -> External Counterparty [abstract]
            -> Contra (ECP) [conc]
            -> ICP Holding [conc]
            -> Depot Claim [conc]
          -> Depot [conc]

       """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of brokerage accounts

        Parameters
        ----------
        record_count : int
            Number of Brokerage accounts to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Brokerage accounts
        """

        pass

    def generate_record(self, id):
        """ Generate a single brokerage account

        Returns
        -------
        dict
            A single brokerage account object
        """

        return {
            'account_id': id,
            'creation_time_stamp': self.generate_timestamp(),
            'updated_time_stamp': self.generate_timestamp(),
            'tax_payer_id': self.generate_tax_payer_id(),
            'account_short_name': self.generate_short_name(),
            'description': self.generate_description()
        }

    def generate_tax_payer_id(self, id):
        """ Generate a single productId

        Returns
        -------
        string
            A single product Id
        """

        return 501 + id

    def generate_short_name(self):
        """ Generate a short name

        Returns
        -------
        string
            A short name
        """

        return "account short name"

    def generate_description(self):
        """ Generate a description

        Returns
        -------
        string
            A Description
        """

        return "account description"
