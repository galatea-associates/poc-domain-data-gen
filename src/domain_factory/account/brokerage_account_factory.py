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
