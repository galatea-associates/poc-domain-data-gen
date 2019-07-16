import pytest
from src.domainobjects import back_office_position as generator

class Test_Back_Office_Position_Generation(object):

    def test_generate_purpose(self):
        purpose = generator.BackOfficePosition.generate_purpose(self)
        assert purpose == 'Outright'