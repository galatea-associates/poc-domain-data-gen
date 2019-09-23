from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import string
import pandas as pd

class SwapPosition(Generatable):

    def generate(self, record_count, start_id):

        record = self.instantiate_record()
        records = []
        persisting_records = []

        all_instruments = self.retrieve_records('instruments')

        start_date = datetime.strptime(self.get_start_date(), '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')
        swap_contract_batch = self.retrieve_batch_records('swap_contracts',
                                                      record_count, start_id)

        for swap_contract in swap_contract_batch:
            record['swap_contract_id'] = swap_contract['id']
            ins_count = self.get_number_of_instruments()
            instruments = random.sample(all_instruments, ins_count)
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

    def get_number_of_instruments(self):
        custom_args = self.get_custom_args()
        ins_per_swap_range = custom_args['ins_per_swap']
        min_ins = int(ins_per_swap_range['min'])
        max_ins = int(ins_per_swap_range['max'])
        return random.randint(min_ins, max_ins)

    def get_start_date(self):
        custom_args = self.get_custom_args()
        return custom_args['start_date']

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