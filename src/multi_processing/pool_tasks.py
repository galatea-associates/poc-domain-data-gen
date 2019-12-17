""" Pool Manager functionality for both create and write parent processes.

The create parent process executes the 'parent_process' method of the Creator
class, which prepares a batch of 'create jobs' then calls the 'run_create_jobs'
method of this module to run them over a pool of child processes.

The write parent process similarly executes the 'parent_process' method of the
Writer class, which waits until the parent process of the Creator class has run
'create jobs' to produce records, then dequeues these created records and
assigns them to 'write jobs' which are stored in a list.

'Write jobs' are run by being passed to file builder objects to be written to
file, and are run in batches over a pool of write child processes.
"""

from multiprocessing import Pool, Lock


def run_create_jobs(
        dequeued_create_jobs, number_of_create_child_processes, object_factory
):
    """ Instantiates a Pool with a number of processes as given in the user
    config by the 'number_of_create_child_processes' line, and begins execution
    of the provided batch of 'create jobs' on the pool.

    Parameters
    ----------
    dequeued_create_jobs : list
        List of create jobs taken from the create job queue
    number_of_create_child_processes : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.
    object_factory : Creatable
        Instantiated subclass of Creatable to be used to create records using
        its create method

    Returns
    -------
    List
        List of created records collated from the results of each 'create job'.
    """

    # multiprocessing lock used to define critical section in the
    # InstrumentFactory class
    local_lock = Lock()
    create_pool = Pool(
        processes=number_of_create_child_processes,
        initializer=make_global,
        initargs=(local_lock,)
    )

    # use a list comprehension to collect the result of each child processes
    # the apply_async method is used in such that multiple arguments can
    # be passed to the 'create_records_from_create_job' function, which is not
    # possible using the Pool.map method
    nested_list_of_created_records = [
        async_result_object.get() for async_result_object in [
            create_pool.apply_async(
                create_records_from_create_job, args=(
                    create_job, object_factory
                )
            ) for create_job in dequeued_create_jobs
        ]
    ]

    # use a list comprehension to flatten the list of lists created above
    created_records_from_multiple_jobs = [
        created_record
        for list_of_created_records in nested_list_of_created_records
        for created_record in list_of_created_records
    ]

    create_pool.close()
    create_pool.join()

    return created_records_from_multiple_jobs


def make_global(local_lock):
    """ helper function used in run_create_jobs that assigns the local_lock
    parameter to a global lock variable. This is required since a
    multiprocessing Lock object cannot otherwise be passed to a Pool method
    since it is not pickleable (required due to implementation of Pool in the
    multiprocessing module).

    For more information see this SO thread (with line break for PEP8):
    https://stackoverflow.com/
    questions/25557686/python-sharing-a-lock-between-processes
    """
    global lock
    lock = local_lock


def create_records_from_create_job(create_job, object_factory):
    """ Returns a list of records created as specified by a single 'create job'

    Parameters
    ----------
    create_job : dict
        dictionary specifying a quantity of records to create and the ID to
        start from (for domain objects with sequential unique IDs)
    object_factory : Creatable
        Instantiated and pre-configured object factory used to create
        records from create jobs

    Returns
    -------
    list
        List containing all the records created for this job
    """

    quantity, start_id = create_job['quantity'], create_job['start_id']

    # The InstrumentFactory is the only factory which has a critical section
    # and therefore requires a lock
    if object_factory.__class__.__name__ == "InstrumentFactory":
        created_records = object_factory.create(quantity, start_id, lock=lock)
    else:
        created_records = object_factory.create(quantity, start_id)

    return created_records


def run_write_jobs(write_jobs, number_of_write_child_processes, file_builder):
    """ Instantiates a Pool with a number of processes as given in the user
    config by the 'number_of_write_child_processes' line, and begins execution
    of the provided batch of 'write jobs' on the pool.

    Parameters
    ----------
    write_jobs : list
        List of write jobs to be run over the pool of child processes
    number_of_write_child_processes : int
        The number of processes sitting within the pool for execution of jobs
        to be ran on.
    file_builder : FileBuilder
        Instantiated subclass of FileBuilder used to write created records to
        file
    """

    write_pool = Pool(number_of_write_child_processes)

    # the apply_async method is used in a for loop such that multiple arguments
    # can be passed to the 'build_file_from_write_job' function, which is not
    # possible using the Pool.map method
    for write_job in write_jobs:
        write_pool.apply_async(
            build_file_from_write_job, args=(write_job, file_builder)
        )

    write_pool.close()
    write_pool.join()


def build_file_from_write_job(write_job, file_builder):
    """ Function to be called by each process in the pool in parallel, each
    taking a different write job as input.
    ----------
    write_job : dict
        Dictionary specifying the records to be written to file, and the file
        number used to uniquely name the output file
    file_builder : FileBuilder
        Instantiated subclass of FileBuilder used to write the output file
    """
    file_number, records = write_job['file_number'], write_job['records']
    file_builder.build(file_number, records)
