import pytest
from src.domainobjects import front_office_position as generator

class Test_Front_Office_Position_Generation(object):

    def test_generate_purpose(self):
        purpose = generator.FrontOfficePosition.generate_purpose(self)
        assert purpose == 'Outright'