from abc import abstractmethod

from domain_factory.factory import Factory


class AccountCollectionFactory(Factory):
    """ Abstract Class to generate Account Collections.  Generate method will
    generate the attributes shared by all account collection factory child
    classes.

    AccountCollection [dir]
        ->AccountCollection [abstract]
            ->AccountGroup [conc]
            ->BookingEntity [abstract]
                ->BookingCompany [conc]
                ->BookingSubCompany [abstract]
                    ->PureTradingEntity [conc]
                    ->BrokerDealerEntity[conc]
                    ->PureSettlementEntity [conc]

    """

    @abstractmethod
    def generate(self, record_count, start_id):
        """generate a set number of Account Collections

            Parameters
            ----------
            record_count : int
                Number of Account Collections to generate
            start_id : int
                Starting id to generate from

            Returns
            -------
            List
                Containing 'record_count' Account Collections
            """

        pass

    def generate_record(self, id):
        """ Generate a single account collection

        Returns
        -------
        dict
            A single account collection object
        """

        return {
            'account_collection_id': id,
            'creation_time_stamp': self.generate_timestamp(),
            'updated_time_stamp': self.generate_timestamp(),
            'account_collection_short_name': self.generate_short_name(),
            'description': self.generate_description()
        }

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