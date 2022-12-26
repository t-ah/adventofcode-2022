class Element:
    def __init__(self, value: int, index: int):
        self.value = value
        self.index = index


def mix(elements: list[Element]) -> list[Element]:
    starting_indices = {e.index: i for i, e in enumerate(elements)}
    moves = []
    for i in range(len(elements)):
        current_index = starting_indices[i]
        for del_i, ins_i in moves:
            if del_i < current_index:
                current_index -= 1
            if ins_i <= current_index:
                current_index += 1
        e = elements[current_index]
        new_position = (current_index + e.value) % (len(elements) - 1)

        elements = elements[:current_index] + elements[current_index + 1:]
        elements = elements[:new_position] + [e] + elements[new_position:]
        moves.append((current_index, new_position))
    return elements


def find_zero(elements: list[Element]) -> int:
    for i in range(len(elements)):
        if elements[i].value == 0:
            return i


def main():
    elements = read_input("day20.txt", 1)
    elements = mix(elements)
    zero_i = find_zero(elements)
    print(sum([elements[(zero_i + i) % len(elements)].value for i in (1000, 2000, 3000)]))

    elements = read_input("day20.txt", 811589153)
    for step in range(10):
        elements = mix(elements)
    zero_i = find_zero(elements)
    print(sum([elements[(zero_i + i) % len(elements)].value for i in (1000, 2000, 3000)]))


def read_input(file_name, factor: int):
    with open(file_name, "r") as f:
        return [Element(int(x) * factor, i) for i, x in enumerate(f.read().split("\n"))]


if __name__ == "__main__":
    main()
