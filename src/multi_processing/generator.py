import time
import multi_processing.pool_tasks as mp_p


class Generator():
    """ A class to coordinate the generation of domain objects as per jobs
    observed within a multiprocessed queue. Data is then generated in a pool
    before the result of which is put into the write queue.

    Attributes
    ----------
    generate_queue : Multiprocess Queue
        Multiprocess safe queue from which jobs to generate data is taken
    write_queue : Multiprocess Queue
        Multiprocess safe queue on which generated data is placed
    terminate : Boolean
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
    get_generation_queue()
        Return a pointer to the multiprocess safe generation job queue
    """

    def __init__(self, generate_queue, write_queue):
        """ Assign variables from input, and set termination to False

        Parameters
        ----------
        generate_queue : Multiprocessed Queue
            Queue containing jobs to generate an amount of domain objects
        write_queue : Multiprocessed Queue
            Queue containing resultant generated objects for writing to file
        """

        self.generate_queue = generate_queue
        self.write_queue = write_queue
        self.terminate = False

    def start(self, object_factory):
        """ Begin the cycle of waiting for, formatting, and running jobs,
        continuing this until an instruction to terminate is observed.

        Parameters
        ----------
        obj_class : String
            For keeping track of which domain object is being generated
        pool_size : int
            The number of processes running in the generator's pool
        """

        generation_pool_size =\
            object_factory.get_shared_args()['generator_pool_size']

        while not self.terminate:
            self.wait_for_jobs()
            job_list = self.format_jobs(object_factory, generation_pool_size)
            self.run_jobs(job_list, generation_pool_size)

        self.write_queue.put("terminate")

    def wait_for_jobs(self):
        """ Sleep until jobs are on the queue """

        while self.generate_queue.empty():
            time.sleep(1)
        return

    def format_jobs(self, object_factory, generation_pool_size):
        """ Takes jobs from the Multiprocess Safe Queue and places them into
        a list for later execution. If twice the pool size of jobs are
        formatted, then this list is returned. If the termination flag is
        observed, then this list is returned. If the queue is empty, then
        the list so far is returned.

        Parameters
        ----------
        obj_class : String
            For keeping track of which domain object is being generated
        pool_size : int
            The number of processes running in the generator's pool

        Returns
        -------
        List
            Containing jobs taken from the Queue. A list intermediary is
            required as multiprocessing pools require an iterable object,
            which a multiprocessing queue is not.
        """

        job_list = []
        while (not self.generate_queue.empty()
                and len(job_list) < (generation_pool_size*2)):
            job = self.get_job()
            if (job == "terminate"):
                self.issue_termination()
            else:
                job_list.append([job, object_factory])
        return job_list

    def get_job(self):
        """ Return the job at the front of the generate queue

        Returns
        -------
        dict
            As defined within coordinator, a job dictionary containing an
            instantiated object class, the amount to generate, and the id
            from which generation is to commence.
        """

        return self.generate_queue.get()

    def issue_termination(self):
        """ Alter the termination flag to be True """
        self.terminate = True

    def run_jobs(self, job_list, pool_size):
        """ Pass a list of jobs to the multiprocessing pool scripts generate
        method. This instantiates a pool and begins execution of the provided
        list of jobs on it. The returned generated data is then placed on the
        write queue.

        Parameters
        ----------
        job_list : List
            Containing jobs to be ran over a Pool
        pool_size : int
            The size of pool on which to execute the job list
        """

        records = mp_p.generate(job_list, pool_size)
        self.write_queue.put(records)

    def get_generation_queue(self):
        """Return the generation queue

        Returns
        -------
        Multiprocessed Queue
            Contains the generation jobs yet to execute
        """
        return self.generate_queue
