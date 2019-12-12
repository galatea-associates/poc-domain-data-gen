from multiprocessing import Manager, Process
from multi_processing.creator import Creator
from multi_processing.writer import Writer
import math

# Class to coordinate the multiprocessing implementation. It is
# required to abstract the multiprocessing logic from any unpickleable
# objects, such as the database connection.


class Coordinator:
    """ Coordination class for the multiprocessing implementation. Required
    to abstract multiprocessing calls from unpickleable objects in the main
    program, such as database connections. Holds, instantiates and passes job
    queues to generation and writing processes, additionally starts these.

    Attributes
    ----------
    create_job_queue : Multiprocessing Queue
        Multiprocessing-safe, holds jobs for the generation process to format
        and execute.
    created_record_queue : Multiprocessing Queue
        Multiprocessing-safe, holds jobs for the writing process to format and
        execute.
    create_coordinator : Creator
        Holds both queues to take jobs from the former, and put the results of
        such in the latter.
    write_coordinator : Writer
        Holds writing job queue, taking jobs from which and formatting them
        before writing files of the user-given size.
    parent_processes : list
        Adds started processes (Creator and Writer) for the purpose of
        knowing once they're finished.

    Methods
    -------
    create_jobs(domain_obj, quantity, job_size)
        Populate the generation job queue with jobs

    start_generator(obj_class, pool_size)
        Begin the generation coordinator as a subprocess, with job pool size

    start_writer(pool_size)
        Begin the writing coordinator as a subprocess, with job pool size

    get_create_coordinator()
        Return the generation coordinator

    get_write_coordinator()
        Return the write coordinator

    await_termination()
        Wait for generation & write coordinators to terminate
    """

    def __init__(self, file_builder, object_factory):
        """Create Job Queues for both generation and file writing processes.
        Instantiate the coordinating process for both, by default not running
        until their "start" methods are called.

        Parameters
        ----------
        file_builder : File_Builder
            Instantiated and pre-configured file builder to write files of
            the necessary format.
        object_factory : Creatable
            Instantiated and pre-configured object factory which produces
            the current object.
        """

        queue_manager = Manager()
        self.__create_job_queue = queue_manager.Queue()
        self.__created_record_queue = queue_manager.Queue()

        self.__create_coordinator = Creator(
            self.__create_job_queue,
            self.__created_record_queue
        )

        self.__write_coordinator = Writer(
            self.__created_record_queue,
            file_builder.get_max_objects_per_file(),
            file_builder
        )

        self.object_factory = object_factory
        self.__parent_processes = []

    def populate_create_job_queue(self):
        """Populate the generation queue with jobs.

        Continually places jobs into the queue, counting down record_count,
        the number of records of this object to produce, until it's value is 0

        A job is a 2-element dictionary. Quantity and Start_ID are arguments
        for the factories generate call. Quantity  informs as to the number of
        objects to produce. Start_ID keeps track of the batch of IDs the job
        will be producing in the case of sequentially ID'd domain objects.

        A termination flag is added to the queue last. This informs the
        generation process to stop awaiting instruction once read, causing
        it to terminate once the currently-running jobs have ceased.
        """

        number_of_records_to_create = self.object_factory.get_record_count()
        number_of_records_per_job = self.object_factory.get_shared_args()[
            'number_of_records_per_job'
        ]
        number_of_create_jobs_to_queue = math.ceil(
            number_of_records_to_create / number_of_records_per_job
        )

        number_of_records_without_create_jobs = number_of_records_to_create

        for index in range(number_of_create_jobs_to_queue):
            quantity = min(
                number_of_records_without_create_jobs,
                number_of_records_per_job
            )
            start_id = index * number_of_records_per_job
            create_job = {
                'quantity': quantity,
                'start_id': start_id
            }
            self.__create_job_queue.put(create_job)
            number_of_records_without_create_jobs -= quantity

        self.__create_job_queue.put("terminate")

    def start_creator(self):
        """ Start the creator coordinator as a process """

        creator_parent_process = Process(
            target=self.__create_coordinator.start,
            args=(self.object_factory,)
        )
        creator_parent_process.start()
        self.__parent_processes.append(creator_parent_process)

    def start_writer(self):
        """ Starts the writing coordinator as a process """

        number_of_write_child_processes =\
            self.object_factory.get_shared_args()[
                'number_of_write_child_processes'
            ]

        writer_parent_process = Process(
            target=self.__write_coordinator.start,
            args=(number_of_write_child_processes,)
        )
        writer_parent_process.start()
        self.__parent_processes.append(writer_parent_process)

    def join_parent_processes(self):
        """Waits for spawned child_processes to terminate."""
        for process in self.__parent_processes:
            process.join()
