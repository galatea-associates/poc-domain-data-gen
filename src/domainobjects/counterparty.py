from domainobjects.generatable import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):

    def generate(self, record_count, custom_args, start_id):

        self.establish_db_connection()
        database = self.get_database()
        records = []

        for i in range(start_id, record_count+start_id):
            records.append({
                'counterparty_id': i,
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
                'time_stamp': datetime.now()})

            database.persist("counterparties", [str(i+1)])
        database.commit_changes()
        return records
