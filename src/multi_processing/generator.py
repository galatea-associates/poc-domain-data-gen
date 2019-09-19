import time
import multi_processing.pool_tasks as mp_p


class Generator():

    def __init__(self, generate_queue, write_queue):
        self.generate_queue = generate_queue
        self.write_queue = write_queue
        self.terminate = False

    def start(self, obj_class, custom_obj_args, pool_size):

        while not self.terminate:
            self.wait_for_jobs()
            job_list = self.format_jobs(obj_class, custom_obj_args, pool_size)
            self.run_jobs(job_list, pool_size)

        self.write_queue.put("terminate")

    def wait_for_jobs(self):
        while self.generate_queue.empty():
            time.sleep(1)
        return

    def format_jobs(self, obj_class, custom_obj_args, pool_size):
        job_list = []
        while (not self.generate_queue.empty()
                and len(job_list) < (pool_size*2)):
            job = self.get_job()
            if (job == "terminate"):
                self.issue_termination()
            else:
                job_list.append([job, obj_class, custom_obj_args])
        return job_list

    def get_job(self):
        return self.generate_queue.get()

    def issue_termination(self):
        self.terminate = True

    def run_jobs(self, job_list, pool_size):
        records = mp_p.generate(job_list, pool_size)
        self.write_queue.put(records)

    def get_generation_queue(self):
        return self.generate_queue
