moves = {"R":(1,0), "L":(-1,0), "D":(0,1), "U":(0,-1)}

def main():
    with open("day09.txt", "r") as f:
        lines = f.read().split("\n")
    simulate(2, lines)
    simulate(10, lines)


def simulate(n, lines):
    positions = [[0,0] for _ in range(n)]
    visited = set()

    for line in lines:
        parts = line.split(" ")
        direction, steps = parts[0], int(parts[1])
        for _ in range(steps):
            move(positions[0], direction)
            for i in range(1, n):
                follow(positions[i - 1], positions[i])
            visited.add(tuple(positions[-1]))
    print(len(visited))


def move(pos, direction):
    current_move = moves[direction]
    pos[0] += current_move[0]
    pos[1] += current_move[1]


def follow(posH, posT):
    v = vec(posT, posH)
    if abs(v[0]) > 1 or abs(v[1]) > 1:
        v = shorten_vec(v)
        posT[0] += v[0]
        posT[1] += v[1]


def vec(posA, posB):
    return (posB[0] - posA[0], posB[1] - posA[1])


def shorten_vec(v):
    return [v[i]//abs(v[i]) if v[i] != 0 else 0 for i in range(2)]


if __name__ == "__main__":
    main()