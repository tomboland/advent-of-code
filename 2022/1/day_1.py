#!/usr/bin/env python

if __name__ == "__main__":
    with open("input", 'r') as f:
        max = 0
        running_total = 0
        for line in f:
            stripped_line = line.strip()
            if stripped_line != "":
                running_total += int(stripped_line)
            elif running_total > max:
                max = running_total
                running_total = 0
            else:
                running_total = 0
            print(max)
