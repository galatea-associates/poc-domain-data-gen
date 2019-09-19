from multiprocessing import Manager, Process
from multi_processing.generator import Generator
from multi_processing.writer import Writer

# Class to coordinate the multiprocessing implementation. It is
# required to abstract the multiprocessing logic from any unpickleable
# objects, such as the database connection.


class Coordinator():

    def __init__(self, max_file_size, file_builder):
        queue_manager = Manager()
        self.__generation_job_queue = queue_manager.Queue()
        self.__write_job_queue = queue_manager.Queue()

        self.__generation_coordinator = Generator(
            self.__generation_job_queue,
            self.__write_job_queue
        )

        self.__write_coordinator = Writer(
            self.__write_job_queue,
            max_file_size,
            file_builder
        )

        self.processes = []

    def create_jobs(self, domain_obj, quantity, job_size):
        start_id = 0
        quantity = int(quantity)

        while quantity > 0:
            if quantity > job_size:
                job = {'domain_object': domain_obj,
                       'amount': job_size,
                       'start_id': start_id}
                quantity = quantity - job_size
                start_id = start_id + job_size
            else:
                job = {'domain_object': domain_obj,
                       'amount': quantity,
                       'start_id': start_id}
                quantity = 0
            self.__generation_job_queue.put(job)

        self.__generation_job_queue.put("terminate")

    def start_generator(self, obj_class, custom_obj_args, pool_size):
        generator_p = Process(target=self.get_generation_coordinator().start,
                              args=(obj_class, custom_obj_args, pool_size,))
        generator_p.start()
        self.processes.append(generator_p)

    def start_writer(self, pool_size):
        writer_p = Process(target=self.get_write_coordinator().start,
                           args=(pool_size,))
        writer_p.start()
        self.processes.append(writer_p)

    def get_generation_coordinator(self):
        return self.__generation_coordinator

    def get_write_coordinator(self):
        return self.__write_coordinator

    # Waits for spawned processes to complete before terminating
    def await_termination(self):
        for process in self.processes:
            process.join()
