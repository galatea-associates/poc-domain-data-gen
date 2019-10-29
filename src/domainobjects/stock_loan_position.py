from domainobjects.generatable import Generatable
from functools import partial
from datetime import datetime
import random

class StockLoanPosition(Generatable):
    """ Class to generate stock loan positions. Generate method will generate
    a set amount of positions. Other generation method included where stock
    loan positions are the only domain object requiring them. """

    COLLATERAL_TYPES = ['Cash', 'Non Cash']
    STOCK_LOAN_POSITION_PURPOSES = ['Borrow', 'Loan']

    def generate(self, record_count, start_id):
        """ Generate a set number of stock loan positions

        Parameters
        ----------
        record_count : int
            Number of stock loan positions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' stock loan positions 

        """
        records = []
        self.instruments = self.retrieve_records('instruments')

        for i in range(start_id, start_id+record_count):
            records.append(self.generate_record(i))
        return records

    def generate_record(self, id):
        """ Generate a single stock loan position record

        Parameters
        ----------
        id : int
            ID of this generation

        Returns
        -------
        dict
            A single stock loan position object
        """

        instrument = self.get_random_instrument()
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
        collateral_type = self.generate_collateral_type()
        return {
                'stock_loan_contract_id': id,
                'ric': instrument['ric'],
                'knowledge_date': knowledge_date,
                'effective_date': self.generate_effective_date(0,
                                                               knowledge_date,
                                                               position_type),
                'purpose': self.generate_purpose(),
                'td_qty': self.generate_random_integer(),
                'sd_qty': self.generate_random_integer(),
                'collateral_type': collateral_type,
                'haircut': self.generate_haircut(collateral_type),
                'collateral_margin': self.generate_collateral_margin(
                                                      collateral_type),
                'rebate_rate': self.generate_rebate_rate(collateral_type),
                'borrow_fee': self.generate_borrow_fee(collateral_type),
                'termination_date': self.generate_termination_date(),
                'account': self.generate_account(),
                'is_callable': self.generate_random_boolean(),
                'return_type': self.generate_return_type(),
                'time_stamp': datetime.now()
            }


    def generate_haircut(self, collateral_type):
        """ Generate a haircut value based on collateral type 
            
        Parameters
        ----------
        collateral_type : String
            The type of collateral used for the loan

        Returns
        -------
        String
            Either a string of percentage, or the fact it's non cash
        """

        return '2.00%' if collateral_type == 'Non Cash' else None

    def generate_collateral_margin(self, collateral_type):
        """ Generate the collateral margin

        Parameters
        ----------
        collateral_type : String
            The type of collateral used for the loan

        Returns
        -------
        String
            Either a string of percentage, or the fact it's cash
        """

        return '140.00%' if collateral_type == 'Cash' else None

    def generate_collateral_type(self):
        """ Generate the type of collateral used

        Returns
        -------
        String
            'Cash' or 'Non Cash'
        """

        return random.choice(self.COLLATERAL_TYPES)

    def generate_termination_date(self):
        """ Generates a date for the termination of the loan

        Returns
        -------
        Date 
            where end date chosen to exist
        Nothing 
            where end date chosen to not exist
        """

        does_exist = random.choice([True, False])
        return None if not does_exist else self.generate_knowledge_date()

    def generate_rebate_rate(self, collateral_type):
        """ Generate the rebate rate of the loan

        Parameters
        ----------
        collateral_type : String
            The type of collateral used for the loan

        Returns
        -------
        String
            Percentage where the collateral type is cash
        """

        return '5.75%' if collateral_type == 'Cash' else None

    def generate_borrow_fee(self, collateral_type):
        """ Generates the borrow fee of the loan

        Parameters
        ----------
        collateral_type : String
            The type of collateral used for the loan

        Returns
        -------
        String
            Percentage where the collateral type is noncash
        """

        return '4.00%'if collateral_type == 'Non Cash' else None

    def generate_purpose(self):
        """ Generates the purpose of the loan

        Returns
        -------
        String
            Random choice between Borrow or Loan
        """

        return random.choice(self.STOCK_LOAN_POSITION_PURPOSES)