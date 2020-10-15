from typing import List, Tuple

from intcode.logic.operators import inputBaseClass, outputBaseClass
from intcode.processor.processor import IntcodeState


class SingleInputClass(inputBaseClass):
    value: int

    def read(self) -> int:
        return self.value


class StackInputClass(inputBaseClass):
    value: List[int] = []

    def read(self) -> int:
        return self.value.pop(0)


class SingleOutputClass(outputBaseClass):
    value: int
    written: bool = False

    def write(self, i: int):
        self.value = i
        self.written = True

    def hasWritten(self):
        return self.written

    def reset(self):
        self.value = None
        self.written = False


class StackOutputClass(outputBaseClass):
    value: List[int]

    def __init__(self):
        self.value = []

    def write(self, i: int):
        self.value.append(i)


def get_input_and_output_classes(processor: IntcodeState) -> Tuple[inputBaseClass, outputBaseClass]:
    input_class: inputBaseClass = processor.instruction_map[3].input
    output_class: outputBaseClass = processor.instruction_map[4].output
    return (
        input_class,
        output_class
    )


def set_input_and_output_classes(processor: IntcodeState, new_input_class: inputBaseClass,
                                 new_output_class: outputBaseClass):
    processor.instruction_map[3].input = new_input_class
    processor.instruction_map[4].output = new_output_class