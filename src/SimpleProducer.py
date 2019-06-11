import atexit
import time

import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer

import csv
import io
import json
from Counter import Counter
from DataConfiguration import configuration
from Runnable import Runnable
from argparse import ArgumentParser
from multiprocessing import Manager, Process, Queue, Value

import math
import statistics


class Producer():
    def __init__(self, init_val=0, limit_val=0, ready_start_prod=False):
        self.sent_counter = Counter(init_val=init_val, limit_val=limit_val)
        self.received_counter = Counter(init_val=init_val, limit_val=limit_val)
        self.ready_start_producing = Value('i', ready_start_prod)
        self.error_counter = Counter(init_val=init_val, limit_val=math.inf)


def serialize_val(val, serializer, schema=None):
    if serializer == "Avro":
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(val, encoder)
        return_val = bytes_writer.getvalue()
    elif serializer == "JSON":
        return_val = json.dumps(val)
    else:
        return_val = val
    return return_val


def process_val(val, args=None):
    if callable(val):
        return process_val(val())
    elif isinstance(val, Runnable):
        return process_val(val.run(args))
    else:
        return_val = val
    return return_val


def send(server_args, producer_counters, topic, shared_data_queue,
         avro_schema_keys, avro_schema_values, serializer):
    server_addr = str(server_args.ip) + ":" + str(server_args.port)
    producer = KafkaProducer(bootstrap_servers=[server_addr])
    atexit.register(cleanup_producer, producer=producer)
    schema_keys = None
    schema_values = None

    if avro_schema_keys:
        schema_keys = avro.schema.Parse(open(avro_schema_keys).read())
    if avro_schema_values:
        schema_values = avro.schema.Parse(open(avro_schema_values).read())
        
    while not producer_counters.ready_start_producing:
        pass
    while True:
        while producer_counters.sent_counter.check_value_and_increment():
            val = shared_data_queue.get()
            if val is None:
                break
            producer.send(
                topic,
                value=serialize_val(val["value"], serializer, schema_values),
                key=serialize_val(val["key"], serializer, schema_keys)
            ).add_callback(
                on_send_success,
                producer_counters
            ).add_errback(on_send_error, producer_counters)


def on_send_success(producer_counters, _):
    producer_counters.received_counter.increment()


def on_send_error(producer_counters, _):
    producer_counters.error_counter.increment()


def reset_every_second(producer_counters, topic, time_interval, shared_dict, shared_data_queue, max_queue_size):
    while ((not producer_counters.ready_start_producing) and 
           (shared_data_queue.qsize() < max_queue_size)):
        pass
    producer_counters.ready_start_producing = True
    prev_time = time.time()
    while True:
        if time.time() - prev_time >= time_interval:
            result = {
                "Sent Counter": int(producer_counters.sent_counter.value()),
                "Received Counter": int(producer_counters.received_counter.value()),
                "Error Counter": int(producer_counters.error_counter.value())
            }
            producer_counters.received_counter.reset()
            producer_counters.sent_counter.reset()
            shared_dict[topic].append(result)
            prev_time = time.time()


def split_key_and_value(data, keys=None):
    keys_dict = {}
    values_dict = {}

    for key in keys:
        keys_dict[key] = data[key]

    value_keys = list(set(data.keys()).difference(keys))
    for value_key in value_keys:
        values_dict[value_key] = data[value_key]
        
    return {"key": keys_dict, "value":values_dict}


def data_pipe_producer(shared_data_queue, data_generator, max_queue_size, data_args, keys):
    while True:
        if shared_data_queue.qsize() < max_queue_size:
            data = process_val(data_generator, data_args)
            if data is None:
                # Means producer has finished sending
                shared_data_queue.put(data)
                break
            if isinstance(data, list):
                for item in data:
                    shared_data_queue.put(split_key_and_value(data=item,
                                                              keys=keys))
            else:
                shared_data_queue.put(split_key_and_value(data=data, keys=keys))


def start_sending(server_args, producer_counters, topic, data_generator, numb_prod_procs=1, numb_data_procs=1,
                  time_interval=1, avro_schema_keys=None, avro_schema_values=None, serializer=None, max_data_pipe_size=100,
                  data_args=None, keys=None):
    shared_dict[topic] = manager.list() 
    shared_data_queue = Queue()

    procs = [Process(target=send,
                     args=(server_args,
                           producer_counters,
                           topic,
                           shared_data_queue,
                           avro_schema_keys,
                           avro_schema_values,
                           serializer)) for i in range(numb_prod_procs)]

    timer_proc = Process(target=reset_every_second,
                         args=(producer_counters,
                               topic,
                               time_interval,
                               shared_dict,
                               shared_data_queue,
                               max_data_pipe_size))

    data_gen_procs = [Process(target=data_pipe_producer,
                              args=(shared_data_queue,
                                    data_generator,
                                    max_data_pipe_size,
                                    data_args,
                                    keys)) for i in range(numb_data_procs)]

    procs.append(timer_proc)
    procs += data_gen_procs
    for p in procs: 
        p.start()
    return procs


def cleanup_processes(procs):
    for p in procs:
        p.terminate()


def cleanup_producer(producer):
    producer.close()


def print_data_results(keys, dict_key):
    print(dict_key + ":")
    for key in keys:
        print(key + " -", end=' ')
        length = sum(1 for _ in (item[key] for item in shared_dict[dict_key]))
        print("Mean: " + str(sum(item[key] for item in shared_dict[dict_key]) / length), end=' ')
        print("Max: " + str(max(item[key] for item in shared_dict[dict_key])), end=' ')
        print("Min: " + str(min(item[key] for item in shared_dict[dict_key])), end=' ')
        if length > 1:
            print("Standard Deviation: " + str(statistics.stdev(item[key] for item in shared_dict[dict_key])))
    print()


def produce_output(dict_key, output_time):
    if not shared_dict[dict_key]:
        return
    keys = shared_dict[dict_key][0].keys()
    print_data_results(keys, dict_key)
    with open("out/output-send-" + str(int(output_time)) + ".csv",
              'a',
              newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(shared_dict[dict_key])


def cleanup(config=None, topics_procs=None):
    for procs in topics_procs:
        cleanup_processes(procs)
    output_time = time.time()
    for topic in config:
        produce_output(dict_key=topic, output_time=output_time)


def process_data_config(config, server_args):

    topics_procs = []
    producer_list = []

    for topic in config:
        producer_counters = Producer(init_val=config[topic]["Counter"]["Initial Value"],
                                     limit_val=config[topic]["Counter"]["Limit Value"],
                                     ready_start_prod=(not config[topic]['Load data first']))
        producer_list.append(producer_counters)

        procs = start_sending(server_args=server_args, 
                              producer_counters=producer_counters, 
                              topic=topic, 
                              data_generator=config[topic]["Data"], 
                              numb_prod_procs=config[topic]["Number of Processes"], 
                              numb_data_procs=config[topic]["Number of Data Generation Processes"], 
                              time_interval=config[topic]["Time Interval"], 
                              avro_schema_keys=config[topic]["Avro Schema - Keys"],
                              avro_schema_values=config[topic]["Avro Schema - Values"],
                              serializer=config[topic]["Serializer"],
                              max_data_pipe_size=config[topic]["Data Queue Max Size"],
                              data_args=config[topic]['Data Args'],
                              keys=config[topic]["Keys"])

        topics_procs.append(procs)

    return topics_procs, producer_list


def parse_args():
    parser = ArgumentParser()

    parser.add_argument("-i",
                        "--serverIP",
                        dest="ip",
                        help="Kafka server address",
                        required=True)

    parser.add_argument("-p",
                        "--serverPort",
                        dest="port",
                        help="Kafka server port",
                        default=9092)

    args = parser.parse_args()
    return args


def run():
    global manager, shared_dict

    server_args = parse_args()

    manager = Manager()
    shared_dict = manager.dict()    

    topics_procs, _ = process_data_config(configuration,
                                          server_args)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)
    input("Press Enter to exit...")


if __name__ == '__main__':
    run()
