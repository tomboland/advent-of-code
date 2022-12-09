import pytest
from day_7 import statement_p, eol_p, HistoryEntry, CdCommand, LsCommand, File, Directory, reconstruct_fs_from_history
from pprint import pprint


@pytest.fixture
def aoc_input():
    with open("input", 'r') as f:
        return f.read()


@pytest.fixture
def simple_input():
    return """$ cd /
$ ls
dir a
dir b
$ cd a
$ ls
10 fa
20 fb
$ cd ..
$ cd b
$ ls
20 fa
30 fb"""


def test_simple_input_is_parsed_correctly(simple_input):
    history = statement_p.sep_by(eol_p).parse(simple_input)
    fs = reconstruct_fs_from_history(history)
    pprint(fs)
    assert False


def serialise_history_entries(history: list[HistoryEntry]) -> str:
    return "\n".join([serialise_history_entry(entry) for entry in history])


def serialise_history_entry(entry: HistoryEntry) -> str:
    match entry:
        case CdCommand(directory_name=directory_name):
            return f"$ cd {directory_name}"
        case LsCommand():
            return "$ ls"
        case Directory(name=name):
            return f"dir {name}"
        case File(name=name, size=size):
            return f"{size} {name}"
        case _:
            print("Why are we here?")
            assert False


def test_input_can_be_parsed_and_reserialised(aoc_input):
    history = statement_p.sep_by(eol_p).parse(aoc_input)
    assert serialise_history_entries(history) == aoc_input
