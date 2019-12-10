""" Pool Manager for both Generation and Writing tasks. Two methods are
responsible for each, a catch-all generate/write method which configures
the Pool for jobs to be executed on. Additionally included are methods the
pools use for each job in their respective job lists to perform the actual
generation/writing tasks.
"""

from multiprocessing import Pool, Lock


def execute_generate_jobs(
        list_of_generate_jobs, number_of_generate_processes_per_pool
):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    list_of_generate_jobs : list
        Jobs to be executed on the
    number_of_generate_processes_per_pool : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.

    Returns
    -------
    List
        List of lists, each contained list is a set of generated records due
        to be written to file.
    """
    local_lock = Lock()
    generate_pool = Pool(
        processes=number_of_generate_processes_per_pool,
        initializer=make_global,
        initargs=(local_lock,)
    )
    generated_records = generate_pool.map(
        create_records_from_generate_job, list_of_generate_jobs
    )
    generate_pool.close()
    generate_pool.join()
    return generated_records


def make_global(local_lock):
    global lock
    lock = local_lock


def create_records_from_generate_job(generate_job):
    """ Generates a single set of records based on an individual job.

    Instruction contains the number of records to generate, or the number of
    records to retrieve from the database (in the case of dependent objects),
    as well as the starting ID for this set in the case of sequential IDs.

    Parameters
    ----------
    generate_job : list
        List of 2 elements, firstly, the production instructions for objects:
        quantity to produce and the id to start generation from. The second
        element is the instantiated factory.

    Returns
    -------
    list
        List containing all the records produced by this factory for this
        instruction set.
    """

    instructions, object_factory = generate_job

    quantity = instructions['quantity']
    start_id = instructions['start_id']
    if object_factory.__class__.__name__ == "InstrumentFactory":
        records = object_factory.create(quantity, start_id, lock=lock)
    else:
        records = object_factory.create(quantity, start_id)

    return records


def execute_write_jobs(list_of_write_jobs, number_of_write_processes_per_pool):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    list_of_write_jobs : list
        Jobs to be executed on the
    number_of_write_processes_per_pool : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.
    """

    pool = Pool(number_of_write_processes_per_pool)
    pool.map(build_file_from_write_job, list_of_write_jobs)
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
    file_number = write_job['file_number']
    file_builder = write_job['file_builder']
    records = write_job['records']

    file_builder.build(file_number, records)
