def main():
    with open("day12.txt", "r") as f:
        text = f.read()
        S, E = text.index("S"), text.index("E")
        text = text.replace("S", "a").replace("E", "z")
        lines = text.split("\n")
        lenX, lenY = len(lines), len(lines[0])
        start, goal = (S // (lenY + 1), S % (lenY + 1)), (E // (lenY + 1), E % (lenY + 1))
        grid = [list(line) for line in lines]
        grid = [list(map(lambda x: ord(x) - 97, row)) for row in grid]

    visited = {start}
    last_visited: set[tuple] = {start}
    steps = 0
    while not goal in visited:
        steps += 1
        new_nodes: set[tuple] = set()
        for node in last_visited:
            new_nodes.update(neighbours(node, grid, lenX, lenY))
        visited.update(new_nodes)
        last_visited = new_nodes
    print(steps)

    visited = {goal}
    last_visited: set[tuple] = {goal}
    steps = 0
    stop = False
    while not stop:
        steps += 1
        new_nodes: set[tuple] = set()
        for node in last_visited:
            new_nodes.update(reverse_neighbours(node, grid, lenX, lenY))
        visited.update(new_nodes)
        for n in new_nodes:
            if grid[n[0]][n[1]] == 0:
                stop = True
                break
        last_visited = new_nodes
    print(steps)


def neighbours(node: tuple, grid: list, lenX: int, lenY: int) -> set:
    result = set()
    x, y = node[0], node[1]
    height = grid[x][y]
    if x > 0:
        if grid[x - 1][y] <= height + 1:
            result.add((x - 1, y))
    if x < lenX - 1:
        if grid[x + 1][y] <= height + 1:
            result.add((x + 1, y))
    if y > 0:
        if grid[x][y - 1] <= height + 1:
            result.add((x, y - 1))
    if y < lenY - 1:
        if grid[x][y + 1] <= height + 1:
            result.add((x, y + 1))
    return result


def reverse_neighbours(node: tuple, grid: list, lenX: int, lenY: int) -> set:
    result = set()
    x, y = node[0], node[1]
    height = grid[x][y]
    if x > 0:
        if grid[x - 1][y] >= height - 1:
            result.add((x - 1, y))
    if x < lenX - 1:
        if grid[x + 1][y] >= height - 1:
            result.add((x + 1, y))
    if y > 0:
        if grid[x][y - 1] >= height - 1:
            result.add((x, y - 1))
    if y < lenY - 1:
        if grid[x][y + 1] >= height - 1:
            result.add((x, y + 1))
    return result


if __name__ == "__main__":
    main()