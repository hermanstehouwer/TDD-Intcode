import copy
import itertools
from typing import List

from intcode.io import make_processors
from intcode.logic.process import run_process_till_output
from intcode.logic.processor_communication import StackInputClass, SingleOutputClass, set_input_and_output_classes
from intcode.processor.processor import IntcodeState

'''
https://adventofcode.com/2019/day/7
    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

'''


def run_amp_circuit(amps: List[int], processor_init: List[int]) -> int:
    input_signal = 0
    shared_input = StackInputClass()
    shared_output = SingleOutputClass()
    for phase_setting in amps:
        curr_processor = make_processors.list2processor(copy.deepcopy(processor_init))
        shared_input.value = [phase_setting, input_signal]
        set_input_and_output_classes(curr_processor, shared_input, shared_output)
        run_process_till_output(curr_processor, shared_output)
        input_signal = shared_output.value
        shared_output.reset()
    return input_signal


def find_max_amp_value(processor_init: List[int]) -> int:
    max_value = 0
    for amp in itertools.permutations(range(5)):
        curr_value = run_amp_circuit(amp, processor_init)
        max_value = max(curr_value, max_value)
    return max_value


'''
https://adventofcode.com/2019/day/7
      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)
'''


def run_feedback_loop(amps: List[int], processor_init: List[int]) -> int:
    input_signal = 0
    processors: List[IntcodeState] = []
    shared_input = StackInputClass()
    shared_output = SingleOutputClass()
    for phase_setting in amps:
        curr_processor = make_processors.list2processor(copy.deepcopy(processor_init))
        shared_input.value = [phase_setting, input_signal]
        set_input_and_output_classes(curr_processor, shared_input, shared_output)
        run_process_till_output(curr_processor, shared_output)
        input_signal = shared_output.value
        shared_output.reset()
        processors.append(curr_processor)
    stop = False
    last_value = input_signal
    while not stop:
        for curr_processor in processors:
            shared_input.value = [input_signal]
            run_process_till_output(curr_processor, shared_output)
            if curr_processor.halted:
                stop = True
            input_signal = shared_output.value
            shared_output.reset()
        if not stop:
            last_value = input_signal
    return last_value


def find_max_feedback_value(processor_init: List[int]) -> int:
    max_value = 0
    for amp in itertools.permutations(range(5,10)):
        curr_value = run_feedback_loop(amp, processor_init)
        max_value = max(curr_value, max_value)
    return max_value
