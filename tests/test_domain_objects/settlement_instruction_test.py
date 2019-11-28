import sys

sys.path.insert(0, 'tests/')
from utils import helper_methods as helper

def test_settlement_instructions():
    records = helper.set_up_settlement_instruction_tests()