import os, shutil, json, timeit
from datetime import datetime, timedelta

gen_pool_sizes = [1, 2, 3, 4, 5, 6]
write_pool_sizes = [1, 2, 3, 4, 5, 6]
job_sizes = [25000, 50000, 75000, 100000,
             125000, 150000, 175000, 200000,
             225000, 250000]

def main():
    with open("results.txt", "a+") as file:
        file.write("gen_pools, write_pools, job_size, time\n")

    for gen_pools in gen_pool_sizes:
        for write_pools in write_pool_sizes:
            for job_size in job_sizes:
                
                clear_out_directory()
                config = get_config()
                update_configuration(config, gen_pools, write_pools, job_size)
                
                start = timeit.default_timer()
                os.system("python src/new_app.py")
                time = timeit.default_timer()-start
                
                update_out_file(gen_pools, write_pools, job_size, time)
    

def update_out_file(gen_pools, write_pools, job_size, time):
    with open("results.txt", "a+") as file:
        file.write(str(gen_pools)+","+str(write_pools)+","+str(job_size)+","+str(time)+"\n")


def clear_out_directory():
    out_directory = "out/"
    for file in os.listdir(out_directory):
        file_path = os.path.join(out_directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def get_config():
    with open("src/config.json") as config_file:
        return json.load(config_file)

def get_week_prior():
    today = datetime.today()
    date = today - timedelta(days = 6)
    return datetime.strftime(date, "%Y%m%d")

def update_configuration(config, gen_pools, write_pools, job_size):
    config['domain_objects'][10]['custom_args']['start_date'] = get_week_prior()
    config['shared_args']['gen_pools'] = gen_pools
    config['shared_args']['write_pools'] = write_pools
    config['shared_args']['job_size'] = job_size
    write_updated_config(config)

def write_updated_config(config):
    with open("src/config.json", 'w') as out_file:
        json.dump(config, out_file, indent=2)

if __name__ == '__main__':
    main()
