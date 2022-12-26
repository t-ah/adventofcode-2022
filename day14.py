test_positions = ((0, 1), (-1, 1), (1, 1))


def main():
    lines = read_input("day14.txt")
    grid = {}
    maxY = 0
    for line in lines:
        points = list(map(lambda x: [int(y) for y in x.split(",")], line.split(" -> ")))
        for i in range(len(points) - 1):
            pointA, pointB = points[i], points[i + 1]
            maxY = max(maxY, pointA[1], pointB[1])
            if pointA[0] == pointB[0]:
                for y in range(min(pointA[1], pointB[1]), max(pointA[1], pointB[1]) + 1):
                    grid[(pointA[0], y)] = "#"
            else:
                for x in range(min(pointA[0], pointB[0]), max(pointA[0], pointB[0]) + 1):
                    grid[(x, pointA[1])] = "#"
    sand = 0
    while add_sand(grid, (500, 0), maxY) != None:
        sand += 1
    print(sand)

    for x in range(500 - (maxY + 3), 500 + maxY + 3):
        grid[(x, maxY + 2)] = "#"
    while add_sand(grid, (500, 0), maxY) != (500, 0):
        sand += 1
    print(sand + 1)


def add_sand(grid, origin, maxY):
    current = origin
    while current[1] <= maxY + 2:
        next_pos = next_sand_pos(grid, current)
        if next_pos == None:
            grid[current] = "o"
            return current
        current = next_pos
    return None


def next_sand_pos(grid, current):
    for t in test_positions:
        current_next = (current[0] + t[0], current[1] + t[1])
        if current_next not in grid:
            return current_next
    return None


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()