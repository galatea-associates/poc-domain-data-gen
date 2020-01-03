from file_builders.file_builder import FileBuilder
from os.path import join
from csv import DictWriter


class CSVBuilder(FileBuilder):

    @classmethod
    def build(
            cls,
            output_directory,
            output_file_name,
            generator_config,
            quantity,
            lock,
            start_id
    ):

        output_file_path = join(output_directory, output_file_name + ".csv")
        generator = cls.get_generator(
            generator_config, quantity, lock, start_id
        )

        first_row = next(generator)
        fieldnames = first_row.keys()

        with open(output_file_path, "w+", newline="") as output_file:
            dict_writer = DictWriter(
                output_file, restval="-", fieldnames=fieldnames, delimiter=","
            )

            dict_writer.writeheader()
            dict_writer.writerow(first_row)
            dict_writer.writerows(generator)
