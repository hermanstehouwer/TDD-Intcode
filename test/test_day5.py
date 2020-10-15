import copy
from typing import Tuple

import pytest
from pytest import fixture

import intcode.logic.processor_communication
from intcode.io.make_processors import list2processor
from intcode.logic import process
from intcode.logic.process import *
from intcode.logic.processor_communication import SingleInputClass, SingleOutputClass
from intcode.processor.processor import *


@fixture
def parameter_mode_example():
    return list2processor([1002, 4, 3, 4, 33])


@fixture
def program_999_1000_1001():
    """
    intcode test program that is supposed to output:
        999  if input <  8
        1000 if input == 8
        1001 if input >  8
    """
    return [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002,
            21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98,
            99]


def make_and_set_test_input_and_output(processor: IntcodeState) -> Tuple[inputBaseClass, outputBaseClass]:
    new_input_class = SingleInputClass()
    new_output_class = SingleOutputClass()
    intcode.logic.processor_communication.set_input_and_output_classes(processor, new_input_class, new_output_class)
    return new_input_class, new_output_class


class TestDay5:
    def test_parse_parameter_modes(self):
        instruction = Instruction(1002)
        assert instruction.operator == 2
        assert instruction.parameter_modes[0] == ParameterMode.ADDRESS
        assert instruction.parameter_modes[1] == ParameterMode.DIRECT
        assert instruction.parameter_modes[2] == ParameterMode.ADDRESS

    def test_get_parsed_parameter_mode_from_processor(self, parameter_mode_example):
        instruction = parameter_mode_example.generate_instruction()
        assert instruction.operator == 2
        assert instruction.parameter_modes[0] == ParameterMode.ADDRESS
        assert instruction.parameter_modes[1] == ParameterMode.DIRECT
        assert instruction.parameter_modes[2] == ParameterMode.ADDRESS

    @staticmethod
    def run_input_output_test(processor_init, input_value, expected_output):
        processor = list2processor(copy.deepcopy(processor_init))
        old_input_class, old_output_class = intcode.logic.processor_communication.get_input_and_output_classes(
            processor)
        inputclass, outputclass = make_and_set_test_input_and_output(processor)

        inputclass.value = input_value
        process.run_process(processor)
        assert outputclass.value == expected_output

        intcode.logic.processor_communication.set_input_and_output_classes(processor, old_input_class, old_output_class)

    @pytest.mark.parametrize("processor_init", [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [3, 3, 1108, -1, 8, 3, 4, 3, 99]])
    @pytest.mark.parametrize("input_value, expected_output", [(0, 0), (8, 1), (12, 0)])
    def test_should_be_1_if_equal_to_eight(self,
                                           processor_init,
                                           input_value,
                                           expected_output):
        self.run_input_output_test(processor_init, input_value, expected_output)

    @pytest.mark.parametrize("processor_init", [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [3, 3, 1107, -1, 8, 3, 4, 3, 99]])
    @pytest.mark.parametrize("input_value, expected_output", [(1, 1), (7, 1), (8, 0), (12, 0)])
    def test_should_be_1_if_less_than_eight(self,
                                            processor_init,
                                            input_value,
                                            expected_output):
        self.run_input_output_test(processor_init, input_value, expected_output)

    @pytest.mark.parametrize("processor_init", [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
                                                [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]])
    @pytest.mark.parametrize("input_value, expected_output", [(0, 0), (1, 1)])
    def test_should_be_1_if_non_zero(self,
                                     processor_init,
                                     input_value,
                                     expected_output):
        self.run_input_output_test(processor_init, input_value, expected_output)

    @pytest.mark.parametrize("input_value, expected_output", [(0, 999), (-300, 999), (8, 1000), (9, 1001), (999, 1001)])
    def test_999_1000_1001(self, program_999_1000_1001, input_value, expected_output):
        self.run_input_output_test(program_999_1000_1001, input_value, expected_output)
