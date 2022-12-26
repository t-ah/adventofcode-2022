import ast
from functools import cmp_to_key, reduce


def main():
    lines = read_input("day13.txt")
    indices = []
    pair_index = 0
    packets = [[[2]], [[6]]]
    for i in range(0, len(lines), 3):
        pair_index += 1
        left = ast.literal_eval(lines[i])
        right = ast.literal_eval(lines[i + 1])
        packets.extend([left, right])
        order = compare(left, right)
        if order < 0:
            indices.append(pair_index)
    print(sum(indices))

    packets.sort(key=cmp_to_key(compare))
    print(reduce(lambda x, y: (x[0]+1) * (y[0]+1), filter(lambda x: x[1] in [[[2]], [[6]]], enumerate(packets))))


def compare(left, right):
    if type(left) is int and type(right) is int:
        return left - right

    l = left if type(left) is list else [left]
    r = right if type(right) is list else [right]

    for i in range(len(l)):
        if i >= len(r):
            return 1
        sub_comparison = compare(l[i], r[i])
        if sub_comparison != 0:
            return sub_comparison
    if len(r) > len(l):
        return -1
    return 0


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()