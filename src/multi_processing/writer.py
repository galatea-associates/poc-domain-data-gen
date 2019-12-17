import time
from multi_processing import pool_tasks


class Writer:
    """ A class to coordinate the writing of created records by
    compiling pre-generated records from a Multiprocessed Queue into larger
    sets such that files can be written in user-requested sizes.

    The write parent process waits until the 'generated_record_queue' is not
    empty, at which point it retrieves lists of records from the queue and
    collates all records from those lists into a
    'dequeued_created_records_not_yet_written_to_file' list.

    It then creates a list of 'write jobs', each of which is a dictionary
    containing a portion of the records from the
    'dequeued_created_records_not_yet_written_to_file' list to write to file,
    and the ID of the output file. A single output file can have multiple
    'write jobs', but a 'write job' can only refer to one output file.

    The 'write jobs' in the list are run over a pool of child write processes,
    which build the output files then terminate. Upon termination of all
    processes, the 'write job' list is emptied and the next iteration begins by
    dequeuing any further records from the 'generated_record_queue'.

    Attributes
    ----------
    created_record_queue : Multiprocessed Queue
        Contains results of the generation process. Each element is a list of
        lists of records.
    dequeued_created_records_not_yet_written_to_file : list
        list collating all records dequeued from the created record queue that
        have not yet been written to file
    number_of_next_file_to_write : int
        The current file number to be writing to.
    max_records_per_file : int
        The maximum number of records in each output file.
    write_jobs : list
        List of jobs to be run
    terminate_dequeued : boolean
        Boolean flag which when True indicates the coordinator is to terminate
    file_builder : FileBuilder
        Instantiated file builder, pre-configured to output the necessary file
        extension.

    Methods
    -------
    parent_process()
        Begin the cycle of waiting for, handling and running jobs. Continue
        this until termination instruction observed
    sleep_while_created_record_queue_empty()
        Sleeps until items are observed on the Multiprocessed Queue.
    create_write_jobs()
        Takes items from the created records queue and adds write jobs to
        the write jobs list representing these records. If a terminate
        instruction is dequeued, the appropriate flag is set.
    get_write_job()
        Create a single write job representing the records at the front of
        the 'dequeued_created_records_not_yet_written_to_file' list. Delete
        these records from the list, then return the write job.
    """

    def __init__(
            self, created_record_queue, max_records_per_file, file_builder
    ):
        """ Initialise instance attributes.

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

    def parent_process(self, number_of_write_child_processes):
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
                self.write_jobs,
                number_of_write_child_processes,
                self.file_builder
            )
            self.write_jobs = []

        if self.dequeued_created_records_not_yet_written_to_file:
            # list is not empty - there are some residual records remaining
            pool_tasks.run_write_jobs(
                [self.get_write_job()],
                number_of_write_child_processes,
                self.file_builder
            )

    def sleep_while_created_record_queue_empty(self):
        """ Sleep until records are on the queue """

        while self.created_record_queue.empty():
            time.sleep(1)
        return

    def create_write_jobs(self, maximum_number_of_write_jobs_to_create):
        """ Takes items from the created records queue and adds write jobs to
        the write jobs list representing these records. If a terminate
        instruction is dequeued, the appropriate flag is set.

        Parameters
        ----------
        maximum_number_of_write_jobs_to_create : int
            The maximum number of write jobs to add to self.write_jobs
        """

        while not self.created_record_queue.empty() and \
                len(self.write_jobs) < maximum_number_of_write_jobs_to_create:

            dequeued_created_records = self.created_record_queue.get()

            if dequeued_created_records == "terminate":
                self.terminate_dequeued = True
            else:
                self.dequeued_created_records_not_yet_written_to_file.extend(
                    dequeued_created_records
                )
                while len(
                        self.dequeued_created_records_not_yet_written_to_file
                ) >= self.max_records_per_file:
                    self.write_jobs.append(self.get_write_job())

    def get_write_job(self):
        """ Create a single write job representing the records at the front of
        the 'dequeued_created_records_not_yet_written_to_file' list. Delete
        these records from the list, then return the write job.
        """

        number_of_records = min(
            self.max_records_per_file, len(
                self.dequeued_created_records_not_yet_written_to_file
            )
        )

        write_job = {
            'file_number': self.number_of_next_file_to_write,
            'records': self.dequeued_created_records_not_yet_written_to_file[
                       :number_of_records
                       ]
        }

        self.number_of_next_file_to_write += 1

        del self.dequeued_created_records_not_yet_written_to_file[
            :number_of_records
            ]

        return write_job
