#!/usr/bin/env python
from typing import Tuple
from hypothesis import given
from hypothesis.strategies import integers


@given(integers())
def test_update_max_is_always_in_sorted_order(i):
    maxs = update_max((1, 2, 3), i)
    assert maxs == tuple(sorted(maxs))


@given(integers())
def test_update_max_always_sums_geq_than_input(i):
    maxs = update_max((1, 2, 3), i)
    assert sum(maxs) >= sum((1, 2, 3))


def update_max(maxs: Tuple[int, int, int], x: int) -> Tuple[int, int, int]:
    match maxs:
        case (_, mid, high) if x >= high:
            return (mid, high, x)
        case (_, mid, high) if x >= mid:
            return (mid, x, high)
        case (low, mid, high) if x >= low:
            return (x, mid, high)
        case _:
            return maxs


if __name__ == "__main__":
    with open("input", 'r') as f:
        maxs = (0, 0, 0)
        running_total = 0
        for line in f:
            stripped_line = line.strip()
            if stripped_line != "":
                running_total += int(stripped_line)
            else:
                maxs = update_max(maxs, running_total)
                running_total = 0
    print(sum(maxs))
