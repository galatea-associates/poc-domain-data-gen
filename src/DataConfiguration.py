from CSVReader import CSVReader

# This file will contrain the core configuration for running the consumer and
# producer. It will also contain the functions needed to generate data for the
# different topics.

configuration = {
    # "prices": {
    #     "Counter": {
    #         "Initial Value": 0,
    #         "Limit Value": 40000
    #     },
    #     "Avro Schema - Keys": "prices-keys.avsc",
    #     "Avro Schema - Values": "prices-values.avsc",
    #     "Serializer": "Avro",
    #     "Data": CSVReader(),
    #     "Data Args": {
    #         'File': 'out/prices.csv',
    #         'Format': 'CSV',
    #         'Chunk Size': 50,
    #         'Loop on end': True
    #     },
    #     "Data Queue Max Size": 40,
    #     "Keys": ["inst_id"],
    #     "Load data first": True,
    #     "Number of Processes": 11,
    #     "Number of Data Generation Processes": 1,
    #     "Time Interval": 1.0
    # },
#     "positions": {
#         "Counter": {
#             "Initial Value": 0,
#             "Limit Value": 20000
#         },
#         "Avro Schema - Keys": "front-office-positions-keys.avsc",
#         "Avro Schema - Values": "front-office-positions-values.avsc",
#         "Serializer": "Avro",
#         "Data": CSVReader(),
#         "Data Args": {
#             'File': 'out/positions.csv',
#             'Format': 'CSV',
#             'Chunk Size': 50,
#             'Loop on end': True
#         },
#         "Data Queue Max Size": 20,
#         "Keys": ["type", "knowledge_date", "effective_date", "account",
#                  "instrument"],
#         "Load data first": True,
#         "Number of Processes": 4,
#         "Number of Data Generation Processes": 1,
#         "Time Interval": 1.0
#     },
    "instrument_reference_data": {
        "Counter": {
            "Initial Value": 0,
            "Limit Value": 100
        },
        "Avro Schema - Keys": "Kafka_Python/instrument-reference-data-keys.avsc",
        "Avro Schema - Values": "Kafka_Python/instrument-reference-data-values.avsc",
        "Serializer": "Avro",
        "Data": CSVReader(),
        "Data Args": {
            'File': 'Kafka_Python/out/inst-refs.csv',
            'Format': 'CSV',
            'Chunk Size': 10,
            'Loop on end': True
        },
        "Data Queue Max Size": 5,
        "Keys": ["inst_id"],
        "Load data first": True,
        "Number of Processes": 1,
        "Number of Data Generation Processes": 1,
        "Time Interval": 60.0
    },
}
