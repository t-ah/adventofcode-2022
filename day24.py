from collections import defaultdict


wind_moves = {"^": (0, -1), "<": (-1, 0), ">": (1, 0), "v": (0, 1)}
move_options = ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))


def main():
    print("Test", solve("day24_test.txt"))
    print("Real", solve("day24.txt"))


def solve(file_name):
    lines = read_input(file_name)
    max_x = len(lines[0]) - 2
    max_y = len(lines) - 2
    grid = defaultdict(list)
    for y in range(1, max_y + 1):
        for x in range(1, max_x + 1):
            if lines[y][x] != ".":
                grid[(x, y)].append(lines[y][x])

    start, goal = (1, 0), (max_x, max_y + 1)
    grid, steps1 = find(start, goal, grid, max_x, max_y)
    grid, steps2 = find(goal, start, grid, max_x, max_y)
    grid, steps3 = find(start, goal, grid, max_x, max_y)
    return steps1, steps1 + steps2 + steps3


def find(start, goal, grid, max_x, max_y):
    states = {start}
    step = 0
    while True:
        step += 1
        new_states = set()
        grid = move_grid(grid, max_x, max_y)
        for state in states:
            for move in move_options:
                new_pos = (state[0] + move[0], state[1] + move[1])
                if new_pos == goal:
                    return grid, step
                if new_pos[0] == 0 \
                        or new_pos[0] > max_x \
                        or (new_pos[1] <= 0 and new_pos != start) \
                        or (new_pos[1] > max_y and new_pos != start):
                    continue
                if len(grid[new_pos]) == 0:
                    new_states.add(new_pos)
        states = new_states


def move_grid(grid: defaultdict, max_x: int, max_y: int) -> defaultdict:
    new_grid = defaultdict(list)
    for x in range(1, max_x + 1):
        for y in range(1, max_y + 1):
            for c in grid[(x, y)]:
                new_grid[moved(x, y, c, max_x, max_y)].append(c)
    return new_grid


def moved(x, y, c, max_x, max_y):
    move = wind_moves[c]
    new_pos = [x + move[0], y + move[1]]
    if new_pos[0] == 0:
        new_pos[0] = max_x
    elif new_pos[0] > max_x:
        new_pos[0] = 1
    elif new_pos[1] == 0:
        new_pos[1] = max_y
    elif new_pos[1] > max_y:
        new_pos[1] = 1
    return tuple(new_pos)


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()
