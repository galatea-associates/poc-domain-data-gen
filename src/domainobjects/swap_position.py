from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import string
import pandas as pd

class SwapPosition(Generatable):

    def generate(self, record_count, custom_args, start_id):
        ins_per_swap_range = custom_args['ins_per_swap']
        range_min = ins_per_swap_range['min']
        range_max = ins_per_swap_range['max']

        record = self.instantiate_record()
        records = []
        persisting_records = []

        all_instruments = self.retrieve_records('instruments')

        start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')
        swap_contract_batch = self.retrieve_batch_records('swap_contracts',
                                                      record_count, start_id)

        for swap_contract in swap_contract_batch:
            ins_count = random.randint(int(range_min), int(range_max))
            instruments = random.sample(all_instruments, ins_count)
            record['swap_contract_id'] = swap_contract['id']
            
            for instrument in instruments:
                long_short = self.generate_long_short()
                purpose = self.generate_purpose()
                record['ric'] = instrument['ric']
                record['long_short'] = long_short
                record['purpose'] = purpose

                for position_type in ['S', 'I', 'E']:
                    quantity = self.generate_random_integer(
                        negative=long_short.upper() == "SHORT"
                    )
                    record['td_quantity'] = quantity
                    record['position_type'] = position_type
                    for date in date_range:
                        current_date = datetime.strftime(date, '%Y-%m-%d')
                        record = self.generate_remaining_record(record, current_date)
                        records.append(record.copy())

                        if (position_type == 'E'):
                            persisting_records.append(
                                [str(swap_contract['id']),
                                 instrument['ric'],
                                 position_type,
                                 current_date,
                                 str(long_short)]
                            )

        self.persist_records('swap_positions', persisting_records)
        return records

    def generate_remaining_record(self, record, current_date):
        record['knowledge_date'] = current_date
        record['effective_date'] = current_date
        record['account'] = self.generate_account()
        record['time_stamp'] = datetime.now()
        return record

    def generate_account(self):
        account_type = random.choice(self.ACCOUNT_TYPES)
        random_string = ''.join(random.choices(string.digits, k=4))
        return ''.join([account_type, random_string])

    def generate_long_short(self):
        return random.choice(self.LONG_SHORT)

    def generate_purpose(self):
        return 'Outright'

    def instantiate_record(self):
        return {
            'ric': None,
            'swap_contract_id': None,
            'position_type': None,
            'knowledge_date': None,
            'effective_date': None,
            'account': None,
            'long_short': None,
            'td_quantity': None,
            'purpose': None,
            'time_stamp': None
        }