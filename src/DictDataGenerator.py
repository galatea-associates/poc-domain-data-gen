import argparse
import csv
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from functools import partial
from Runnable import Runnable
from DataGenerator import DataGenerator

data_generator = DataGenerator()
data_template = {
    'inst_ref': {
        'ric*': {'func': data_generator.generate_new_ric, 'args': ['asset_class']},
        'isin': {'func': data_generator.generate_isin,
                 'args': ['coi', 'cusip', 'asset_class']},
        'sedol': {'func': data_generator.generate_sedol,
                  'args': ['ticker', 'asset_class']},
        'ticker': {'func': partial(data_generator.generate_ticker, new_ric_generator=True),
                   'args': ['asset_class', 'ric']},
        'cusip': {'func': data_generator.generate_cusip,
                  'args': ['ticker', 'asset_class']},
        'asset_class': {'func': partial(data_generator.generate_asset_class,
                                        generating_inst=True)},
        'coi': {'func': data_generator.generate_coi, 'args': ['asset_class']},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'price': {
        'ric*': {'func': partial(data_generator.generate_ric, no_cash=True),
                 'args': ['ticker', 'ric']},
        'price': {'func': data_generator.generate_price, 'args': ['ticker']},
        'curr': {'func': partial(data_generator.generate_currency, for_ticker=True)},
        'update_time_stamp*': {'func': data_generator.generate_update_time_stamp}
    },
    'front_office_position': {
        'ric*': {'func': partial(data_generator.generate_ric, no_cash=True),
                 'args': ['ticker', 'asset_class']},
        'position_type*': {'func': data_generator.generate_position_type},
        'knowledge_date*': {'func': data_generator.generate_knowledge_date},
        'effective_date*': {
            'func': partial(data_generator.generate_effective_date, n_days_to_add=0),
            'args': ['knowledge_date', 'position_type']},
        'account*': {'func': partial(data_generator.generate_account, no_ecp=True)},
        'direction': {'func': data_generator.generate_direction},
        'qty': {'func': data_generator.generate_qty},
        'purpose*': {'func': partial(data_generator.generate_purpose, data_type='FOP')},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'back_office_position': {
        'cusip*': {'func': partial(data_generator.generate_cusip, no_cash=True),
                  'args': ['ticker', 'asset_class']},
        'position_type*': {'func': data_generator.generate_position_type},
        'knowledge_date*': {'func': data_generator.generate_knowledge_date},
        'effective_date*': {'func': partial(data_generator.generate_effective_date,
                                            n_days_to_add=3),
                            'args': ['knowledge_date', 'position_type']},
        'account*': {'func': data_generator.generate_account},
        'direction': {'func': data_generator.generate_direction},
        'qty': {'func': data_generator.generate_qty},
        'purpose*': {'func': partial(data_generator.generate_purpose, data_type='BOP')},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'depot_position': {
        'isin*': {'func': partial(data_generator.generate_isin, no_cash=True),
                 'args': ['coi', 'cusip', 'asset_class']},
        'position_type': {'func': partial(data_generator.generate_position_type,
                                          no_td=True)},
        'knowledge_date*': {'func': data_generator.generate_knowledge_date},
        'effective_date*': {'func': data_generator.generate_effective_date,
                            'args': ['knowledge_date', 'position_type']},
        'account*': {'func': partial(data_generator.generate_account, no_ecp=True)},
        'direction': {'func': data_generator.generate_direction},
        'qty': {'func': data_generator.generate_qty},
        'purpose*': {'func': partial(data_generator.generate_purpose, data_type='DP')},
        'depot_id*': {'func': data_generator.generate_depot_id},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'order_execution': {
        'order_id*': {'func': data_generator.generate_order_id, 'args': ['asset_class']},
        'account_num': {'func': data_generator.generate_account_number},
        'direction': {'func': data_generator.generate_direction},
        'sto_id': {'func': data_generator.generate_sto_id, 'args': ['asset_class']},
        'agent_id': {'func': data_generator.generate_agent_id, 'args': ['asset_class']},
        'price': {'func': data_generator.generate_price, 'args': ['inst_id']},
        'curr': {'func': data_generator.generate_currency},
        'ric': {'func': partial(data_generator.generate_ric, no_cash=True),
                'args': ['ticker', 'asset_class']},
        'qty': {'func': data_generator.generate_qty},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'stock_loan_position': {
        'stock_loan_contract_id*': {
            'func': data_generator.generate_new_stock_loan_contract_id
        },
        'ric*': {'func': partial(data_generator.generate_ric, no_cash=True),
                 'args': ['ticker', 'asset_class']},
        'knowledge_date*': {'func': data_generator.generate_knowledge_date},
        'effective_date*': {'func': data_generator.generate_effective_date,
                            'args': ['knowledge_date', 'position_type']},
        'purpose*': {'func': partial(data_generator.generate_purpose, data_type='SL')},
        'td_qty': {'func': data_generator.generate_qty},
        'sd_qty': {'func': data_generator.generate_qty},
        'collateral_type*': {'func': data_generator.generate_collateral_type},
        'haircut': {'func': data_generator.generate_haircut, 'args': ['collateral_type']},
        'collateral_margin': {'func': data_generator.generate_collateral_margin,
                              'args': ['collateral_type']},
        'rebate_rate': {'func': data_generator.generate_rebate_rate,
                        'args': ['collateral_type']},
        'borrow_fee': {'func': data_generator.generate_borrow_fee,
                       'args': ['collateral_type']},
        'termination_date': {'func': data_generator.generate_termination_date},
        'account*': {'func': data_generator.generate_account},
        'is_callable': {'func': data_generator.generate_is_callable},
        'return_type': {'func': data_generator.generate_return_type},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'swap_contract': {
        'swap_contract_id*': {'func': data_generator.generate_new_swap_contract_id},
        'status': {'func': data_generator.generate_status},
        'start_date': {'func': data_generator.generate_swap_start_date},
        'end_date': {'func': data_generator.generate_swap_end_date,
                     'args': ['status', 'start_date']},
        'swap_type': {'func': data_generator.generate_swap_type},
        'reference_rate': {'func': data_generator.generate_reference_rate},
        'field1': {'func': data_generator.generate_rdn},
        'field2': {'func': data_generator.generate_rdn},
        'field3': {'func': data_generator.generate_rdn},
        'field4': {'func': data_generator.generate_rdn},
        'field5': {'func': data_generator.generate_rdn},
        'field6': {'func': data_generator.generate_rdn},
        'field7': {'func': data_generator.generate_rdn},
        'field8': {'func': data_generator.generate_rdn},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'swap_position': {
        'ric*': {'func': partial(data_generator.generate_ric, no_cash=True),
                 'args': ['ticker', 'asset_class']},
        'swap_contract_id*': {'func': data_generator.generate_swap_contract_id},
        'position_type*': {'func': data_generator.generate_position_type},
        'knowledge_date*': {'func': data_generator.generate_knowledge_date},
        'effective_date*': {'func': partial(data_generator.generate_effective_date,
                                            n_days_to_add=3),
                            'args': ['knowledge_date', 'position_type']},
        'account*': {'func': data_generator.generate_account},
        'direction': {'func': data_generator.generate_direction},
        'qty': {'func': data_generator.generate_qty},
        'purpose*': {'func': partial(data_generator.generate_purpose, data_type='ST')},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    },
    'cash': {
        'amount': {'func': data_generator.generate_qty},
        'curr': {'func': data_generator.generate_currency},
        'account_num': {'func': data_generator.generate_account_number},
        'purpose': {'func': partial(data_generator.generate_purpose, data_type='C')},
        'time_stamp': {'func': data_generator.generate_time_stamp},
    }
}


class DictRunnable(Runnable):

    # In DataConfiguration.py, 'Data Args' field should look like:
    # {'Type': 'position'}
    def run(self, args):
        pass

    @staticmethod
    def main():
        args = get_args()
        dict_data_generator = DictRunnable()
        dict_data_generator .__generate_data_files(args)

    def __authenticate_gdrive(self, creds):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(creds)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(creds)
        return gauth

    def __generate_data_files(self, args):
        os.chdir('data_gen')
        # Create out directory if it does not yet exist
        if not os.path.exists('out'):
            os.makedirs('out')

        gauth = self.__authenticate_gdrive(args.creds)
        drive = GoogleDrive(gauth)

        if args.inst_refs > 0:
            self.__create_data_file('out/inst_refs.csv',
                                    args.inst_refs,
                                    'inst_ref')
            self.__upload_to_gdrive(args.folder_id, drive, 'inst_refs.csv')
        if args.prices > 0:
            self.__create_data_file('out/prices.csv', args.prices, 'price')
            self.__upload_to_gdrive(args.folder_id, drive, 'prices.csv')
        if args.front_office_positions > 0:
            self.__create_data_file('out/front_office_positions.csv',
                                    args.front_office_positions,
                                    'front_office_position')
            self.__upload_to_gdrive(args.folder_id,
                                    drive,
                                    'front_office_positions.csv')
        if args.back_office_positions > 0:
            self.__create_data_file('out/back_office_positions.csv',
                                    args.back_office_positions,
                                    'back_office_position')
            self.__upload_to_gdrive(args.folder_id,
                                    drive,
                                    'back_office_positions.csv')
        if args.depot_positions > 0:
            self.__create_data_file('out/depot_positions.csv',
                                    args.depot_positions,
                                    'depot_position')
            self.__upload_to_gdrive(args.folder_id,
                                    drive,
                                    'depot_positions.csv')
        if args.order_executions > 0:
            self.__create_data_file('out/order_executions.csv',
                                    args.order_executions,
                                    'order_execution')
            self.__upload_to_gdrive(args.folder_id,
                                    drive,
                                    'order_executions.csv')
        if args.stock_loan_positions > 0:
            self.__create_data_file('out/stock_loan_positions.csv',
                                    args.stock_loan_positions,
                                    'stock_loan_position')
            self.__upload_to_gdrive(args.folder_id,
                                    drive,
                                    'stock_loan_positions.csv')
        if args.swap_contracts > 0:
            self.__create_data_file('out/swap_contracts.csv',
                                    args.swap_contracts,
                                    'swap_contract')
            self.__upload_to_gdrive(args.folder_id, drive, 'swap_contracts.csv')
        if args.swap_positions > 0:
            self.__create_data_file('out/swap_positions.csv',
                                    args.swap_positions,
                                    'swap_position')
            self.__upload_to_gdrive(args.folder_id, drive, 'swap_positions.csv')
        if args.cash > 0:
            self.__create_data_file('out/cash.csv', args.cash, 'cash')
            self.__upload_to_gdrive(args.folder_id, drive, 'cash.csv')

    def __upload_to_gdrive(self, folder_id, drive, file_name):
        self.__delete_existing_file(folder_id, drive, file_name)
        self.__add_file(folder_id, drive, file_name)

    def __add_file(self, folder_id, drive, file_name):
        file = drive.CreateFile({
            "parents": [{"kind": "drive#fileLink", "id": folder_id}]
        })
        file.SetContentFile('out/' + file_name)
        file['title'] = file_name
        file['mimeType'] = 'text/x-csv'
        file.Upload()

    def __delete_existing_file(self, folder_id, drive, file_name):
        file_list = self.__get_all_files_in_folder(folder_id, drive)
        for f in file_list:
            if f['title'] == file_name:
                f.Delete()

    def __get_all_files_in_folder(self, folder_id, drive):
        return drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()

    # file_name corresponds to the name of the CSV file the function will write
    # to n is the number of data entities to write to the CSV file
    # data_generator is the function reference that generates the data entity
    # of interest
    def __create_data_file(self, file_name, n, data_type):
        # w+ means create file first if it does not already exist
        date = datetime.datetime.utcnow() - datetime.timedelta(days=4)
        data_generator.set_date(date)
        with open(file_name, mode='w+', newline='') as file:
            self.__write_data_type_at_top(file, data_type)

            data = self.__generate_data(data_template[data_type])
            writer = self.__create_csv_with_headers(file, list(data))
            writer.writerow(data)
            # n - 1 because we already wrote to the file once with the entity
            # variable - we do this to get the keys of the dictionary in order
            # to get the field names of the CSV file
            new_date_at = int(n/4)
            counter = 1
            for i in range(1, n):
                if i == counter * new_date_at:
                    date += datetime.timedelta(days=1)
                    data_generator.set_date(date)
                    counter += 1
                entity = self.__generate_data(data_template[data_type])

                writer.writerow(entity)
        data_generator.reset_update_timestamp()

    def __write_data_type_at_top(self, file, data_type):
        file.write(' '.join(map(str.capitalize, data_type.split('_'))) + '\n')

    def __create_csv_with_headers(self, file, headers):
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        return writer

    def __is_key(self, field):
        return '*' in field

    def __generate_data(self, template):
        data = {}
        for field, generator_function in template.items():
            if not self.__field_already_generated(field, data):
                if self.__is_key(field, data):
                    suffix = '*'
                    field = self.__remove_asterix_from_field_name(field)
                else:
                    suffix = ''

                if data_generator.state_contains_field(field):
                    data[field + suffix] = data_generator.get_state_value(field)
                elif 'args' in generator_function:
                    args_needed = generator_function['args']
                    args_generated = self.__generate_args_for_generator_function(args_needed, data)
                    data[field + suffix] = generator_function['func'](**args_generated)
                else:
                    data[field + suffix] = generator_function['func']()
        data_generator.clear_state()
        return data

    def __remove_aterix_field_name(self, field):
        return field.replace('*', '')


    def __is_key(self, field, data):
        return field + '*' in data

    def __field_already_generated(self, field, data):
        return field in data

    def __generate_args_for_generator_function(self, args_needed, data):
        args_generated = {}
        for field in args_needed:
            if self.__field_already_generated(field, data):
                args_generated[field] = data[field]
            elif self.__is_key(field, data):
                args_generated[field] = data[field + '*']
            elif data_generator.state_contains_field(field):
                args_generated[field] = data_generator.get_state_value(field)
        return args_generated


def get_args():
    parser = argparse.ArgumentParser()
    optional_args = {'nargs': '?', 'type': int, 'default': 0}
    parser.add_argument('--prices', **optional_args)
    parser.add_argument('--front-office-positions', **optional_args)
    parser.add_argument('--back-office-positions', **optional_args)
    parser.add_argument('--inst-refs', **optional_args)
    parser.add_argument('--depot-positions', **optional_args)
    parser.add_argument('--order-executions', **optional_args)
    parser.add_argument('--stock-loan-positions', **optional_args)
    parser.add_argument('--swap-contracts', **optional_args)
    parser.add_argument('--swap-positions', **optional_args)
    parser.add_argument('--cash', **optional_args)
    parser.add_argument('--creds', required=True)
    parser.add_argument('--folder-id', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    DictRunnable.main()
