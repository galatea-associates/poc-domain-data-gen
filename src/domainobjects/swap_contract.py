import random
import uuid

from datetime import datetime, timedelta
from domainobjects.generatable import Generatable

class SwapContract(Generatable):

    def generate(self, record_count, custom_args, start_id):
        swaps_per_counterparty = custom_args['swap_per_counterparty']
        swap_min = int(swaps_per_counterparty['min'])
        swap_max = int(swaps_per_counterparty['max'])

        record = self.instantiate_record()
        records = []
        persisting_records = []
        counterparties = self.retrieve_batch_records('counterparties',
                                                 record_count, start_id)

        for counterparty in counterparties:
            swap_count = random.randint(swap_min, swap_max)
            record["counterparty_id"] = counterparty['id']
            for _ in range(0, swap_count): 
                contract_id = str(uuid.uuid1())
                record['swap_contract_id'] = contract_id
                record = self.generate_remaining_record(record)
                records.append(record.copy())

                persisting_records.append([contract_id])

        self.persist_records("swap_contracts", persisting_records)
        return records

    def generate_remaining_record(self, record):
        start_date = self.generate_random_date()
        status = self.generate_status()

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

    def generate_swap_end_date(self, years_to_add=5,
                               start_date=None, status=None):
        return None if status == 'Live' else start_date +\
                             timedelta(days=365 * years_to_add)

    def generate_swap_type(self):
        return random.choice(['Equity', 'Portfolio'])

    def generate_reference_rate(self):
        return random.choice(['LIBOR'])

    def generate_status(self):
        return random.choice(['Live', 'Dead'])

    def instantiate_record(self):
        return {
            'swap_mnemonic': None,
            'accounting_area': None,
            'status': None,
            'start_date': None,
            'end_date': None,
            'swap_type': None,
            'reference_rate': None,
            'swap_contract_f1': None,
            'swap_contract_f2': None,
            'swap_contract_f3': None,
            'swap_contract_f4': None,
            'swap_contract_f5': None,
            'swap_contract_f6': None,
            'swap_contract_f7': None,
            'swap_contract_f8': None,
            'time_stamp': None
        }
