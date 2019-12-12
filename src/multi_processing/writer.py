import time
from multi_processing import pool_tasks


class Writer:
    """ A class to coordinate the writing of pre-generated records by
    compiling pre-generated records from a Multiprocessed Queue into larger
    sets such that files can be written in user-requested sizes.

    Attributes
    ----------
    created_record_queue : Multiprocessed Queue
        Contains results of the generation process. Each element is a list of
        lists of records.
    all_records : dict
        Dictionary containing all records so far received and not currently
        written to file.
    file_number : int
        The current file number to be writing to.
    max_size : int
        The maximum number of records in each output file.
    write_jobs : List
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
    calculate_residual_writes()
        Calculate any remaining writes after terminate has been observed
    """

    def __init__(
            self, created_record_queue, max_records_per_file, file_builder
    ):
        """ Assign write queue, maximum file size, and the file builder to
        use. Additionally, set starting/deafult values for all records,

        Parameters
        ----------
        created_record_queue : Multiprocessing Queue
            Shared, multiprocessing safe, queue holding lists of lists of
            records
        max_records_per_file : int
            Value representing the maximum number of records per file
        file_builder : File_Builder
            Instantiated file builder, pre-configured to output the necessary
            file extension.
        """

        self.created_record_queue = created_record_queue
        self.dequeued_created_records_not_yet_written_to_file = []
        self.number_of_next_file_to_write = 0
        self.max_records_per_file = max_records_per_file
        self.write_jobs = []
        self.terminate_dequeued = False
        self.file_builder = file_builder

    def start(self, number_of_write_child_processes):
        """ Begin the cycle of waiting for, handling, and running jobs,
        continuing this until an instruction to terminate is observed. Once
        observed, calculate any residual write to be made and terminate.

        Parameters
        ----------
        number_of_write_child_processes : int
            The number of processes running in the generator's pool
        """

        maximum_number_of_write_jobs_to_create = \
            2 * number_of_write_child_processes

        while not self.terminate_dequeued:
            self.sleep_while_created_record_queue_empty()
            self.create_write_jobs(
                maximum_number_of_write_jobs_to_create
            )
            pool_tasks.run_write_jobs(
                self.write_jobs, number_of_write_child_processes
            )
            self.write_jobs = []

        if self.dequeued_created_records_not_yet_written_to_file:
            # list is not empty - there are some residual records remaining
            pool_tasks.run_write_jobs(
                [self.get_write_job()], number_of_write_child_processes
            )

    def sleep_while_created_record_queue_empty(self):
        """ Sleep until records are on the queue """

        while self.created_record_queue.empty():
            time.sleep(1)
        return

    def create_write_jobs(self, maximum_number_of_write_jobs_to_create):
        """ Takes items from the Multiprocess safe queue, if a terminate
        instruction, the appropriate flag is set. If not, it must be a list
        of records, thus it is formatted.

        Parameters
        ----------
        maximum_number_of_write_jobs_to_create : int
            The maximum number of write job to add to self.write_jobs
        """

        while not self.created_record_queue.empty() and \
                len(self.write_jobs) < maximum_number_of_write_jobs_to_create:
            dequeued_created_records = self.created_record_queue.get()
            if dequeued_created_records == "terminate":
                self.terminate_dequeued = True
            else:
                self.create_write_jobs_from_dequeued_records(
                    dequeued_created_records
                )

    def create_write_jobs_from_dequeued_records(
            self, dequeued_created_records
    ):
        """ Amalgamate all content from the record list into a single store.

        Parameters
        ----------
        dequeued_created_records
            List of record lists, each arising from an individual writing
            process.
        """

        for list_of_created_records in dequeued_created_records:
            self.dequeued_created_records_not_yet_written_to_file.extend(
                list_of_created_records
            )
            if len(self.dequeued_created_records_not_yet_written_to_file) \
                    >= self.max_records_per_file:
                self.write_jobs.append(self.get_write_job())

    def get_write_job(self):
        """ Calculates jobs from the currently dequeued information observed.
        For each chunk of stored records of size equal to the maximum file
        size, a new job is created and that data removed from primary store.
        The job is enqueued once created.
        """

        number_of_records = min(
            self.max_records_per_file, len(
                self.dequeued_created_records_not_yet_written_to_file
            )
        )

        write_job = {
            'file_number': self.number_of_next_file_to_write,
            'file_builder': self.file_builder,
            'records': self.dequeued_created_records_not_yet_written_to_file[
                       :number_of_records
                       ]
        }

        self.number_of_next_file_to_write += 1

        del self.dequeued_created_records_not_yet_written_to_file[
            :number_of_records
            ]

        return write_job
