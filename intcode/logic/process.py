from intcode.logic.processor_communication import SingleOutputClass
from intcode.logic.operators import *
from intcode.processor.processor import *


def init_processor(processor: IntcodeState):
    processor.instruction_map = {
        1: AdditionOperator(),
        2: MultiplicationOperator(),
        3: InputOperator(),
        4: OutputOperator(),
        5: JumpIfTrueOperator(),
        6: JumpIfFalseOperator(),
        7: LessThanOperator(),
        8: EqualsOperator(),
        9: AdjustRelativeBaseOperator(),
        99: HaltingOperator()
    }


def apply_instruction(instruction: Instruction, processor: IntcodeState):
    if instruction.operator not in processor.instruction_map.keys():
        print(f"debug for operator {instruction.operator}: idx:{processor.index}, halted:{processor.halted}")
        print(f"{processor.state}")
        raise ValueError()
    processor.instruction_map[instruction.operator].apply_operator(processor, instruction)


def run_process_till_output(processor: IntcodeState, output_class: SingleOutputClass):
    while processor.not_halted() and not output_class.hasWritten():
        apply_instruction(processor.generate_instruction(), processor)


def run_process(processor: IntcodeState):
    while processor.not_halted():
        apply_instruction(processor.generate_instruction(), processor)


