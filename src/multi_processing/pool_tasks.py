""" Pool Manager for both Generation and Writing tasks. Two methods are
responsible for each, a catch-all generate/write method which configures
the Pool for jobs to be executed on. Additionally included are methods the
pools use for each job in their respective job lists to perform the actual
generation/writing tasks.
"""

from multiprocessing import Pool, Lock


def generate(job_list, pool_size):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    job_list : list
        Jobs to be executed on the
    pool_size : int
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
        processes=pool_size,
        initializer=make_global,
        initargs=(local_lock,)
    )
    generated_records = generate_pool.map(
        generate_data, job_list
    )
    generate_pool.close()
    generate_pool.join()
    return generated_records


def make_global(local_lock):
    global lock
    lock = local_lock


def generate_data(job):
    """ Generates a single set of records based on an individual job.

    Instruction contains the number of records to generate, or the number of
    records to retrieve from the database (in the case of dependent objects),
    as well as the starting ID for this set in the case of sequential IDs.

    Where objects are generated in nondeterministic amounts, sequential IDs
    are not possible.

    Parameters
    ----------
    job : list
        List of 2 elements, firstly, the production instructions for objects:
        quantity to produce and the id to start generation from. The second
        element is the instantiated factory.

    Returns
    -------
    list
        List containing all the records produced by this factory for this
        instruction set.
    """

    instructions = job[0]
    object_factory = job[1]

    quantity = instructions['quantity']
    start_id = instructions['start_id']

    if object_factory.__class__.__name__ == "InstrumentFactory":
        records = object_factory.create(quantity, start_id, lock=lock)
    else:
        records = object_factory.create(quantity, start_id)

    return records


def write(job_list, pool_size):
    """ Instantiates a job Pool for user-defined size, and begins execution
    of provided jobs on the pool.

    Parameters
    ----------
    job_list : list
        Jobs to be executed on the
    pool_size : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.
    """

    pool = Pool(pool_size)
    pool.map(write_data, job_list)
    pool.close()
    pool.join()


def write_data(job):
    """ Writes a single file of data based on the provided records.

    Parameters
    ----------
    job : dict
        Contains the file number, for sequential ordering. Contains the
        instantiated file builder, pre-configured to output the necessary
        file extension. Contains the records to be written to file.
    """
    file_number = job['file_number']
    file_builder = job['file_builder']
    records = job['records']

    file_builder.build(file_number, records)
