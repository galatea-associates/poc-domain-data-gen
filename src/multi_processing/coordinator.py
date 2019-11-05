from multiprocessing import Manager, Process
from multi_processing.generator import Generator
from multi_processing.writer import Writer

# Class to coordinate the multiprocessing implementation. It is
# required to abstract the multiprocessing logic from any unpickleable
# objects, such as the database connection.


class Coordinator():
    """ Coordination class for the multiprocessing implementation. Required
    to abstract multiprocessing calls from unpickleable objects in the main
    program, such as database connections. Holds, instantiates and passes job
    queues to generation and writing processes, additionally starts these.

    Attributes
    ----------
    generation_job_queue : Multiprocessing Queue
        Multiprocessing-safe, holds jobs for the generation process to format
        and execute.
    write_job_queue : Multiprocessing Queue
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

    start_generator(obj_class, pool_size)
        Begin the generation coordinator as a subprocess, with job pool size

    start_writer(pool_size)
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
        object_factory : Generatable
            Instantiated and pre-configured object factory which produces
            the current object. 
        """

        queue_manager = Manager()
        self.__generation_job_queue = queue_manager.Queue()
        self.__write_job_queue = queue_manager.Queue()

        self.__generation_coordinator = Generator(
            self.__generation_job_queue,
            self.__write_job_queue
        )

        self.__write_coordinator = Writer(
            self.__write_job_queue,
            file_builder.get_max_objects_per_file(),
            file_builder
        )

        self.object_factory = object_factory
        self.processes = []

    def create_jobs(self):
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
        record_count = self.object_factory.get_record_count()
        job_size = self.object_factory.get_shared_args()['pool_job_size']

        while record_count > 0:
            if record_count > job_size:
                job = {'quantity': job_size,
                       'start_id': start_id}
                record_count = record_count - job_size
                start_id = start_id + job_size
            else:
                job = {'quantity': record_count,
                       'start_id': start_id}
                record_count = 0
            self.__generation_job_queue.put(job)

        self.__generation_job_queue.put("terminate")

    def start_generator(self):
        """ Start the generation coordinator as a subprocess """

        generator_p = Process(target=self.get_generation_coordinator().start,
                              args=(self.object_factory,))
        generator_p.start()
        self.processes.append(generator_p)

    def start_writer(self):
        """ Starts the writing coordinator as a subprocess """

        writer_pool_size =\
            self.object_factory.get_shared_args()['writer_pool_size']

        writer_p = Process(target=self.get_write_coordinator().start,
                           args=(writer_pool_size,))
        writer_p.start()
        self.processes.append(writer_p)

    def get_generation_coordinator(self):
        """
        Returns
        -------
        Generator
            Instantiated Generator class, handles generation of domain objects
        """

        return self.__generation_coordinator

    def get_write_coordinator(self):
        """
        Returns
        -------
        Writer
            Instantiated Writer class, handles writing of domain objects to
            file
        """

        return self.__write_coordinator

    def await_termination(self):
        """Waits for spawned subprocesses to terminate."""
        for process in self.processes:
            process.join()
