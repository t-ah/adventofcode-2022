from functools import reduce

def main():
    with open("day03.txt", "r") as f:
        lines = f.read().split("\n")
        duplicates = map(get_duplicate, lines)
        prios = map(get_priority, duplicates)
        print(sum(prios))

        sets = [set(x) for x in lines]
        groups = [sets[i : i + 3] for i in range(0, len(sets), 3)]
        commons = map(get_common, groups)
        prios = map(get_priority, commons)
        print(sum(prios))


def get_duplicate(line) -> str:
    lookup = set()
    part1, part2 = line[:len(line)//2], line[len(line)//2:]
    for c in part1:
        lookup.add(c)
    for c in part2:
        if c in lookup:
            return c
    raise Exception("No duplicate found")


def get_common(sets: list) -> str:
    return reduce(set.intersection, sets).pop()


def get_priority(c: str) -> int:
    prio = ord(c)
    if prio >= 97:
        return prio - 96
    else:
        return prio - 38


if __name__ == "__main__":
    main()