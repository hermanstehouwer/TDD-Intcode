from typing import List

from intcode.logic import process
from intcode.logic.processor_communication import SingleInputClass
from intcode.processor.processor import IntcodeState


def file2processor(filename: str) -> IntcodeState:
    processor: IntcodeState = IntcodeState(file2processor_init(filename))
    process.init_processor(processor)
    return processor


def file2processor_init(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(elem) for elem in f.read().split(",")]


def list2processor(list: List[int]) -> IntcodeState:
    processor: IntcodeState = IntcodeState(list)
    process.init_processor(processor)
    return processor
