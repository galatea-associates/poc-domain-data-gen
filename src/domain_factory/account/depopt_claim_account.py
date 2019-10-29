from domain_factory.account.external_counterparty_account import ECPAccount


class DepotClaimAccount(ECPAccount):
    """ Class to generate depot claim ecp accounts. Generate method will call
    the ECPAccount generate method in order to populate fields shared by all
    ECP accounts. The generate method in this class will then populate the
    remaining attributes unique to the Depot Claim Account domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of Depot Claim accounts

            Parameters
            ----------
            record_count : int
                Number of Depot Claim accounts to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Depot Claim accounts
            """

        records = []

        return records
