import pytest
from pytest import fixture

from intcode.io import make_processors
from intcode.io.make_processors import list2processor
from intcode.logic import process
from intcode.logic.processor_communication import StackOutputClass, set_input_and_output_classes
from intcode.processor.processor import IntcodeState


@fixture
def example_intcode_processor():
    return IntcodeState([1, 9, 10, 3])


@fixture
def make_16_digit_number():
    return [1102, 34915192, 34915192, 7, 4, 7, 99, 0]


@fixture
def print_middle_number():
    return [104, 1125899906842624, 99]


@fixture
def example_filename():
    return "data/day2_testfile.txt"


class TestProcessorBasics:
    def test_get_instruction_out_of_bounds(self, example_intcode_processor):
        with pytest.raises(IndexError):
            example_intcode_processor.index = -100
            example_intcode_processor.generate_instruction()
        with pytest.raises(IndexError):
            example_intcode_processor.index = 999
            instruction = example_intcode_processor.generate_instruction()
            assert instruction.operator == 0

    def test_large_number(self, make_16_digit_number):
        processor = list2processor(make_16_digit_number)
        output_class = StackOutputClass()
        set_input_and_output_classes(processor, None, output_class)
        process.run_process(processor)
        assert output_class.value[0] == 34915192 * 34915192

    def test_large_number_2(self, print_middle_number):
        processor = list2processor(print_middle_number)
        output_class = StackOutputClass()
        set_input_and_output_classes(processor, None, output_class)
        process.run_process(processor)
        assert output_class.value[0] == 1125899906842624


class TestIO:
    def test_read_testfile(self, example_intcode_processor, example_filename):
        assert make_processors.file2processor(example_filename) == example_intcode_processor
