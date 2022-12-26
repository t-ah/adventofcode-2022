def main():
    coordinates = read_input("day15.txt")
    print(count_no_beacon(coordinates, 2000000))

    for y in range(4000000):
        if y % 100000 == 0:
            print(y)
        x = find_free_x(coordinates, y)
        if x == None:
            continue
        print(x, y, 4000000 * x + y)
        break


# this is slow but works
def count_no_beacon(coordinates: list, target_row: int) -> int:
    no_beacon = set()
    for (sx, sy, bx, by) in coordinates:
        distance = abs(sx - bx) + abs(sy - by)
        dist_target_y = abs(sy - target_row)
        if dist_target_y <= distance:
            x_offset = distance - dist_target_y
            for x in range(-x_offset, x_offset + 1):
                no_beacon.add(sx + x)
    for (_, _, bx, by) in coordinates:
        if by == target_row and bx in no_beacon:
            no_beacon.remove(bx)
    return len(no_beacon)


# this also works, but much faster
def find_free_x(coordinates: list, target_row: int):
    bounds = list()
    for (sx, sy, bx, by) in coordinates:
        distance = abs(sx - bx) + abs(sy - by)
        dist_target_y = abs(sy - target_row)
        if dist_target_y <= distance:
            x_offset = distance - dist_target_y
            bounds.append((sx - x_offset, sx + x_offset))
    bounds.sort()
    up_to = -1
    for bound in bounds:
        if bound[0] > up_to:
            return bound[0] - 1
        up_to = max(up_to, bound[1])
    return None


def read_input(file_name):
    with open(file_name, "r") as f:
        lines = f.read().split("\n")
        word_lists = [line.split(" ") for line in lines]
        coords = [(int(words[2][2:-1]), int(words[3][2:-1]), int(words[8][2:-1]), int(words[9][2:])) for words in word_lists]
        return coords


if __name__ == "__main__":
    main()