from day_7 import DirectoryName, File, FileSize, FileName, Directory, tree_size, tree_filter, tree_size_filter
import pytest


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
