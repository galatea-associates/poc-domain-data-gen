import time
import multi_processing.pool_tasks as mp_p


class Writer():
    """ A class to coordinate the writing of pre-generated records by
    compiling pre-generated records from a Multiprocessed Queue into larger
    sets such that files can be written in user-requested sizes.

    Attributes
    ----------
    write_queue : Multiprocessed Queue
        Contains results of the generation process. Each element is a list of
        lists of records.
    all_records : dict
        Dictionary containing all records so far received and not currently
        written to file.
    file_number : int
        The current file number to be writing to.
    max_size : int
        The maximum number of records in each output file.
    job_list : List
        List of jobs to be executed
    terminate : Boolean
        Boolean flag which when True indicates the coordinator is to terminate
    file_builder : File_Builder
        Instantiated file builder, pre-configured to output the necessary file
        extension.

    Methods
    -------
    start(pool_size)
        Begin the cycle of waiting for, handling and running jobs. Continue
        this until termination instruction observed
    wait_for_jobs()
        Sleeps until items are observed on the Multiprocessed Queue.
    handle_jobs(pool_size)
        Pulls an item from the Multiprocessed Queue if terminate, issues
        termination, otherwise passes the List containing lists of records
        to the format method.
    format_jobs(record_list)
        Splits jobs into object name & records, then adds to storage & issues
        instruction to calculate writes.
    get_job()
        Retrieve an item from the queue
    issue_termination()
        Set the termination flag to True
    add_to_stored_records(domain_object, records)
        Add observed data into a dictionary "Domain_Object : All_Records"
    calculate_writes()
        Calculate any writes to perform based on currently observed data
    get_file_num()
        Increment & return a value recording current file number
    run_jobs(pool_size)
        Execute the current job list on the write pool
    reset_job_list()
        Clear contents of the job list
    calculate_residual_writes()
        Calculate any remaining writes after terminate has been observed
    """

    def __init__(self, write_queue, max_file_size, file_builder):
        """ Assign write queue, maximum file size, and the file builder to
        use. Additionally, set starting/deafult values for all records,

        Parameters
        ----------
        write_queue : Multiprocessing Queue
            Shared, multiprocessing safe, queue holding lists of lists of
            records
        max_file_size : int
            Value representing the maximum number of records per file
        file_builder : File_Builder
            Instantiated file builder, pre-configured to output the necessary
            file extension.
        """

        self.write_queue = write_queue

        self.all_records = []
        self.file_number = 0
        self.max_size = int(max_file_size)

        self.job_list = []
        self.terminate = False
        self.file_builder = file_builder

    def start(self, pool_size):
        """ Begin the cycle of waiting for, handling, and running jobs,
        continuing this until an instruction to terminate is observed. Once
        observed, calculate any residual write to be made and terminate.

        Parameters
        ----------
        pool_size : int
            The number of processes running in the generator's pool
        """

        while not self.terminate:
            self.wait_for_jobs()
            self.handle_jobs(pool_size)
            self.run_jobs(pool_size)
            self.reset_job_list()

        self.calculate_residual_writes()
        self.run_jobs(pool_size)

    def wait_for_jobs(self):
        """ Sleep until records are on the queue """

        while self.write_queue.empty():
            time.sleep(1)
        return

    def handle_jobs(self, pool_size):
        """ Takes items from the Multiprocess safe queue, if a terminate
        instruction, the appropriate flag is set. If not, it must be a list
        of records, thus it formatted.

        Parameters
        ----------
        pool_size : int
            The number of processes running in the generator's pool
        """

        while (not self.write_queue.empty()
                and len(self.job_list) < pool_size*2):
            record_list = self.get_job()
            if (record_list == "terminate"):
                self.issue_termination()
            else:
                self.format_jobs(record_list)

    def format_jobs(self, record_list):
        """ Amalgamate all content from the record list into a single store.

        Parameters
        ----------
        record_list
            List of record lists, each arising from an individual writing
            process.
        """

        for job in record_list:
            domain_object = job[0]
            records = job[1]
            self.add_to_stored_records(domain_object, records)
            self.calculate_writes()

    def get_job(self):
        """ Return the record list at the front of the generate queue

        Returns
        -------
        list
            A list of lists. The primary list is a set of records as returned
            by a set of generation jobs executing on the generation job pool.
            Therefore, each contained list is the set of records generated by
            a single Process within the generation pool.
        """

        return self.write_queue.get()

    def issue_termination(self):
        """ Alter the termination flag to be True """

        self.terminate = True

    def add_to_stored_records(self, domain_object, records):
        """ From the dequeued list of lists of records, the record lists are
        amalgamated within a central store.

        Parameters
        ----------
        domain_object
            Name of the domain_object the data pertains to. TODO: Irrelevant
            information in this stage, remove this variable.
        records
            The List of lists of records.
        """

        for item in records:
            self.all_records.append(item)

    def calculate_writes(self):
        """ Calculates jobs from the currently dequeued information observed.
        For each chunk of stored records of size equal to the maximum file
        size, a new job is created and that data removed from primary store.
        The job is enqueued once created.
        """

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
        """ Return an incremented integer for sequentially named files

        Returns
        -------
        int
            The file number to be written next
         """

        cur = self.file_number
        self.file_number = cur+1
        return cur

    def run_jobs(self, pool_size):
        """ Pass a list of jobs to the job pool coordinator to be executed.
        Jobs contain the file number, the pre-instantiated file builder to
        use, as well as  the data itself.
        """

        mp_p.write(self.job_list, pool_size)

    def reset_job_list(self):
        """ Resets the list of records to be written out to file """

        self.job_list = []

    def calculate_residual_writes(self):
        """ Largely the same functionality as above calculation of writes, but
        where no jobs have been observed on the job queue. Forces the
        remaining data in the store to be written to file regardless of size.
        """

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
