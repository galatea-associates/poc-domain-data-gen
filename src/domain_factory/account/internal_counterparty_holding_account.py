from domain_factory.account.external_counterparty_account import ECPAccount


class ICPHoldingAccount(ECPAccount):
    """ Class to generate ICP accounts. Generate method will call the
  ECPAccount generate method in order to populate fields shared by all
  ECP accounts. The generate method in this class will then populate the
  remaining attributes unique to the ICP Holding Account domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of ICP Holding accounts

            Parameters
            ----------
            record_count : int
                Number of ICP Holding accounts to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' ICP Holding accounts
            """

        records = []

        return records
