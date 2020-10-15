from pytest import fixture

from intcode.io.make_processors import list2processor, file2processor
from intcode.logic import process
from intcode.logic.processor_communication import set_input_and_output_classes, StackOutputClass
from intcode.main import run_processor_with_single_input


@fixture
def quine():
    return [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

def test_quine_program(quine):
    '''
    A quine is a program that outputs itself.
    '''
    processor = list2processor(quine)
    output_class = StackOutputClass()
    set_input_and_output_classes(processor, None, output_class)
    process.run_process(processor)
    assert output_class.value == quine

def test_run_test_program():
    processor = file2processor("data/day9_input.txt")
    # 2890527621 is the "boost keycode" we found for the day9 assignment.
    # It is the only output of the program if the self-test is successful.
    assert run_processor_with_single_input(processor, 1)[0] == 2890527621
