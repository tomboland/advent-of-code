def char_to_priority(c: str) -> int:
    if c.islower():
        return ord(c) - 97 + 1
    else:
        return ord(c) - 65 + 27


if __name__ == "__main__":
    with open("input", 'r') as f:
        totes = 0
        for line in map(str.rstrip, f):
            c1, c2 = set(line[:len(line) // 2]), set(line[len(line) // 2:])
            totes += char_to_priority(str(list(c1 & c2)[0]))
    print(totes)
