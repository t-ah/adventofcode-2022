from functools import reduce


def best_outcome(cost, steps) -> int:
    print(cost)
    start_state = ((1, 0, 0, 0), (0, 0, 0, 0))
    states = {start_state}
    for step in range(steps):
        current_states = states
        states = set()
        for state in current_states:
            res = tuple([state[0][i] + state[1][i] for i in range(4)])
            bots = state[0]
            if state[0][0] <= cost[1]:
                states.add((state[0], res))  # build nothing
            if cost[0] <= state[1][0]:
                states.add(((bots[0] + 1, bots[1], bots[2], bots[3]), (res[0] - cost[0], res[1], res[2], res[3])))
            if cost[1] <= state[1][0]:
                states.add(((bots[0], bots[1] + 1, bots[2], bots[3]), (res[0] - cost[1], res[1], res[2], res[3])))
            if cost[2][0] <= state[1][0] and cost[2][1] <= state[1][1]:
                states.add(((bots[0], bots[1], bots[2] + 1, bots[3]), (res[0] - cost[2][0], res[1] - cost[2][1], res[2], res[3])))
            if cost[3][0] <= state[1][0] and cost[3][1] <= state[1][2]:
                states.add(((bots[0], bots[1], bots[2], bots[3] + 1), (res[0] - cost[3][0], res[1], res[2] - cost[3][1], res[3])))
        max_g = max(states, key=lambda s: s[1][3])[1][3]
        states = filter(lambda s: s[1][3] >= max_g - 2, states)
    return max(states, key=lambda s: s[1][3])[1][3]


def main():
    lines = read_input("day19.txt")
    blueprints = [(int(line[6]), int(line[12]), (int(line[18]), int(line[21])), (int(line[27]), int(line[30]))) for line in lines]
    results = [(i+1) * best_outcome(b, 24) for i, b in enumerate(blueprints)]
    print(sum(results))

    results = [best_outcome(b, 32) for b in blueprints[:3]]
    print(results, reduce(lambda x, y: x * y, results))


def read_input(file_name):
    with open(file_name, "r") as f:
        return [line.split(" ") for line in f.read().split("\n")]


if __name__ == "__main__":
    main()
