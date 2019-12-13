""" Pool Manager for both Creation and Writing tasks. Two methods are
responsible for each, a catch-all generate/write method which configures
the Pool for jobs to be executed on. Additionally included are methods the
pools use for each job in their respective job lists to perform the actual
generation/writing tasks.
"""

from multiprocessing import Pool, Lock


def run_create_jobs(
        dequeued_create_jobs, number_of_create_child_processes
):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    dequeued_create_jobs : list
        List of create jobs taken from the create job queue
    number_of_create_child_processes : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.

    Returns
    -------
    List
        List of lists, each contained list is a set of generated records due
        to be written to file.
    """

    local_lock = Lock()
    create_pool = Pool(
        processes=number_of_create_child_processes,
        initializer=make_global,
        initargs=(local_lock,)
    )
    # execute all jobs, placing the result of each job in a list
    # this returns a list of lists, each list containing the records from
    # one create job
    created_records_from_multiple_jobs = create_pool.map(
        create_records_from_create_job, dequeued_create_jobs
    )

    create_pool.close()
    create_pool.join()

    return created_records_from_multiple_jobs


def make_global(local_lock):
    global lock
    lock = local_lock


def create_records_from_create_job(create_job):
    """ Generates a single set of records based on an individual job.

    Instruction contains the number of records to generate, or the number of
    records to retrieve from the database (in the case of dependent objects),
    as well as the starting ID for this set in the case of sequential IDs.

    Where objects are generated in nondeterministic amounts, sequential IDs
    are not possible.

    Parameters
    ----------
    create_job : list
        List of 2 elements, firstly, the production instructions for objects:
        quantity to produce and the id to start generation from. The second
        element is the instantiated factory.

    Returns
    -------
    list
        List containing all the records produced by this factory for this
        instruction set.
    """

    instructions, object_factory = create_job

    quantity, start_id = instructions['quantity'], instructions['start_id']

    if object_factory.__class__.__name__ == "InstrumentFactory":
        created_records = object_factory.create(quantity, start_id, lock=lock)
    else:
        created_records = object_factory.create(quantity, start_id)

    return created_records


def run_write_jobs(write_jobs, number_of_write_child_processes):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    write_jobs : list
        Jobs to be executed on the
    number_of_write_child_processes : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.
    """

    pool = Pool(number_of_write_child_processes)
    pool.map(build_file_from_write_job, write_jobs)
    pool.close()
    pool.join()


def build_file_from_write_job(write_job):
    """ Writes a single file of data based on the provided records.
    Parameters
    ----------
    write_job : dict
        Contains the file number, for sequential ordering. Contains the
        instantiated file builder, pre-configured to output the necessary
        file extension. Contains the records to be written to file.
    """
    file_number, file_builder, records = write_job['file_number'], \
        write_job['file_builder'], write_job['records']

    file_builder.build(file_number, records)
