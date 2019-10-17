""" Pool Manager for both Generation and Writing tasks. Two methods are
responsible for each, a catch-all generate/write method which configures
the Pool for jobs to be executed on. Additionally included are methods the
pools use for each job in their respective job lists to perform the actual
generation/writing tasks.
"""

from multiprocessing import Pool


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

    pool = Pool(pool_size)
    result = pool.map(generate_data, job_list)
    pool.close()
    pool.join()
    return result


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
        List of 2 elements, the instruction to generate, and the instantiated
        domain object.

    Returns
    -------
    list
        Two element list. First, the objects name, for the purpose of
        segmenting records within the write coordinator. The second, a list
        of records, is the result of the generate call.
    """

    instructions = job[0]
    domain_object = job[1]

    domain_object_name = instructions['domain_object']
    amount = instructions['amount']
    start_id = instructions['start_id']

    records = domain_object.generate(amount, start_id)
    output = [domain_object_name, records]
    return output


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
