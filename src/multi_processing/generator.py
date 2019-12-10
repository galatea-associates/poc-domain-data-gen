import time
import multi_processing.pool_tasks as pool_tasks


class Generator:
    """ A class to coordinate the generation of domain objects as per jobs
    observed within a multiprocessed queue. Data is then generated in a pool
    before the result of which is put into the write queue.

    Attributes
    ----------
    queue_of_generate_jobs : Multiprocess Queue
        Multiprocess safe queue from which jobs to generate data is taken
    queue_of_generated_records : Multiprocess Queue
        Multiprocess safe queue on which generated data is placed
    terminate : Boolean
        Boolean flag which when True indicates the coordinator is to terminate

    Methods
    -------
    start(obj_class, number_of_processes_per_generate_job)
        Begin the cycle of waiting for, formatting and running jobs. Continue
        this until termination instruction observed
    sleep_while_generate_queue_empty()
        Sleep whilst the generation queue is empty
    format_jobs(obj_class, number_of_processes_per_generate_job)
        Retrieve jobs from queue and place them into an iterable structure
    issue_termination()
        Set flag to terminate to True
    run_jobs(job_list, number_of_processes_per_generate_job)
        Pass formatted jobs to the generation pool for execution
    get_queue_of_generate_jobs()
        Return a pointer to the multiprocess safe generation job queue
    """

    def __init__(self, queue_of_generate_jobs, queue_of_generated_records):
        """ Assign variables from input, and set termination to False

        Parameters
        ----------
        queue_of_generate_jobs : Multiprocessed Queue
            Queue containing jobs to generate an amount of domain objects
        queue_of_generated_records : Multiprocessed Queue
            Queue containing resultant generated objects for writing to file
        """

        self.queue_of_generate_jobs = queue_of_generate_jobs
        self.queue_of_generated_records = queue_of_generated_records
        self.terminate_job_dequeued = False

    def start(self, object_factory):
        """ Begin the cycle of waiting for, formatting, and running jobs,
        continuing this until an instruction to terminate is observed.

        Parameters
        ----------
        object_factory : Generatable
            Instantiated and pre-configured object factory which produces
            the current object.
        """

        number_of_processes_per_generate_job =\
            object_factory.get_shared_args()[
                'number_of_generate_processes_per_pool'
            ]
        maximum_length_of_generate_job_list \
            = 2 * number_of_processes_per_generate_job

        while not self.terminate_job_dequeued:
            self.sleep_while_generate_queue_empty()
            list_of_generate_jobs = \
                self.get_list_of_generate_jobs_from_generate_queue(
                    object_factory, maximum_length_of_generate_job_list
                )
            records = pool_tasks.execute_generate_jobs(
                list_of_generate_jobs,
                number_of_processes_per_generate_job
            )
            self.queue_of_generated_records.put(records)

        self.queue_of_generated_records.put("terminate")

    def sleep_while_generate_queue_empty(self):
        """ Sleep until jobs are on the queue """

        while self.queue_of_generate_jobs.empty():
            time.sleep(1)
        return

    def get_list_of_generate_jobs_from_generate_queue(
            self, object_factory, maximum_length_of_generate_job_list
    ):
        """ Takes jobs from the Multiprocess Safe Queue and places them into
        a list for later execution. If twice the pool size of jobs are
        formatted, then this list is returned. If the termination flag is
        observed, then this list is returned. If the queue is empty, then
        the list so far is returned.

        Parameters
        ----------
        object_factory : Generatable
            Instantiated and pre-configured object factory which produces
            the current object.
        maximum_length_of_generate_job_list : int
            Max length the job list can reach before it is added to the queue

        Returns
        -------
        List
            Containing jobs taken from the Queue. A list intermediary is
            required as multiprocessing pools require an iterable object,
            which a multiprocessing queue is not.
        """

        list_of_generate_jobs = []

        while not self.queue_of_generate_jobs.empty() and \
                len(list_of_generate_jobs) < \
                maximum_length_of_generate_job_list:

            generate_job = self.queue_of_generate_jobs.get()

            if generate_job == "terminate":
                self.terminate_job_dequeued = True

            else:
                list_of_generate_jobs.append([generate_job, object_factory])

        return list_of_generate_jobs
