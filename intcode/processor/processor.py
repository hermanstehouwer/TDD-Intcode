from abc import abstractmethod, ABC
from enum import Enum
from typing import List, Mapping


class ParameterMode(Enum):
    ADDRESS = 0
    DIRECT = 1
    RELATIVE_BASE = 2


class Parameter:
    val: int
    mode: ParameterMode

    def __init__(self, val: int, mode: ParameterMode):
        self.val = val
        self.mode = mode

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return False
        return self.val == other.val \
               and self.mode == other.mode

    def __str__(self):
        return "%s:%s" % (self.val, self.mode)


class Parameters:
    parameters: List[Parameter]

    def __init__(self):
        self.parameters = []

    def __eq__(self, other):
        if not isinstance(other, Parameters):
            return False
        return self.parameters == other.parameters

    def __str__(self):
        return " - ".join([str(p) for p in self.parameters])

    def num_steps(self) -> int:
        return len(self.parameters) + 1


class Instruction:
    operator: int
    parameter_modes: List[ParameterMode]

    def __init__(self, input: int):
        self.operator = input % 100
        self.parameter_modes = []
        self.parameter_modes.append(ParameterMode(int((input % 1000) / 100)))
        self.parameter_modes.append(ParameterMode(int((input % 10000) / 1000)))
        self.parameter_modes.append(ParameterMode(int((input) / 10000)))
        pass

    def __eq__(self, other):
        if not isinstance(other, Instruction):
            return False
        return self.operator == other.operator \
               and self.parameter_modes == other.parameter_modes


class OperatorInterface(ABC):
    @abstractmethod
    def apply_operator(self, processor, instruction: Instruction):
        pass


class IntcodeState:
    index: int
    relative_base: int
    state: List[int]
    halted: bool = False
    instruction_map: Mapping[int, OperatorInterface] = {}

    def __init__(self, state: List[int]):
        self.state = state
        self.index = 0
        self.relative_base = 0

    def __eq__(self, other):
        if not isinstance(other, IntcodeState):
            return False
        return self.index == other.index and self.state == other.state

    def _extend_if_needed(self, i: int):
        if i >= len(self.state):
            self.state = self.state + [0] * (i - len(self.state) + 1)

    def _get_value(self, i: int) -> int:
        self._extend_if_needed(i)
        return self.state[i]

    def set_value(self, i: int, value: int):
        self._extend_if_needed(i)
        self.state[i] = value
        return

    def get_address(self, param: Parameter) -> int:
        if param.mode == ParameterMode.ADDRESS:
            return param.val
        if param.mode == ParameterMode.RELATIVE_BASE:
            return self.relative_base + param.val
        raise ValueError(param)

    def get_value(self, param: Parameter) -> int:
        if param.mode == ParameterMode.DIRECT:
            return param.val
        if param.mode == ParameterMode.ADDRESS or param.mode == ParameterMode.RELATIVE_BASE:
            return self._get_value(self.get_address(param))
        raise ValueError(param)

    def generate_instruction(self) -> Instruction:
        return Instruction(self.state[self.index])

    def generate_parameters(self, number_parameters: int, instruction: Instruction) -> Parameters:
        param = Parameters()
        if number_parameters < 1 or number_parameters > 3:
            raise ValueError(f"number_parameters should be between 1 and 3, and not {number_parameters}")
        # +1 as range is exclusive
        self._extend_if_needed(self.index + number_parameters)
        for idx in range(1, number_parameters + 1):
            value = self.state[self.index + idx]
            # idx starts at 1, parameter_modes list index starts at 0.
            parameter_mode: ParameterMode = instruction.parameter_modes[idx - 1]
            param.parameters.append(Parameter(value, parameter_mode))
        return param

    def not_halted(self) -> bool:
        return not self.halted

    def halt(self):
        self.halted = True

    def step(self, step: int):
        self.index = self.index + step
