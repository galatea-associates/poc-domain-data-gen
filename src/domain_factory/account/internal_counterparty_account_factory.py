from domain_factory.account.brokerage_account_factory import \
    BrokerageAccountFactory


class ICPAccountFactory(BrokerageAccountFactory):
    """ Class to generate ICP accounts. Generate method will call the
  BrokerageAccountFactory generate method in order to populate fields shared
  by all Brokerage accounts. The generate method in this class will then
  populate the remaining attributes unique to the ICP Account domain
  factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of ICP accounts

        Parameters
        ----------
        record_count : int
            Number of ICP accounts to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' ICP accounts
        """

        records = []

        return records
