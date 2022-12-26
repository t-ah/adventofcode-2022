def main():
    cubes = read_input("day18.txt")
    cube_set = set(cubes)
    sides = 0
    for cube in cubes:
        sides += len(list(filter(lambda n: n not in cube_set, neighbours(cube))))
    print(sides)

    sides = 0
    max_xyz = [max(cubes, key=lambda c: c[i])[i] for i in range(3)]
    internal_cache, external_cache = set(), set()
    for cube in cubes:
        sides += len(list(
            filter(lambda n: n not in cube_set and not is_internal(n, cubes, max_xyz, internal_cache, external_cache),
                   neighbours(cube))))
    print(sides)


def is_internal(cube, cubes, max_xyz, internal_cache, external_cache) -> bool:
    if cube in internal_cache:
        return True
    if cube in external_cache:
        return False
    visited = {cube}
    new_nodes = {cube}
    while len(new_nodes) > 0:
        current_nodes = new_nodes
        new_nodes = set()
        for node in current_nodes:
            for neighbour in neighbours(node):
                if neighbour not in cubes and neighbour not in visited:
                    visited.add(neighbour)
                    new_nodes.add(neighbour)
                    for i in range(3):
                        if neighbour[i] > max_xyz[i] or neighbour[i] < 0:
                            external_cache.update(visited)
                            return False
    internal_cache.update(visited)
    return True


def neighbours(cube) -> tuple:
    x, y, z = cube
    return (x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)


def read_input(file_name):
    with open(file_name, "r") as f:
        return [tuple(map(int, ls.split(","))) for ls in f.read().split("\n")]


if __name__ == "__main__":
    main()
