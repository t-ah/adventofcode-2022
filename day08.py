def main():
    with open("day08.txt", "r") as f:
        lines = f.read().split("\n")
    grid = map(list, lines)
    grid = [list(map(int, row)) for row in grid]
    
    visible = set()
    for x in range(len(grid)):
        row = grid[x]
        highest = -1
        for y in range(len(row)):
            height = grid[x][y]
            if height > highest:
                visible.add((x,y))
                highest = height
    
    lenX, lenY = len(grid), len(grid[0])
    check_visibility(grid, visible, (0, lenX, 1), (0, lenY, 1), False) # from left
    check_visibility(grid, visible, (0, lenX, 1), (lenY-1, -1, -1), False) # from right
    check_visibility(grid, visible, (0, lenY, 1), (0, lenX, 1), True) # from above
    check_visibility(grid, visible, (0, lenY, 1), (lenX-1, -1, -1), True) # from below
    print(len(visible))

    max_score = 0
    for x in range(lenX):
        for y in range(lenY):
            max_score = max(max_score, get_score(grid, x, y, lenX, lenY))
    print(max_score)


def check_visibility(grid: list, visible: set, outer_range_params: tuple, inner_range_params: tuple, switchXY: bool):
    for x in range(*outer_range_params):
        highest = -1
        for y in range(*inner_range_params):
            height = grid[x][y] if not switchXY else grid[y][x]
            if height > highest:
                visible.add((x,y) if not switchXY else (y,x))
                highest = height


def get_score(grid: list, x: int, y: int, lenX: int, lenY: int) -> int:
    right = count_lower(grid, grid[x][y], x, y+1, lenY, 1, False)
    left = count_lower(grid, grid[x][y], x, y-1, -1, -1, False)
    down = count_lower(grid, grid[x][y], y, x+1, lenX, 1, True)
    up = count_lower(grid, grid[x][y], y, x-1, -1, -1, True)
    return right * left * down * up


def count_lower(grid: list, start_height: int, fixed: int, start: int, end: int, direction: int, first_coord: bool) -> int:
    count = 0
    for i in range(start, end, direction):
        count += 1
        height = grid[i][fixed] if first_coord else grid[fixed][i]
        if height >= start_height:
            break
    return count


if __name__ == "__main__":
    main()