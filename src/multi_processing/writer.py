import time
import cProfile, pstats, io
from pstats import SortKey

import multi_processing.pool_tasks as mp_p

class Writer():

    def __init__(self, write_queue, max_file_size, file_builder):
        self.write_queue = write_queue

        self.all_records = {}       # Dictionary of {'Domain_Object':ALL RECORDS} that jobs are built FROM
        self.file_numbers = {}      # Tracker of current file num for each D_O
        self.max_size = int(max_file_size)

        self.job_list = []
        self.terminate = False
        self.file_builder = file_builder

    def start(self, pool_size):
        #pr = cProfile.Profile()
        #pr.enable()
        
        while not self.terminate:
            self.wait_for_jobs()
            self.handle_jobs()
            self.run_jobs(pool_size)
            self.reset_job_list()

        self.calculate_residual_writes() 
        self.run_jobs(pool_size)

        #pr.disable()
        #s = io.StringIO()
        #ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
        #ps.print_stats()
        #print(s.getvalue())

    def wait_for_jobs(self):
        while self.write_queue.empty():
            time.sleep(1)
        return

    def handle_jobs(self):
        while (not self.write_queue.empty()
                and len(self.job_list) < 2):
            record_list = self.get_job()
            if (record_list == "terminate"):
                self.issue_termination()
            else:
                self.format_jobs(record_list)

    def format_jobs(self, record_list):
        for job in record_list:
            domain_object = job[0]
            records = job[1]
            self.add_to_stored_records(domain_object, records)
            self.calculate_writes()

    def get_job(self):
        return self.write_queue.get()

    def issue_termination(self):
        self.terminate = True

    def add_to_stored_records(self, domain_object, records):
        cur = self.all_records.get(domain_object)
        if cur is None:
            self.all_records[domain_object] = records
        else:
            for item in records: 
                self.all_records[domain_object].append(item)

    def calculate_writes(self):
        # self.max_size indicates largest file size
        # self.all_records contains all records currently received
        store = self.all_records
        file_size = self.max_size
        file_builder = self.file_builder
        for domain_object in store:
            if len(store[domain_object]) > int(file_size):
                file_num = self.get_file_num(domain_object)
                records = store[domain_object][:file_size]
                del store[domain_object][:file_size]
                job = {
                    'domain_object': domain_object,
                    'file_number': file_num,
                    'file_builder': file_builder,
                    'records': records
                }
                self.job_list.append(job)

    def get_file_num(self, domain_object):
        cur = self.file_numbers.get(domain_object)
        if cur is None:
            self.file_numbers[domain_object] = 2
            return 1
        else:
            self.file_numbers[domain_object] = cur+1
            return cur

    def run_jobs(self, pool_size):
        mp_p.write(self.job_list, pool_size)

    def reset_job_list(self):
        self.job_list = []

    def calculate_residual_writes(self):
        store = self.all_records
        file_builder = self.file_builder
        for domain_object in store:
            file_num = self.get_file_num(domain_object)
            records = store[domain_object]
            job = {
                    'domain_object': domain_object,
                    'file_number': file_num,
                    'file_builder': file_builder,
                    'records': records
                }
            self.job_list.append(job)
        self.all_records = None
