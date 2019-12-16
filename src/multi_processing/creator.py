import time
from multi_processing import pool_tasks


class Creator:
    """ A class to coordinate the creation of domain objects as per jobs
    observed within a multiprocessed queue. Create jobs are sequentially
    dequeued in batches and run over a pool of child processes, returning a
    list containing all created records from the jobs in that batch.

    Attributes
    ----------
    create_job_queue : Multiprocess Queue
        Multiprocess safe queue from which jobs to create records are taken
    created_record_queue : Multiprocess Queue
        Multiprocess safe queue into which lists of created records are placed
    terminate_dequeued : Boolean
        Boolean flag which when True indicates the coordinator is to terminate

    Methods
    -------
    parent_process(object_factory)
        Until the "terminate" flag is dequeued, cycle through a loop that waits
        until the create job queue is not empty, then dequeues and runs a batch
        of jobs, and puts a list of created records from that batch onto the
        created record queue.
    sleep_while_create_job_queue_empty()
        Sleep whilst the create job queue is empty
    get_dequeued_create_jobs(maximum_number_of_create_jobs_to_dequeue)
        Return a list containing a batch of jobs dequeued from the create job
        queue such that they can be run over a pool of child processes
    """

    def __init__(self, create_job_queue, created_record_queue):
        """ Assign variables from input, and set termination to False

        Parameters
        ----------
        create_job_queue : Multiprocessed Queue
            Queue containing jobs to create a certain quantity of domain
            objects
        created_record_queue : Multiprocessed Queue
            Queue containing resultant created records for writing to file
        """

        self.create_job_queue = create_job_queue
        self.created_record_queue = created_record_queue
        self.terminate_dequeued = False

    def parent_process(self, object_factory):
        """ Begin the cycle of waiting for, formatting, and running jobs,
        continuing this until an instruction to terminate is observed.

        Parameters
        ----------
        object_factory : Creatable
            Instantiated and pre-configured object factory used to create
            records from create jobs
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
                maximum_number_of_create_jobs_to_dequeue
            )

            created_records_from_multiple_jobs = \
                pool_tasks.run_create_jobs(
                    dequeued_create_jobs,
                    number_of_create_child_processes,
                    object_factory
                )

            self.created_record_queue.put(created_records_from_multiple_jobs)

        self.created_record_queue.put("terminate")

    def sleep_while_create_job_queue_empty(self):
        """ Sleep until jobs are on the queue """

        while self.create_job_queue.empty():
            time.sleep(1)

    def get_dequeued_create_jobs(
            self, maximum_number_of_create_jobs_to_dequeue
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
                dequeued_create_jobs.append(create_job)

        return dequeued_create_jobs
