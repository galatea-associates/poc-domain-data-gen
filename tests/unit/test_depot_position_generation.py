import pytest
from src.domainobjects import depot_position as generator

class Test_Depot_Position_Generation(object):

    def test_generate_purpose(self):
        purpose = generator.DepotPosition.generate_purpose(self)
        assert purpose in ['Holdings', 'Seg']