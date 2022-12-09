import re
from typing import Optional, Set, Tuple

input_line_re = re.compile("(\d+)-(\d+),(\d+)-(\d+)")


def parse_input_line(line: str) -> Optional[Tuple[Set, Set]]:
    m = re.match(input_line_re, line)
    if m and len(m.groups()) == 4:
        start_one, end_one, start_two, end_two = map(int, m.groups())
        return set(range(start_one, end_one + 1)), set(range(start_two, end_two + 1))
    else:
        return None


if __name__ == "__main__":
    with open("input", 'r') as f:
        count = 0
        for line in f:
            parsed = parse_input_line(line)
            if not parsed:
                continue
            one, two = parsed
            print(one & two)
            if one & two:
                count += 1
    print(count)
