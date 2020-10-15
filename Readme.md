# Overview
## Intcode Processor

Herein you will find an examplar implementation of the intcode processor from the Advent-of-Code 2019 assignments.
The intcode processor is described in the following AoC assignments:
- https://adventofcode.com/2019/day/2
- https://adventofcode.com/2019/day/5
- https://adventofcode.com/2019/day/7
- https://adventofcode.com/2019/day/9

The solutions to these problems can be calculated using the calls in intcode/main.py

## Motivation

This code was written in order to have a good examplar demostration of how to write a somewhat larger Python project.
Using as a base: 
- Clean Coding (i.e. the code is readable and tells you what it does, also by its naming)
- Clean Architecture (more on this below)
- Testdriven Development (TDD) (i.e. we write the tests before we write the code)

If you look at the commit history of the archive you can also see how the core datamodel (and the things around it) changed in order to respond to changing requirements.

##Clean Architecture
See https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html for a short explanation.

# Code overview
- The code for the processor can be found in intcode/
- The code for all the tests can be found in test/

## intcode code structure
Intcode contains the main.py, which is just the glue that calls the other modules in order to answer the AoC assignments.

### intcode/processor

This is our entity-model of an intcode processor.
It has no dependencies (imports) outside of intcode/processor.
It only contains the processor-model itself and some small definitions (parameters, instructions) that it needs.

### intcode/logic

This is our use-cases and controlers; or **business logic** part of the code.
It deals with:
 - The operations you want to perform on the processor-state (e.g. addition, jumpifequals, etc.) in operators.py
 - Hooking into the input and output operators in processor_communication.py
 - Initializing and running the program contained in the processor state in process.py
 - Building and running the "amp" and "feedback" multi-processor combinations as required for AoC day7 in amp_circuit.py

### intcode/io
This is our external connections layer.
This deals with:
- Creating a processor based on a file or based on an in-memory list.

## Testcode code structure
The testcode is divided in two ways:
- test_processor.py which contains some basic tests.
- test_dayX which contain the tests added for the modifications of that day.

# Howto use:
Please look at main.py or the testcases to see how to call an intcode processor.
It may be useful to subclass inputBaseClass en outputBaseClass (located in intcode/logic/operators.py) in order to be able to hook into the input and output of your intcode program. 