from domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):

    def generate(self, record_count, custom_args, start_id):

        records = []

        database = self.establish_db_connection()

        self.instruments = database.retrieve('instruments')

        for i in range(start_id, start_id+record_count):
            records.append(self.generate_record(i))

        return records

    def generate_record(self, id):
        instrument = self.get_random_instrument()
        return {
                'order_id': id,
                'account_num': self.generate_random_integer(length=8),
                'direction': self.generate_credit_debit(),
                'sto_id': self.generate_random_integer(length=7),
                'agent_id': self.generate_random_integer(length=7),
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'ric': instrument['ric'],
                'qty': self.generate_random_integer(),
                'time_stamp': datetime.now(),
            }