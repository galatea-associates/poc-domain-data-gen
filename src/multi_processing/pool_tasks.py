from multiprocessing import Pool


def generate(job_list, pool_size):
    pool = Pool(pool_size)
    result = pool.map(generate_data, job_list)
    pool.close()
    pool.join()
    return result


def generate_data(instruction):

    instructions = instruction[0]
    domain_object = instruction[1]

    domain_object_name = instructions['domain_object']
    amount = instructions['amount']
    start_id = instructions['start_id']

    records = domain_object.generate(amount, start_id)
    output = [domain_object_name, records]
    return output


def write(job_list, pool_size):
    pool = Pool(pool_size)
    pool.map(write_data, job_list)
    pool.close()
    pool.join()


def write_data(job):
    file_number = job['file_number']
    file_builder = job['file_builder']
    records = job['records']

    file_builder.build(file_number, records)
