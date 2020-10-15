import copy
from typing import List

from intcode.io.make_processors import file2processor, file2processor_init
from intcode.logic import process
from intcode.logic.processor_communication import SingleInputClass, SingleOutputClass, set_input_and_output_classes, \
    StackOutputClass
from intcode.logic.amp_circuit import find_max_amp_value, find_max_feedback_value
from intcode.processor.processor import IntcodeState

day2file = "../data/day2_input.txt"
day5file = "../data/day5_input.txt"
day7file = "../data/day7_input.txt"
day9file = "../data/day9_input.txt"



def set_noun_and_verb(processor: IntcodeState, noun: int, verb: int):
    processor.state[1] = noun
    processor.state[2] = verb


def get_deepcopy_with_noun_and_verb(processor: IntcodeState, noun: int, verb: int) -> IntcodeState:
    ret = copy.deepcopy(processor)
    set_noun_and_verb(ret, noun, verb)
    return ret


def day2part1():
    processor = file2processor(day2file)
    set_noun_and_verb(processor, 12, 2)
    process.run_process(processor)
    print(processor.state[0])


def day2part2():
    processor = file2processor(day2file)
    for noun in range(99):
        for verb in range(99):
            currentProcessor = get_deepcopy_with_noun_and_verb(processor, noun, verb)
            process.run_process(currentProcessor)
            if currentProcessor.state[0] == 19690720:
                print(100 * noun + verb)
                return


def run_processor_with_single_input(processor: IntcodeState, input: int) -> List[int]:
    newInputclass = SingleInputClass()
    newOutputClass = StackOutputClass()
    set_input_and_output_classes(processor, newInputclass, newOutputClass)
    newInputclass.value = input
    process.run_process(processor)
    return newOutputClass.value


def day5part1():
    processor = file2processor(day5file)
    run_processor_with_single_input(processor, 1)

def day5part2():
    processor = file2processor(day5file)
    run_processor_with_single_input(processor, 5)

def day7part1():
    processor_init = file2processor_init(day7file)
    print(find_max_amp_value(processor_init))

def day7part2():
    processor_init = file2processor_init(day7file)

def day9part1():
    processor = file2processor(day9file)
    run_processor_with_single_input(processor, 1)

def day9part2():
    processor = file2processor(day9file)
    run_processor_with_single_input(processor, 2)


if __name__ == "__main__":
    #day2part1()
    #day2part2()
    #day5part1()
    #day5part2()
    #day7part1()
    #day7part2()
    #day9part1()
    day9part2()
