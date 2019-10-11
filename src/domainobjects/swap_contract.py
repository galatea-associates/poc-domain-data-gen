import random
import uuid

from datetime import datetime, timedelta
from domainobjects.generatable import Generatable

class SwapContract(Generatable):
    """ Class to generate swap contracts. Generate method will generate a set
    of swap contracts. Other generation methods are included where swap
    contracts are the only domain object requiring them.

    Process of generating swap contracts is dependent on counterparties, for
    each of these, randomly select a number of swaps between the user-defined
    range, and generate a record for each swap.
    """

    SWAP_TYPES = ['Equity', 'Portfolio']
    REFERENCE_RATES = ['LIBOR']

    def generate(self, record_count, start_id):
        """ Generate a set number of swap contracts

        Parameters
        ----------
        record_count : int
            Number of swap contracts to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' swap contract
        """

        counterparties =\
            self.retrieve_batch_records('counterparties',
                                        record_count, start_id)

        records = [self.generate_record(counterparty['id'])
                   for counterparty in counterparties
                   for _ in range(0, self.get_number_of_swaps())]

        self.persist_records("swap_contracts")
        return records

    def generate_record(self, counterparty):
        """ Generate a single swap contract

        Parameters
        ----------
        Counterparty : dict
            Dictionary containing a partial record of a counterparty, only
            contains the information necessary to generate swap contracts

        Returns
        -------
        dict
            A single swap contract object
        """

        record = self.instantiate_record()

        status = self.generate_status()
        start_date = self.generate_random_date()
        contract_id = str(uuid.uuid1())
        self.persist_record([contract_id])

        record['counterparty_id'] = counterparty
        record['swap_contract_id'] = contract_id
        record['swap_mnemonic'] = self.generate_random_string(10)
        record['is_short_mtm_financed'] = self.generate_random_boolean()
        record['accounting_area'] = self.generate_random_string(10)
        record['status'] = status
        record['start_date'] = start_date
        record['end_date'] = self.generate_swap_end_date(
                                    start_date=start_date,
                                    status=status)
        record['swap_type'] = self.generate_swap_type()
        record['reference_rate'] = self.generate_reference_rate()
        record['swap_contract_field1'] = self.generate_random_string(10)
        record['swap_contract_field2'] = self.generate_random_string(10)
        record['swap_contract_field3'] = self.generate_random_string(10)
        record['swap_contract_field4'] = self.generate_random_string(10)
        record['swap_contract_field5'] = self.generate_random_string(10)
        record['swap_contract_field6'] = self.generate_random_string(10)
        record['swap_contract_field7'] = self.generate_random_string(10)
        record['swap_contract_field8'] = self.generate_random_string(10)
        record['time_stamp'] = datetime.now()

        return record

    def get_number_of_swaps(self):
        """ Randomly calculate a value between the user-provided minimums
        and maximums.

        Returns
        -------
        int
            The number of swaps
        """

        custom_args = self.get_custom_args()
        swaps_per_counterparty = custom_args['swap_per_counterparty']
        swap_min = int(swaps_per_counterparty['min'])
        swap_max = int(swaps_per_counterparty['max'])
        return random.randint(swap_min, swap_max)

    def generate_swap_end_date(self, years_to_add=5,
                               start_date=None, status=None):
        """ Generate the end date of the swap

        Parameters
        ----------
        years_to_add : int
            Number of years to add to the start date if contract live
        start_date : Date
            Date from which swap contract commenced
        Status : String
            'Live' or 'Dead' - randomly generated beforehand

        Returns
        -------
            String
                If the swap contract is live
            Date
                Where the swap contract is dead, adds specified number of
                years
        """

        return None if status == 'Live' else start_date +\
                       timedelta(days=365 * years_to_add)

    def generate_swap_type(self):
        """ Generate the type of swap

        Returns
        -------
        String
            Random choice between 'Equity' and 'Portfolio'

        """

        return random.choice(self.SWAP_TYPES)

    def generate_reference_rate(self):
        """ Generate the reference rate

        Returns
        -------
        String
            Randomly chosen reference rate
        """

        return random.choice(self.REFERENCE_RATES)

    def generate_status(self):
        """ Generate the current status of the swap

        Returns
        -------
        String
            Random choice between 'Live' and 'Dead'
        """

        return random.choice(['Live', 'Dead'])

    def instantiate_record(self):
        return {
            'counterparty_id': None,
            'swap_contract_id': None,
            'swap_mnemonic': None,
            'accounting_area': None,
            'status': None,
            'start_date': None,
            'end_date': None,
            'swap_type': None,
            'reference_rate': None,
            'swap_contract_field1': None,
            'swap_contract_field2': None,
            'swap_contract_field3': None,
            'swap_contract_field4': None,
            'swap_contract_field5': None,
            'swap_contract_field6': None,
            'swap_contract_field7': None,
            'swap_contract_field8': None,
            'time_stamp': None
        }
