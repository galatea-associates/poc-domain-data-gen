from abc import abstractmethod

from domain_factory.generatable import Generatable


class BrokerageAccount(Generatable):
    """ Abstract Class to generate brokerage accounts. Generate method will
    generate the attributes shared by all brokerage account child classes.

       Account [dir]
        ->Brokerage Account [abstract]
          -> Internal Counterparty [impl]
          -> External Counterparty [abstract]
            -> Contra (ECP) [impl]
            -> ICP Holding [impl]
            -> Depot Claim [impl]
          -> Depot [impl]

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

        records = []

        return records
