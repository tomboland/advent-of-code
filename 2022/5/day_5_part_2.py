from queue import LifoQueue
from parsy import regex
from typing import Literal, NewType, Iterable, List, cast
from enum import Enum
from funcy import takewhile, partial, drop
from dataclasses import dataclass
import re

EncodedCrate = Literal['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                       'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Crate = Enum("Crate", ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                       'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
EncodedStack = List[EncodedCrate]
Stack = LifoQueue[Crate]


@dataclass
class MoveInstruction(object):
    quantity: int
    source: int
    destination: int


def str_not_empty(s: str) -> bool:
    return s != ""


take_while_str_not_empty = partial(takewhile, str_not_empty)


def populate_stack(encoded_stack: EncodedStack) -> Stack:
    stack: Stack = LifoQueue()
    for encoded_crate in encoded_stack:
        stack.put(Crate[encoded_crate])
    return stack


crate_indexes = [1, 5, 9, 13, 17, 21, 25, 29, 33]


def parse_encoded_stacks(encoded_stacks: List[str]) -> List[Stack]:
    stacks: List[Stack] = [LifoQueue(), LifoQueue(), LifoQueue(), LifoQueue(
    ), LifoQueue(), LifoQueue(), LifoQueue(), LifoQueue(), LifoQueue()]
    for row in drop(1, reversed(encoded_stacks)):
        for index, crate_index in enumerate(crate_indexes):
            if len(row) > crate_index and row[crate_index] != " ":
                stacks[index].put(Crate[row[crate_index]])
    return stacks


instruction_re = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse_encoded_instructions(encoded_instructions: List[str]) -> List[MoveInstruction]:
    instructions: List[MoveInstruction] = []
    for encoded_instruction in encoded_instructions:
        m = re.match(instruction_re, encoded_instruction)
        if not m:
            continue
        quantity, source, destination = m.groups()
        instructions.append(
            MoveInstruction(int(quantity), int(source), int(destination))
        )
    return instructions


def move_crate(stacks, move_instruction: MoveInstruction) -> None:
    crates_to_move: List[Crate] = []
    for _i in range(0, move_instruction.quantity):
        crates_to_move.append(stacks[move_instruction.source - 1].get())
    for crate in crates_to_move[::-1]:
        stacks[move_instruction.destination - 1].put(crate)


if __name__ == "__main__":
    with open("input", 'r') as f:
        stripped = map(str.strip, f)
        encoded_stacks = list(take_while_str_not_empty(stripped))
        encoded_instructions = list(take_while_str_not_empty(stripped))
        parsed_stacks = parse_encoded_stacks(encoded_stacks)
        parsed_instructions = parse_encoded_instructions(encoded_instructions)
        for instruction in parsed_instructions:
            move_crate(parsed_stacks, instruction)
        print(''.join([str(stack.get().name) for stack in parsed_stacks]))
