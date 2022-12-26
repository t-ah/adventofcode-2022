from collections import Counter


def main():
    with open("day06.txt", "r") as f:
        line = f.read()
    print(next_marker(line, 0, 4))
    print(next_marker(line, 0, 14))


def next_marker(line: str, start: int, length: int) -> int:
    for i in range(start, len(line) - length + 1):
        mc = Counter(line[i : i + length]).most_common(1)[0]
        if mc[1] == 1:
            return i + length
    return -1


if __name__ == "__main__":
    main()