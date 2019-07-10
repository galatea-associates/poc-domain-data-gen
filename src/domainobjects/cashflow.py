from domainobjects.generatable import Generatable
from functools import partial
import random
import pandas as pd
import datetime
import calendar

class Cashflow(Generatable):

    def generate(self, data_generator, record_count, custom_args):
        cashflow_gen_args = custom_args['cashflow_generation']   
        start_date = datetime.datetime.strptime(custom_args['start_date'], '%Y%m%d') 
        end_date = datetime.datetime.today()
        swap_contract_instruments = data_generator.retrieve_from_global_state('swap_contract_instrument')
        records = []
        i = 1

        for cashflow_gen_arg in cashflow_gen_args:
            cashflow_type = cashflow_gen_arg['cashFlowType']
            accrual = cashflow_gen_arg['cashFlowAccrual']
            pay_date_period = cashflow_gen_arg['cashFlowPaydatePeriod']
            probability = cashflow_gen_arg['cashFlowAccrualProbability']
            pay_date_func = self.get_pay_date_func(pay_date_period)
            date_range = self.get_date_range(accrual, start_date, end_date)            

            for swap_contract_instrument in swap_contract_instruments:
                data_generator.persist_to_current_record_state('swap_contract_id', swap_contract_instrument[0])
                data_generator.persist_to_current_record_state('instrument_id', swap_contract_instrument[1])                
                data_generator.persist_to_current_record_state('cashflow_type', cashflow_type)
                
                for date in date_range:  
                    if random.random() < (int(probability) / 100):
                        data_generator.persist_to_current_record_state('effective_date', date.date())
                        data_generator.persist_to_current_record_state('pay_date', pay_date_func(date))
                        records.append(self.generate_record(data_generator, i))     
                        i += 1 

                data_generator.clear_current_record_state()
        
        return records

    def calc_eom(self, d):
       return datetime.date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])

    def calc_eoh(self, d):
       return datetime.date(d.year, 6, 30) if d.month <= 6 else datetime.date(d.year, 12, 31)

    def get_pay_date_func(self, pay_date_period):
        return {
            "END_OF_MONTH":self.calc_eom,
            "END_OF_HALF":self.calc_eoh
        }.get(pay_date_period, lambda:"Invalid pay date period")  

    def get_date_range(self, accrual, sd, ed):
        return {
            "DAILY":pd.date_range(sd, ed, freq='D'),
            "QUARTERLY":pd.date_range(sd, ed, freq='Q'),
            "CHANCE_ACCRUAL":pd.date_range(sd, ed, freq='D')
        }.get(accrual, lambda:"Invalid accrual frequency")

    def get_template(self, data_generator):
        return {
            'cashflow_id': {'func': data_generator.generate_rdn, 'field_type': 'id'},
            'swap_contract_id': {'func': partial(data_generator.retrieve_from_current_record_state, 'swap_contract_id')},
            'instrument_id': {'func': partial(data_generator.retrieve_from_current_record_state, 'instrument_id')},
            'cashflow_type': {'func': partial(data_generator.retrieve_from_current_record_state, 'cashflow_type')},
            'pay_date': {'func': partial(data_generator.retrieve_from_current_record_state, 'pay_date')},
            'effective_date': {'func': partial(data_generator.retrieve_from_current_record_state, 'effective_date')},
            'currency': {'func': data_generator.generate_currency},
            'amount': {'func': data_generator.generate_qty},
            'long_short': {'func': data_generator.generate_long_short},  
        }
  
