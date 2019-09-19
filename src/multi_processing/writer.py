import time
import multi_processing.pool_tasks as mp_p


class Writer():

    def __init__(self, write_queue, max_file_size, file_builder):
        self.write_queue = write_queue

        self.all_records = []
        self.file_number = 0
        self.max_size = int(max_file_size)

        self.job_list = []
        self.terminate = False
        self.file_builder = file_builder

    def start(self, pool_size):

        while not self.terminate:
            self.wait_for_jobs()
            self.handle_jobs(pool_size)
            self.run_jobs(pool_size)
            self.reset_job_list()

        self.calculate_residual_writes()
        self.run_jobs(pool_size)

    def wait_for_jobs(self):
        while self.write_queue.empty():
            time.sleep(1)
        return

    def handle_jobs(self, pool_size):
        while (not self.write_queue.empty()
                and len(self.job_list) < pool_size*2):
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
        for item in records:
            self.all_records.append(item)

    def calculate_writes(self):
        # self.max_size indicates largest file size
        # self.all_records contains all records currently received
        file_size = self.max_size
        file_builder = self.file_builder
        if len(self.all_records) > int(file_size):
            file_num = self.get_file_num()
            records = self.all_records[:file_size]
            del self.all_records[:file_size]
            job = {
                'file_number': file_num,
                'file_builder': file_builder,
                'records': records
            }
            self.job_list.append(job)

    def get_file_num(self):
        cur = self.file_number
        self.file_number = cur+1
        return cur

    def run_jobs(self, pool_size):
        mp_p.write(self.job_list, pool_size)

    def reset_job_list(self):
        self.job_list = []

    def calculate_residual_writes(self):
        file_builder = self.file_builder
        file_num = self.get_file_num()
        records = self.all_records
        job = {
                'file_number': file_num,
                'file_builder': file_builder,
                'records': records
            }
        self.job_list.append(job)
        self.all_records = None
