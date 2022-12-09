from dataclasses import dataclass
from typing import NewType, NamedTuple, Callable
import pytest
from parsy import string, whitespace, digit, letter, seq, match_item
import hypothesis.strategies as st
from pprint import pprint


DirectoryName = NewType("DirectoryName", str)
FileSize = NewType("FileSize", int)
FileName = NewType("FileName", str)


@dataclass
class CdCommand(object):
    directory_name: DirectoryName


class LsCommand(object):
    pass


class File(NamedTuple):
    name: str
    size: int


@dataclass
class Directory(object):
    name: DirectoryName
    directories: list["Directory"]
    files: set[File]


HistoryEntry = CdCommand | LsCommand | File | Directory


def tree_size(directory: Directory) -> FileSize:
    return FileSize(
        sum([tree_size(d) for d in directory.directories])
        + sum([f.size for f in directory.files])
    )


def tree_size_filter(directory: Directory, max_size: FileSize) -> \
        list[tuple[Directory, FileSize]]:
    filtered = tree_filter(lambda d: tree_size(d) <= max_size, directory)
    return [(d, tree_size(d)) for d in filtered]


def tree_filter(f: Callable[[Directory], bool], directory: Directory) -> list[Directory]:
    return [
        fd for fd in filter(f, [directory] + [
            cd for child in directory.directories for cd in tree_filter(f, child)
        ])
    ]


@dataclass
class CdDirCommand(object):
    directory_name: DirectoryName


# _p suffix denotes parser
ws_p = whitespace
eol_p = match_item("\n")
filesize_p = digit.many()
filename_p = seq(
    letter.many(), string(".").map(lambda c: [c]), letter.many()
) | letter.many()
file_entry_p = seq(filesize_p << ws_p, filename_p).map(
    lambda args: File(FileName(''.join([''.join(xs) for xs in args[1]])), FileSize(int(''.join(args[0])))))
dir_name_p = letter.many()
dir_entry_p = string("dir") >> ws_p >> dir_name_p.map(
    lambda name: Directory(name=DirectoryName(''.join(name)), directories=[], files=set()))
command_prompt_p = string("$")
cd_command_p = command_prompt_p >> ws_p >> string("cd")
cd_root_p = cd_command_p >> ws_p >> string("/").map(
    lambda _: CdCommand(DirectoryName("/"))
)
cd_dir_p = cd_command_p >> ws_p >> dir_name_p.concat().map(
    lambda dir_name: CdCommand(DirectoryName(dir_name)))
cd_up_p = cd_command_p >> ws_p >> string(
    "..").map(lambda _: CdCommand(DirectoryName("..")))
ls_command_p = command_prompt_p >> ws_p >> string(
    "ls").map(lambda _: LsCommand())
statement_p = file_entry_p | cd_root_p | cd_up_p | cd_dir_p | ls_command_p | dir_entry_p | eol_p


@pytest.fixture
def root_dir():
    return Directory(name=DirectoryName("/"), directories=[], files=[])


lower_case_letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
upper_case_letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
digits = [chr(i) for i in range(ord('0'), ord('9')+1)]

at_least_one_alpha = st.text(
    alphabet=lower_case_letters + upper_case_letters, min_size=1)


def unsafe_stack_peek(stack: list[Directory]) -> Directory:
    return stack[-1]


def unsafe_stack_pop(stack: list[Directory]) -> Directory:
    return stack.pop()


def unsafe_stack_append(stack: list[Directory], dir: Directory) -> None:
    stack.append(dir)


def reconstruct_fs_from_history(history: list[HistoryEntry]) -> Directory:
    root_dir = Directory(name=DirectoryName("/"), directories=[], files=set())
    dir_stack: list[Directory] = []
    def cur_dir(): return unsafe_stack_peek(dir_stack)
    dir_stack.append(root_dir)

    for entry in history:
        match entry:

            case CdCommand(directory_name="/"):
                dir_stack.clear()
                dir_stack.append(root_dir)

            case CdCommand(directory_name=".."):
                unsafe_stack_pop(dir_stack)

            case CdCommand(directory_name=directory_name):
                try:
                    unsafe_stack_append(
                        dir_stack,
                        next((
                            d for d in cur_dir().directories
                            if d.name == directory_name)))
                except StopIteration:
                    new_dir = Directory(
                        name=DirectoryName(directory_name),
                        directories=[],
                        files=set())
                    cur_dir().directories.append(new_dir)
                    unsafe_stack_append(dir_stack, new_dir)

            case LsCommand():
                pass

            case Directory(name=name):
                if name not in [d.name for d in cur_dir().directories]:
                    cur_dir().directories.append(entry)

            case File():
                if entry not in cur_dir().files:
                    cur_dir().files.add(entry)

            case _:
                print(entry)
                return "This is a bug!"

    return root_dir


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


@pytest.fixture
def test_tree_a():
    return Directory(
        name="/",
        directories=[
            Directory(
                name="a",
                directories=[
                    Directory(
                        name="b",
                        directories=[],
                        files=[
                            File(name=FileName("a"), size=FileSize(10))
                        ]
                    ),
                    Directory(
                        name="c",
                        directories=[],
                        files=[
                            File(name=FileName("a"), size=FileSize(10)),
                            File(name=FileName("b"), size=FileSize(20)),
                            File(name=FileName("c"), size=FileSize(30)),
                        ]
                    )],
                files=[
                    File(name=FileName("a"), size=FileSize(10)),
                    File(name=FileName("b"), size=FileSize(20)),
                ]
            ),
            Directory(
                name="d",
                directories=[],
                files=[
                    File(name=FileName("a"), size=FileSize(10)),
                    File(name=FileName("b"), size=FileSize(20)),
                ]
            )
        ],
        files=[
            File(name=FileName("a"), size=FileSize(10)),
            File(name=FileName("b"), size=FileSize(20)),
        ])


@pytest.fixture
def test_tree_b():
    return Directory(
        name='/',
        directories=[
            Directory(
                name='a',
                directories=[
                    Directory(name='a',
                              directories=[],
                              files={File(name=FileName('fa'), size=FileSize(10)),
                                     File(name=FileName('fb'), size=FileSize(20))}),
                    Directory(name='b',
                              directories=[],
                              files={File(name=FileName('fa'), size=FileSize(20)),
                                     File(name=FileName('fb'), size=FileSize(30))})],
                files=set()),
            Directory(name='b', directories=[], files=set())],
        files=set())


def test_treesize_correctly_sizes_test_tree(test_tree):
    assert tree_size(test_tree) == FileSize(160)


def test_tree_size_filter_output_sums_correctly(test_tree):
    sized = tree_size_filter(test_tree, 10)
    size = FileSize(sum(sz[1] for sz in sized))
    assert size == FileSize(10)
    assert sized[0][0].name == "b"


def test_tree_filter_works_in_basic_sense():
    tree = Directory(name=DirectoryName("a"), directories=[], files=[])
    filtered = tree_filter(lambda d: d.name == "a", tree)
    assert filtered[0].name == "a"


def test_tree_filter_works_with_test_tree(test_tree):
    filtered = tree_filter(lambda d: tree_size(d) >= 20, test_tree)
    assert set([d.name for d in filtered]) == set(["/", "a", "c", "d"])


def total_size_of_all_directories_gt_100k(tree: Directory) -> FileSize:
    filtered = tree_size_filter(fs, FileSize(100000))
    return FileSize(sum(entry[1] for entry in filtered))


def find_size_of_smallest_dir_large_enough_to_remove_taking_the_fs_over_threshold_free_space(tree: Directory) \
        -> FileSize:
    TOTAL_DISK_SPACE = 70000000
    TOTAL_REQUIRED_SPACE = 30000000
    total_used = tree_size(tree)
    threshold = TOTAL_REQUIRED_SPACE - (TOTAL_DISK_SPACE - total_used)
    filtered_tree = tree_filter(lambda d: tree_size(d) >= FileSize(threshold), tree)
    sized_dirs = [(d, tree_size(d)) for d in filtered_tree]
    sorted_tree = sorted(sized_dirs, key=lambda t: t[1])
    pprint(sorted_tree)
    return sorted_tree[0][1]


if __name__ == "__main__":
    with open("input", 'r') as f:
        input = f.read()
        history = statement_p.sep_by(eol_p).parse(input)
    fs = reconstruct_fs_from_history(history)
    filtered_tree = tree_size_filter(fs, FileSize(100000))
    print(total_size_of_all_directories_gt_100k(fs))
    print(find_size_of_smallest_dir_large_enough_to_remove_taking_the_fs_over_threshold_free_space(fs))
