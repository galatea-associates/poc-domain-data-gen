from domainobjects.generatable import Generatable
from datetime import datetime, timedelta
import random
import string
import timeit
import pandas as pd
import logging

class SwapPosition(Generatable):

    def generate(self, record_count, custom_args):
        config = self.get_object_config()
        ins_per_swap_range = custom_args['ins_per_swap']

        records_per_file = int(config['max_objects_per_file'])
        file_num = 1
        i = 1

        records = []
        persisting_records = []
        database = self.get_database()

        all_instruments = database.retrieve('instruments')
        start_date = datetime.strptime(custom_args['start_date'], '%Y%m%d')
        date_range = pd.date_range(start_date, datetime.today(), freq='D')

        batch_size = int(config['batch_size'])
        logging.info("Batch size for Swap Positions are: "+str(batch_size))
        offset = 0

        # Throughput timer
        start_gen = timeit.default_timer()

        while True:
            swap_contract_batch = database\
                .retrieve_batch('swap_contracts', batch_size, offset)
            offset += batch_size

            for swap_contract in swap_contract_batch:
                ins_count = random.randint(
                    int(ins_per_swap_range['min']),
                    int(ins_per_swap_range['max']))
                instruments = random.sample(all_instruments, ins_count)

                for instrument in instruments:
                    long_short = self.generate_long_short()
                    purpose = self.generate_purpose()
                    for position_type in ['S', 'I', 'E']:
                        quantity = self.generate_random_integer(
                            negative=long_short.upper() == "SHORT"
                        )
                        for date in date_range:
                            current_date = datetime.strftime(date, '%Y-%m-%d')
                            records.append({
                                'swap_position_id': i,
                                'ric': instrument['ric'],
                                'swap_contract_id': swap_contract['id'],
                                'position_type': position_type,
                                'knowledge_date': current_date,
                                'effective_date': current_date,
                                'account': self.generate_account(),
                                'long_short': long_short,
                                'td_quantity': quantity,
                                'purpose': purpose,
                                'time_stamp': datetime.now()
                            })

                            if (position_type == 'E'):
                                persisting_records.append([str(swap_contract['id']), instrument['ric'], position_type, current_date, str(long_short)])

                            if (i % int(batch_size) == 0):
                                database.persist_batch(
                                    "swap_positions", persisting_records
                                )
                                persisting_records = []

                            if (i % records_per_file == 0):
                                self.write_to_file(file_num, records)
                                end_gen = timeit.default_timer()
                                generation_throughput = \
                                    records_per_file/(end_gen-start_gen)
                                logging.info('''Swap Position
                                             generation throughput: '''
                                             + str(generation_throughput))
                                start_gen = timeit.default_timer()

                                file_num += 1
                                records = []

                            i += 1
            if not swap_contract_batch:
                break

        if records != []:
            self.write_to_file(file_num, records)
            end_gen = timeit.default_timer()
            generation_throughput = \
                len(records)/(end_gen-start_gen)
            logging.info("Swap Position generation throughput: "
                         + str(generation_throughput))
            records = []

        if persisting_records != []:
            database.persist_batch("swap_positions", persisting_records)
            persisting_records = []

        database.commit_changes()

    def generate_account(self):
        account_type = random.choice(self.ACCOUNT_TYPES)
        random_string = ''.join(random.choices(string.digits, k=4))
        return ''.join([account_type, random_string])

    def generate_long_short(self):
        return random.choice(self.LONG_SHORT)

    def generate_purpose(self):
        return 'Outright'
