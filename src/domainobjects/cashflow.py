from domainobjects.generatable import Generatable
import random
import pandas as pd
from datetime import datetime, date
import calendar

class Cashflow(Generatable):

    def generate(self, record_count, start_id):

        record = self.instantiate_record()
        record_store = []
        swap_position_batch =\
         self.retrieve_batch_records('swap_positions', record_count, start_id)
        cashflow_gen_args = self.get_cashflow_gen_args()

        for swap_position in swap_position_batch:
            if swap_position['position_type'] != 'E': continue

            effective_date_ = swap_position['effective_date']
            effective_date = datetime.strptime(effective_date_, '%Y-%m-%d')
            record['effective_date'] = effective_date
            record['swap_contract_id'] = swap_position['swap_contract_id']
            for cf_arg in cashflow_gen_args:
                record['ric'] = swap_position['ric']
                record['long_short'] = swap_position['long_short']

                accrual = cf_arg['cashFlowAccrual']
                probability = cf_arg['cashFlowAccrualProbability']
                if self.cashflow_accrues(effective_date,
                                          accrual,
                                          probability):

                    record = self.generate_remaining_record(cf_arg, 
                                                  effective_date, record)
                    record_store.append(record.copy())

        return record_store

    def get_cashflow_gen_args(self):
        custom_args = self.get_custom_args()
        return custom_args['cashflow_generation']

    def generate_remaining_record(self, cf_arg, effective_date, record):

        pay_date_period = cf_arg['cashFlowPaydatePeriod']
        p_date_func = self.get_pay_date_func(pay_date_period)

        record['cashflow_type'] = cf_arg['cashFlowType']
        record['pay_date'] = datetime.strftime(p_date_func(effective_date),
                                              '%Y-%m-%d')
        record['currency'] = self.generate_currency()
        record['amount'] = self.generate_random_integer()

        return record

    def calc_eom(self, d):
        return date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])

    def calc_eoh(self, d):
        return date(d.year, 6, 30) if d.month <= 6 else date(d.year, 12, 31)

    def get_pay_date_func(self, pay_date_period):
        return {
            "END_OF_MONTH":self.calc_eom,
            "END_OF_HALF":self.calc_eoh
        }.get(pay_date_period, lambda: "Invalid pay date period")

    def cashflow_accrues(self, effective_date, accrual, probability):
        if accrual == "DAILY":
            return True
        elif accrual == "QUARTERLY" and \
                (effective_date.day, effective_date.month) in \
                [(31, 3), (30, 6), (30, 9), (31, 12)]:
            return True
        elif accrual == "CHANCE_ACCRUAL" and \
                random.random() < (int(probability) / 100):
            return True
    
    def instantiate_record(self):
        return {
            'swap_contract_id': None,
            'ric': None,
            'cashflow_type': None,
            'pay_date': None,
            'effective_date': None,
            'currency': None,
            'amount': None,
            'long_short': None
        }
