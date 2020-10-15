from intcode.processor.processor import OperatorInterface, IntcodeState, Instruction


class inputBaseClass:
    def read(self) -> int:
        return int(input("value plz:"))


class outputBaseClass:
    def write(self, i: int):
        print(i)


class AdditionOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(3, instruction)
        processor.set_value(
            processor.get_address(param.parameters[2]),
            processor.get_value(param.parameters[0]) +processor.get_value(param.parameters[1])
        )
        processor.step(param.num_steps())


class MultiplicationOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(3, instruction)
        processor.set_value(
            processor.get_address(param.parameters[2]),
            processor.get_value(param.parameters[0]) * processor.get_value(param.parameters[1])
        )
        processor.step(param.num_steps())


class HaltingOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        processor.halt()


class InputOperator(OperatorInterface):
    input: inputBaseClass = inputBaseClass()

    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(1, instruction)
        processor.set_value(
            processor.get_address(param.parameters[0]),
            self.input.read()
        )
        processor.step(param.num_steps())


class OutputOperator(OperatorInterface):
    output: outputBaseClass = outputBaseClass()

    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(1, instruction)
        value = processor.get_value(param.parameters[0])
        self.output.write(value)
        processor.step(param.num_steps())


class JumpIfTrueOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(2, instruction)
        if processor.get_value(param.parameters[0]) != 0:
            processor.index = processor.get_value(param.parameters[1])
        else:
            processor.step(param.num_steps())


class JumpIfFalseOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(2, instruction)
        if processor.get_value(param.parameters[0]) == 0:
            processor.index = processor.get_value(param.parameters[1])
        else:
            processor.step(param.num_steps())


class LessThanOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(3, instruction)
        if processor.get_value(param.parameters[0]) \
                < processor.get_value(param.parameters[1]):
            processor.set_value(
                processor.get_address(param.parameters[2]),
                1
            )
        else:
            processor.set_value(
                processor.get_address(param.parameters[2]),
                0
            )
        processor.step(param.num_steps())


class EqualsOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(3, instruction)
        if processor.get_value(param.parameters[0]) \
                == processor.get_value(param.parameters[1]):
            processor.set_value(
                processor.get_address(param.parameters[2]),
                1
            )
        else:
            processor.set_value(
                processor.get_address(param.parameters[2]),
                0
            )
        processor.step(param.num_steps())


class AdjustRelativeBaseOperator(OperatorInterface):
    def apply_operator(self, processor: IntcodeState, instruction: Instruction):
        param = processor.generate_parameters(1, instruction)
        processor.relative_base += processor.get_value(param.parameters[0])
        processor.step(param.num_steps())
