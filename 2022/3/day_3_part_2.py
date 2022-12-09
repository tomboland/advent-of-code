from funcy import chunks


def char_to_priority(c: str) -> int:
    if c.islower():
        return ord(c) - 97 + 1
    else:
        return ord(c) - 65 + 27


if __name__ == "__main__":
    with open("input", 'r') as f:
        totes = 0
        for one, two, three in chunks(3, map(str.rstrip, f)):
            r1, r2, r3 = set(one), set(two), set(three)
            totes += char_to_priority(str(list(r1 & r2 & r3)[0]))
    print(totes)
