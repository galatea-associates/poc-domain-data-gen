import time
import multi_processing.pool_tasks as pool_tasks


class Writer:
    """ A class to coordinate the writing of pre-generated records by
    compiling pre-generated records from a Multiprocessed Queue into larger
    sets such that files can be written in user-requested sizes.

    Attributes
    ----------
    queue_of_generated_records : Multiprocessed Queue
        Contains results of the generation process. Each element is a list of
        lists of records.
    all_records : dict
        Dictionary containing all records so far received and not currently
        written to file.
    file_number : int
        The current file number to be writing to.
    max_records_per_file : int
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
    start(number_of_write_processes_per_pool)
        Begin the cycle of waiting for, handling and running jobs. Continue
        this until termination instruction observed
    wait_for_jobs()
        Sleeps until items are observed on the Multiprocessed Queue.
    handle_jobs(number_of_write_processes_per_pool)
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
    run_jobs(number_of_write_processes_per_pool)
        Execute the current job list on the write pool
    reset_job_list()
        Clear contents of the job list
    calculate_residual_writes()
        Calculate any remaining writes after terminate has been observed
    """

    def __init__(
            self, queue_of_generated_records, max_records_per_file,
            file_builder
    ):
        """ Assign write queue, maximum file size, and the file builder to
        use. Additionally, set starting/deafult values for all records,

        Parameters
        ----------
        queue_of_generated_records : Multiprocessing Queue
            Shared, multiprocessing safe, queue holding lists of lists of
            records
        max_records_per_file : int
            Value representing the maximum number of records per file
        file_builder : File_Builder
            Instantiated file builder, pre-configured to output the necessary
            file extension.
        """

        self.queue_of_generated_records = queue_of_generated_records
        self.list_of_dequeued_generated_records = []
        self.list_of_write_jobs = []
        self.file_number = 0
        self.max_records_per_file = max_records_per_file
        self.terminate_job_dequeued = False
        self.file_builder = file_builder

    def start(self, number_of_write_processes_per_pool):
        """ Begin the cycle of waiting for, handling, and running jobs,
        continuing this until an instruction to terminate is observed. Once
        observed, calculate any residual write to be made and terminate.

        Parameters
        ----------
        number_of_write_processes_per_pool : int
            The number of processes running in the write pool
        """

        maximum_length_of_write_job_list = \
            2 * number_of_write_processes_per_pool

        while not self.terminate_job_dequeued:
            self.sleep_until_records_generated()
            self.create_write_jobs(
                maximum_length_of_write_job_list
            )
            pool_tasks.execute_write_jobs(
                self.list_of_write_jobs, number_of_write_processes_per_pool
            )
            self.list_of_write_jobs = []

        self.calculate_residual_writes()
        pool_tasks.execute_write_jobs(
            self.list_of_write_jobs, number_of_write_processes_per_pool
        )

    def sleep_until_records_generated(self):
        """ Sleep until records are on the queue """

        while self.queue_of_generated_records.empty():
            time.sleep(1)
        return

    def create_write_jobs(
            self, maximum_length_of_write_job_list
    ):
        """ Takes items from the Multiprocess safe queue, if a terminate
        instruction, the appropriate flag is set. If not, it must be a list
        of records, thus it is formatted.

        Parameters
        ----------
        maximum_length_of_write_job_list : int
            Max length the job list can reach before it is added to the queue
        """

        while not self.queue_of_generated_records.empty() and \
                len(self.list_of_write_jobs) < \
                maximum_length_of_write_job_list:
            list_of_lists_of_generated_records = \
                self.queue_of_generated_records.get()
            if list_of_lists_of_generated_records == "terminate":
                self.terminate_job_dequeued = True
            else:
                self.update_list_of_dequeued_generated_records(
                    list_of_lists_of_generated_records
                )

    def update_list_of_dequeued_generated_records(
            self, list_of_lists_of_generated_records
    ):
        """ Amalgamate all content from the record list into a single store.

        Parameters
        ----------
        list_of_lists_of_generated_records
            List of record lists, each arising from an individual writing
            process.
        """

        for list_of_generated_records in list_of_lists_of_generated_records:
            self.list_of_dequeued_generated_records.append(
                list_of_generated_records
            )
            self.update_list_of_write_jobs()

    def update_list_of_write_jobs(self):
        """ Calculates jobs from the currently dequeued information observed.
        For each chunk of stored records of size equal to the maximum file
        size, a new job is created and that data removed from primary store.
        The job is enqueued once created.
        """

        # self.max_records_per_file indicates largest file size
        # self.all_records contains all records currently received

        if len(self.list_of_dequeued_generated_records) > \
                self.max_records_per_file:
            records = self.list_of_dequeued_generated_records[
                      :self.max_records_per_file
                      ]
            del self.list_of_dequeued_generated_records[
                :self.max_records_per_file
                ]
            write_job = {
                'file_number': self.file_number,
                'file_builder': self.file_builder,
                'records': records
            }
            self.list_of_write_jobs.append(write_job)
            self.file_number += 1

    def calculate_residual_writes(self):
        """ Largely the same functionality as above calculation of writes, but
        where no jobs have been observed on the job queue. Forces the
        remaining data in the store to be written to file regardless of size.
        """

        write_job = {
            'file_number': self.file_number,
            'file_builder': self.file_builder,
            'records': self.list_of_dequeued_generated_records
        }

        self.list_of_write_jobs.append(write_job)
        self.list_of_dequeued_generated_records = []
