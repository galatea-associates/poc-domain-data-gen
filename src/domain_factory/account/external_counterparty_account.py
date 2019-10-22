from abc import abstractmethod

from domain_factory.account.brokerage_account import BrokerageAccount


class ECPAccount(BrokerageAccount):
    """ Abstract class to generate ECP accounts. Generate method will call the
   BrokerageAccount generate method in order to populate fields shared by all
   Brokerage accounts. The generate method in this class will then populate the
   remaining attributes unique to the ECP Account domain factory. """

    @abstractmethod
    def generate(self, record_count, start_id):
        """ Generate a set number of ECP accounts
    
            Parameters
            ----------
            record_count : int
                Number of ecp accounts to generate
            start_id : int
                Starting id to generate from
    
            Returns
            -------
            List
                Containing 'record_count' ecp accounts
            """

        records = []

        return records
