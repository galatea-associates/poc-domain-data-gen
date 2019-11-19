from domainobjects.generatable import Generatable
import random
import pandas as pd
from datetime import datetime, date
import calendar


class Cashflow(Generatable):
    """ Class to generate cashflows. Generate method will generate a set
    amount of cashflows. Other generation methods are included where cashflows
    are the only domain object requiring them.

    Process of generating cashflows dependent on Swap Positions, for each of
    these positions, simulate whether each cashflow type (defined by the user
    in custom arguments -> cashflow args) would accrue, and if so, generate a
    record of such. Only Swap Positions with type 'E' (end of day) will have
    cashflows generated.
    """

    def generate(self, record_count, start_id):
        """ Generate a set number of cashflows

        Parameters
        ----------
        record_count : int
            Number of cashflows to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' cashflows
        """

        swap_position_batch =\
            self.retrieve_batch_records('swap_positions',
                                        record_count, start_id)
        cashflow_gen_args = self.get_cashflow_gen_args()

        records = [self.generate_record(swap_position, cf_arg)
                   for swap_position in swap_position_batch
                   for cf_arg in cashflow_gen_args
                   if swap_position['position_type'] == 'E']
        records = filter(None, records)
        return records

    def generate_record(self, swap_position, cf_arg):
        """ Generate a single cashflow

        Parameters
        ----------
        Swap Position : dict
            Dictionary containing a partial record of a Swap Position, only
            contains the information necessary to generate Cashflows
        cf_arg : dict
            Dictionary defining the particular cashflow being generated for

        Returns
        -------
        dict
            A single cashflow object
        """

        accrual = cf_arg['cashFlowAccrual']
        probability = cf_arg['cashFlowAccrualProbability']
        effective_date = self.effective_date(swap_position['effective_date'])
        if self.cashflow_accrues(effective_date, accrual, probability):
            pay_date_period = cf_arg['cashFlowPaydatePeriod']
            p_date_func = self.get_pay_date_func(pay_date_period)
            record = {
                'swap_contract_id': swap_position['swap_contract_id'],
                'ric': swap_position['ric'],
                'cashflow_type': cf_arg['cashFlowType'],
                'pay_date': datetime.strftime(p_date_func(effective_date),
                                              '%Y-%m-%d'),
                'effective_date': effective_date,
                'currency': self.generate_currency(),
                'amount': self.generate_random_integer(),
                'long_short': swap_position['long_short']
            }

            for key, value in self.get_dummy_field_generator():
                record[key] = value

            return record

    def effective_date(self, effective_date):
        """ Parse string time into Datetime type

        Parameters
        ----------
        effective_date : String
            String to parse into datetime. Expected format '%Y-%m-%d'

        Returns
        -------
        Datetime
            Parsed Datetime of given date string
        """

        return datetime.strptime(effective_date, '%Y-%m-%d')

    def get_cashflow_gen_args(self):
        """ Retrieve the user-defined cashflow generation arguments from
        config. These are the definitions of cashflow type and the attributes
        thereof.

        Returns
        -------
        dict
            All cashflow types and their respective definitions
        """

        custom_args = self.get_custom_args()
        return custom_args['cashflow_generation']

    def calc_eom(self, d):
        """ Calculate the end of month from a given Date

        Parameters
        ----------
        d : Date
            Date from which the end of month is to be calculated

        Returns
        -------
        Date
            End of month the provided date is within
        """

        return date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])

    def calc_eoh(self, d):
        """ Calculate the end of half from a given Date

        Parameters
        ----------
        d : Date
            Date from which the end of half is to be calculated

        Returns
        -------
        Date
            End of half the provided date is within
        """

        return date(d.year, 6, 30) if d.month <= 6 else date(d.year, 12, 31)

    def get_pay_date_func(self, pay_date_period):
        """ Retrieve the pay date function for a given pay date period from
        the user-defined cashflow arguments. This value is either end of month
        or half, and returns the end of month/half date in each case
        respectively.

        Parameters
        ----------
        pay_date_period : String
            User-defined period of payment, either end of month or half.

        Returns
        -------
        Date
            The end of month/half depending on which period is observed.
        """

        return {
            "END_OF_MONTH": self.calc_eom,
            "END_OF_HALF": self.calc_eoh
        }.get(pay_date_period, lambda: "Invalid pay date period")

    def cashflow_accrues(self, effective_date, accrual, probability):
        """ Returns True where a particular cashflow with accrual
        rate/probability has been simulated as accruing.

        Parameters
        ----------
        effective_date : Date
            Date the cashflow is effective from
        accrual : String
            Rate at which the cashflow accrues, daily, quarterly, or chance
        probability : int
            Value 1 - 100 of percentage change this cashflow accrues

        Returns
        -------
        Boolean
            True where the cashflow is simulated to/naturally does accrue
        """

        if accrual == "DAILY":
            return True
        elif accrual == "QUARTERLY" and \
                (effective_date.day, effective_date.month) in \
                [(31, 3), (30, 6), (30, 9), (31, 12)]:
            return True
        elif accrual == "CHANCE_ACCRUAL" and \
                random.random() < (int(probability) / 100):
            return True
