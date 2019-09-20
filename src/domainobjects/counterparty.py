from domainobjects.generatable import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):

    def generate(self, record_count, custom_args, start_id):

        database = self.establish_db_connection()
        records = []
        persisting_records = []

        for i in range(start_id, record_count+start_id):
            records.append(self.get_record(i))
            persisting_records.append([str(i)])

        database.persist_batch("counterparties", persisting_records)
        database.commit_changes()
        return records

    def get_record(self, current_id):
        return {
            'counterparty_id': current_id,
            'book': self.generate_random_string(5, include_numbers=False),
            'counterparty_field1': self.generate_random_string(10),
            'counterparty_field2': self.generate_random_string(10),
            'counterparty_field3': self.generate_random_string(10),
            'counterparty_field4': self.generate_random_string(10),
            'counterparty_field5': self.generate_random_string(10),
            'counterparty_field6': self.generate_random_string(10),
            'counterparty_field7': self.generate_random_string(10),
            'counterparty_field8': self.generate_random_string(10),
            'counterparty_field9': self.generate_random_string(10),
            'counterparty_field10': self.generate_random_string(10),
            'time_stamp': datetime.now()
        }
