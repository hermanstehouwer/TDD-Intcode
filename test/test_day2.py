from pytest import fixture

from intcode.logic import process
from intcode.processor.processor import IntcodeState
from intcode.io.make_processors import list2processor

@fixture
def day2_example_program_1():
    return list2processor([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])


@fixture
def day2_example_program_2():
    return list2processor([1, 0, 0, 0, 99])


@fixture
def day2_example_program_3():
    return list2processor([2, 3, 0, 3, 99])


@fixture
def day2_example_program_4():
    return list2processor([2, 4, 4, 5, 99, 0])


@fixture
def day2_example_program_5():
    return list2processor([1, 1, 1, 4, 99, 5, 6, 0, 99])


class TestLogicDay2:
    def test_take_one_step(self, day2_example_program_1):
        process.apply_instruction(day2_example_program_1.generate_instruction(), day2_example_program_1)
        assert day2_example_program_1.state[3] == 70
        assert day2_example_program_1.index == 4

    def test_take_two_steps(self, day2_example_program_1):
        process.apply_instruction(day2_example_program_1.generate_instruction(), day2_example_program_1)
        process.apply_instruction(day2_example_program_1.generate_instruction(), day2_example_program_1)
        assert day2_example_program_1.state[0] == 3500
        assert day2_example_program_1.index == 8

    def test_run_day2_program(self, day2_example_program_1):
        process.run_process(day2_example_program_1)
        assert day2_example_program_1.halted
        assert day2_example_program_1.state[0] == 3500
        assert day2_example_program_1.index == 8

    def test_run_day2_2(self, day2_example_program_2):
        process.run_process(day2_example_program_2)
        assert day2_example_program_2.halted
        assert day2_example_program_2.state[0] == 2

    def test_run_day2_3(self, day2_example_program_3):
        process.run_process(day2_example_program_3)
        assert day2_example_program_3.halted
        assert day2_example_program_3.state[3] == 6

    def test_run_day2_4(self, day2_example_program_4):
        process.run_process(day2_example_program_4)
        assert day2_example_program_4.halted
        assert day2_example_program_4.state[5] == 9801

    def test_run_day2_5(self, day2_example_program_5):
        process.run_process(day2_example_program_5)
        assert day2_example_program_5.halted
        assert day2_example_program_5.state == [30, 1, 1, 4, 2, 5, 6, 0, 99]
