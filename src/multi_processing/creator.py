import time
from multi_processing import pool_tasks


class Creator:
    """ A class to coordinate the generation of domain objects as per jobs
    observed within a multiprocessed queue. Data is then generated in a pool
    before the result of which is put into the write queue.

    Attributes
    ----------
    create_job_queue : Multiprocess Queue
        Multiprocess safe queue from which jobs to generate data is taken
    created_record_queue : Multiprocess Queue
        Multiprocess safe queue on which generated data is placed
    terminate_dequeued : Boolean
        Boolean flag which when True indicates the coordinator is to terminate

    Methods
    -------
    start(obj_class, pool_size)
        Begin the cycle of waiting for, formatting and running jobs. Continue
        this until termination instruction observed
    wait_for_jobs()
        Sleep whilst the generation queue is empty
    format_jobs(obj_class, pool_size)
        Retrieve jobs from queue and place them into an iterable structure
    issue_termination()
        Set flag to terminate to True
    run_jobs(job_list, pool_size)
        Pass formatted jobs to the generation pool for execution
    """

    def __init__(self, create_job_queue, created_record_queue):
        """ Assign variables from input, and set termination to False

        Parameters
        ----------
        create_job_queue : Multiprocessed Queue
            Queue containing jobs to generate an amount of domain objects
        created_record_queue : Multiprocessed Queue
            Queue containing resultant generated objects for writing to file
        """

        self.create_job_queue = create_job_queue
        self.created_record_queue = created_record_queue
        self.terminate_dequeued = False

    def start(self, object_factory):
        """ Begin the cycle of waiting for, formatting, and running jobs,
        continuing this until an instruction to terminate is observed.

        Parameters
        ----------
        object_factory : Creatable
            Instantiated and pre-configured object factory which produces
            the current object.
        """

        number_of_create_child_processes =\
            object_factory.get_shared_args()[
                'number_of_create_child_processes'
            ]

        # the maximum number of jobs to dequeue for processing is proportional
        # to the number of processes available to execute the jobs

        maximum_number_of_create_jobs_to_dequeue = \
            number_of_create_child_processes * 2

        while not self.terminate_dequeued:
            self.sleep_while_create_job_queue_empty()

            dequeued_create_jobs = self.get_dequeued_create_jobs(
                object_factory, maximum_number_of_create_jobs_to_dequeue
            )

            created_records_from_multiple_jobs = \
                pool_tasks.run_create_jobs(
                    dequeued_create_jobs, number_of_create_child_processes
                )

            self.created_record_queue.put(created_records_from_multiple_jobs)

        self.created_record_queue.put("terminate")

    def sleep_while_create_job_queue_empty(self):
        """ Sleep until jobs are on the queue """

        while self.create_job_queue.empty():
            time.sleep(1)

    def get_dequeued_create_jobs(
            self, object_factory, maximum_number_of_create_jobs_to_dequeue
    ):
        """ Takes jobs from the Multiprocess Safe Queue and places them into
        a list for later execution. If twice the pool size of jobs are
        formatted, then this list is returned. If the termination flag is
        observed, then this list is returned. If the queue is empty, then
        the list so far is returned.

        Parameters
        ----------
        object_factory : Creatable
            Instantiated and pre-configured object factory which produces
            the current object.
        maximum_number_of_create_jobs_to_dequeue : int
            the maximum number of jobs to dequeue for processing

        Returns
        -------
        List
            Containing jobs taken from the Queue. A list intermediary is
            required as multiprocessing pools require an iterable object,
            which a multiprocessing queue is not.
        """

        dequeued_create_jobs = []

        while not self.create_job_queue.empty() and len(dequeued_create_jobs) \
                < maximum_number_of_create_jobs_to_dequeue:

            create_job = self.create_job_queue.get()

            if create_job == "terminate":
                self.terminate_dequeued = True
            else:
                dequeued_create_jobs.append([create_job, object_factory])

        return dequeued_create_jobs
