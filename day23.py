directions = ((0, -1, 0), (0, 1, 0), (-1, 0, 1), (1, 0, 1))


def main():
    solve("day23_test.txt")
    solve("day23.txt")


def get_proposal(pos, grid, start_direction_i):
    if is_all_free(pos, grid):
        return None
    for i in range(4):
        direction_i = (start_direction_i + i) % 4
        direction = directions[direction_i]
        pos_m = [pos[0] + direction[0], pos[1] + direction[1]]
        if tuple(pos_m) in grid:
            continue
        pos_m[direction[2]] -= 1
        if tuple(pos_m) in grid:
            continue
        pos_m[direction[2]] += 2
        if tuple(pos_m) in grid:
            continue
        pos_m[direction[2]] -= 1
        return tuple(pos_m)
    return None


def simulate(grid, start_direction_i) -> bool:
    moves = dict()
    blocked = set()
    for pos in grid:
        p = get_proposal(pos, grid, start_direction_i)
        if p is None:
            continue
        if p in blocked:
            del moves[p]
            continue
        blocked.add(p)
        moves[p] = pos
    for z, a in moves.items():
        grid.remove(a)
        grid.add(z)
    return len(moves) == 0


def is_all_free(pos, grid) -> bool:
    x, y = pos
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx, dy) == (0, 0):
                continue
            if (x + dx, y + dy) in grid:
                return False
    return True


def print_grid(grid):
    min_x, max_x, min_y, max_y = bound(grid, 0, min), bound(grid, 0, max), bound(grid, 1, min), bound(grid, 1, max)
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if (x, y) in grid else "."
        print(line)
    print()


def solve(file_name):
    grid = read_input(file_name)
    for i in range(10):
        simulate(grid, i % 4)
    min_x, max_x, min_y, max_y = bound(grid, 0, min), bound(grid, 0, max), bound(grid, 1, min), bound(grid, 1, max)
    print(((max_x - min_x + 1) * (max_y - min_y + 1)) - len(grid))

    grid = read_input(file_name)
    i = -1
    while True:
        i += 1
        if simulate(grid, i % 4):
            print(i + 1)
            break


def bound(grid, i, fnc):
    return fnc(grid, key=lambda p: p[i])[i]


def read_input(file_name):
    with open(file_name, "r") as f:
        lines = f.read().split("\n")
        grid = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    grid.add((x, y))
    return grid


if __name__ == "__main__":
    main()
