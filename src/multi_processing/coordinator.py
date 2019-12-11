from multiprocessing import Manager, Process
from multi_processing.generator import Generator
from multi_processing.writer import Writer

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
    queue_of_generation_jobs : Multiprocessing Queue
        Multiprocessing-safe, holds jobs for the generation process to format
        and execute.
    queue_of_generated_records : Multiprocessing Queue
        Multiprocessing-safe, holds jobs for the writing process to format and
        execute.
    generation_coordinator : Generator
        Holds both queues to take jobs from the former, and put the results of
        such in the latter.
    write_coordinator : Writer
        Holds writing job queue, taking jobs from which and formatting them
        before writing files of the user-given size.
    processes : list
        Adds started processes (Generator and Writer) for the purpose of
        knowing once they're finished.

    Methods
    -------
    create_jobs(domain_obj, quantity, job_size)
        Populate the generation job queue with jobs

    start_generator(obj_class, number_of_generate_processes_per_pool)
        Begin the generation coordinator as a subprocess, with job pool size

    start_writer(number_of_write_processes_per_pool)
        Begin the writing coordinator as a subprocess, with job pool size

    get_generation_coordinator()
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
        self.__queue_of_generation_jobs = queue_manager.Queue()
        self.__queue_of_generated_records = queue_manager.Queue()

        self.__generator = Generator(
            self.__queue_of_generation_jobs,
            self.__queue_of_generated_records
        )

        self.__writer = Writer(
            self.__queue_of_generated_records,
            file_builder.get_max_objects_per_file(),
            file_builder
        )

        self.object_factory = object_factory
        self.processes = []

    def add_jobs_to_generation_queue(self):
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

        start_id = 0
        number_of_records_not_yet_queued = \
            self.object_factory.get_record_count()
        number_of_records_per_job = \
            self.object_factory.get_shared_args()['number_of_records_per_job']

        while number_of_records_not_yet_queued > 0:
            if number_of_records_not_yet_queued > number_of_records_per_job:
                quantity = number_of_records_per_job
            else:
                quantity = number_of_records_not_yet_queued

            generate_job = {
                'quantity': quantity,
                'start_id': start_id
            }
            start_id += quantity
            number_of_records_not_yet_queued -= quantity
            self.__queue_of_generation_jobs.put(generate_job)

        self.__queue_of_generation_jobs.put("terminate")

    def start_generator_process(self):
        """ Start the generation coordinator as a subprocess """

        generator_process = Process(
            target=self.get_generator().start,
            args=(self.object_factory,)
        )
        generator_process.start()
        self.processes.append(generator_process)

    def start_write_process(self):
        """ Starts the writing coordinator as a subprocess """

        number_of_write_processes_per_pool =\
            self.object_factory.get_shared_args()[
                'number_of_write_processes_per_pool'
            ]

        writer_process = Process(
            target=self.get_writer().start,
            args=(number_of_write_processes_per_pool,)
        )
        writer_process.start()
        self.processes.append(writer_process)

    def get_generator(self):
        """
        Returns
        -------
        Generator
            Instantiated Generator class, handles generation of domain objects
        """

        return self.__generator

    def get_writer(self):
        """
        Returns
        -------
        Writer
            Instantiated Writer class, handles writing of domain objects to
            file
        """

        return self.__writer

    def await_termination(self):
        """Waits for spawned subprocesses to terminate."""
        for process in self.processes:
            process.join()
