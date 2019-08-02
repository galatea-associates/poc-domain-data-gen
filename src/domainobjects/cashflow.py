from domainobjects.generatable import Generatable
import random
import pandas as pd
from datetime import datetime, date
import calendar

class Cashflow(Generatable):
    
    def generate(self, record_count, custom_args):
        cashflow_gen_args = custom_args['cashflow_generation']          
        records = []
        i = 1
        swap_positions = self.dependency_db.retrieve_from_database('swap_positions')

        for swap_position in swap_positions:
            if swap_position['position_type'] != 'E':
                continue

            # Intermediary variable required as sqlite3.Row does not support assignment
            effective_date_ = swap_position['effective_date']
            effective_date = datetime.strptime(effective_date_, '%Y%m%d')

            for cashflow_gen_arg in cashflow_gen_args:
                if self.generate_cashflow(effective_date, cashflow_gen_arg['cashFlowAccrual'], cashflow_gen_arg['cashFlowAccrualProbability']):
                    
                    pay_date_period = cashflow_gen_arg['cashFlowPaydatePeriod']                    
                    pay_date_func = self.get_pay_date_func(pay_date_period) 
                    records.append({
                        'cashflow_id': i,
                        'swap_contract_id': swap_position['swap_contract_id'],
                        'ric': swap_position['ric'],
                        'cashflow_type': cashflow_gen_arg['cashFlowType'],
                        'pay_date': pay_date_func(effective_date),
                        'effective_date': effective_date,
                        'currency': self.generate_currency(),
                        'amount': self.generate_random_integer(),
                        'long_short': swap_position['long_short'] 
                    })

                    i+=1 
        
        return records
    
    def calc_eom(self, d):
        return date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])
    
    def calc_eoh(self, d):
        return date(d.year, 6, 30) if d.month <= 6 else datetime.date(d.year, 12, 31)
    
    def get_pay_date_func(self, pay_date_period):
        return {
            "END_OF_MONTH":self.calc_eom,
            "END_OF_HALF":self.calc_eoh
        }.get(pay_date_period, lambda:"Invalid pay date period")  
    
    def generate_cashflow(self, effective_date, accrual, probability):
        if accrual == "DAILY":
            return True
        elif accrual == "QUARTERLY" and (effective_date.day, effective_date.month) in [(31, 3), (30, 6), (30, 9), (31, 12)]:
            return True
        elif accrual == "CHANCE_ACCRUAL" and random.random() < (int(probability) / 100):
            return True
        


    
