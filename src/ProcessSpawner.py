from multiprocessing import Process

def spawn_write(file_number, records, file_builder):
    Process(target=file_builder.build, args=(file_number, records)).start()