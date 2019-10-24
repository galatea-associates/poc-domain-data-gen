from abc import abstractmethod

from domain_factory.generatable import Generatable


class AccountCollectionFactory(Generatable):
    """ Abstract Class to generate Account Collections.  Generate method will
    generate the attributes shared by all brokerage account child classes.

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
