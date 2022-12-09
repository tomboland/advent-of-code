from funcy import chunks

if __name__ == "__main__":
    with open("input", 'r') as f:
        signal = f.readline()

    for count, chunk in enumerate(chunks(4, 1, signal)):
        if len(set(chunk)) == 4:
            print(chunk, count + 4)
            break
