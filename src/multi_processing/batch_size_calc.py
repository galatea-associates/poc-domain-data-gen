import math
from datetime import datetime

# Utility methods used to determine what batch size should be used for jobs
#
# Where domain objects are deterministic, i.e, the amount to generate is known
#   prior, trivially return the default generation_job_size_value
#
# Where domain objects are not, i.e, the amount to generate is based on
#   randomness and prior generated domain objects, calculate a batch size
#   to retrieve from the dependency database a number of rows which would
#   reasonably result in an amount of domain objects close to the default
#   generation_job_size_value


def get(obj_name, custom_args, default_job_size):
    nondeterministic_objects = ['SwapContract', 'SwapPosition', 'Cashflow']
    if obj_name not in nondeterministic_objects:
        return default_job_size
    elif obj_name == 'SwapContract':
        return swap_contract_size(custom_args, default_job_size)
    elif obj_name == 'SwapPosition':
        return swap_position_size(custom_args, default_job_size)
    elif obj_name == 'Cashflow':
        return cashflow_size(custom_args, default_job_size)
    else:
        print("Object not found")


# Calculate the average number of counterparties to retrieve from DB in
# order to generate the default_job_size worth of Swap Contract records
# based on given configuration
def swap_contract_size(custom_args, target_num_records):
    swaps_per_counterparty = custom_args['swap_per_counterparty']
    min_swaps = int(swaps_per_counterparty['min'])
    max_swaps = int(swaps_per_counterparty['max'])
    batch_size = math.ceil((2*target_num_records)/(min_swaps + max_swaps))
    return batch_size


# Calculate the average number of Swap Contracts to retrieve from DB in
# order to generate the default_job_size worth of Swap Position records
# based on given configuration
def swap_position_size(custom_args, target_num_records):
    start_date = custom_args['start_date']
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.today()
    num_dates = ((end_date-start_date).days)+1
    ins_per_swap = custom_args['ins_per_swap']
    ins_min = int(ins_per_swap['min'])
    ins_max = int(ins_per_swap['max'])

    batch_size = math.ceil((2*target_num_records) / 
                           (3*num_dates*(ins_min+ins_max)))
    return batch_size


# Calculate the average number of Swap Positions to retrieve from DB in
# order to generate the default_job_size worth of Cashflow records based
# on given configuration
def cashflow_size(custom_args, target_num_records):
    cashflow_args = custom_args['cashflow_generation']
    sum_probability = 0

    for cashflow in cashflow_args:
        accrual_chance = cashflow['cashFlowAccrualProbability']
        sum_probability += (accrual_chance/100)

    batch_size = math.ceil(target_num_records/sum_probability)
    return batch_size
