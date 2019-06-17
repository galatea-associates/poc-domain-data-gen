from domainobjects.generatable import Generatable
from functools import partial

class StockLoanPosition(Generatable):

    def get_template(self, data_generator):
        return {
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
        }