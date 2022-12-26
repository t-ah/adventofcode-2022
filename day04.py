import re

def main():
    with open("day04.txt", "r") as f:
        lines = f.read().split("\n")
    p = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    groups = [re.search(p, l).groups() for l in lines]
    nums = [[int(x) for x in g] for g in groups]
    
    contained = filter(is_contained, nums)
    print(len(list(contained)))

    overlap = filter(overlaps, nums)
    print(len(list(overlap)))


def is_contained(bounds: list) -> bool:
    startA, endA, startB, endB = bounds[0], bounds[1], bounds[2], bounds[3]
    if startB >= startA and startB <= endA and endB <= endA:
        return True
    if startA >= startB and startA <= endB and endA <= endB:
        return True
    return False


def overlaps(bounds: list) -> bool:
    startA, endA, startB, endB = bounds[0], bounds[1], bounds[2], bounds[3]
    return (startA >= startB and startA <= endB) or (startB >= startA and startB <= endA)

if __name__ == "__main__":
    main()