from dataclasses import dataclass
from typing import NewType
import pytest


DirectoryName = NewType("DirectoryName", str)
FileSize = NewType("FileSize", int)
FileName = NewType("FileName", str)


@dataclass
class File(object):
    name: str
    size: int


@dataclass
class Directory(object):
    name: DirectoryName
    directories: list["Directory"]
    files: list[File]


def tree_size(directory: Directory) -> FileSize:
    return FileSize(
        sum([tree_size(d) for d in directory.directories])
        + sum([f.size for f in directory.files])
    )


@pytest.fixture
def test_tree():
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


def test_treesize_correctly_sizes_test_tree(test_tree):
    assert tree_size(test_tree) == FileSize(160)


if __name__ == "__main__":
    with open("input", 'r') as f:
        pass
