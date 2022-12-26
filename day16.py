from itertools import chain, combinations


class Valve:
    name: str
    rate: int
    tunnels: set[str]
    shortest_paths: dict[str, int]

    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.rate = rate
        self.tunnels = set()
        self.shortest_paths = dict()

    def calculate_paths(self, valves) -> None:
        new_nodes = set()
        new_nodes.add(self.name)
        path_length = 0
        while len(new_nodes) > 0:
            path_length += 1
            current_nodes = set(new_nodes)
            new_nodes = set()
            for node in current_nodes:
                for neighbour in valves[node].tunnels:
                    if neighbour not in self.shortest_paths:
                        self.shortest_paths[neighbour] = path_length
                        new_nodes.add(neighbour)


class State:
    def __init__(self, current: str, flow: int, remaining: int, opened: set) -> None:
        self.current = current
        self.flow = flow
        self.remaining = remaining
        self.opened = opened


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def best_flow(valves: dict, rel_valves: frozenset, steps: int, cache: dict):
    if rel_valves in cache:
        return cache[rel_valves]
    all_states: list[State] = []
    new_states = [State("AA", 0, steps, set())]
    while len(new_states) > 0:
        current_states = list(new_states)
        new_states = list()
        for state in current_states:
            valve = valves[state.current]
            for other_valve in rel_valves:
                if other_valve.name not in state.opened and valve.shortest_paths[other_valve.name] < state.remaining + 1:
                    remaining = state.remaining - (valve.shortest_paths[other_valve.name] + 1)
                    new_state = State(other_valve.name, state.flow + (remaining * other_valve.rate), remaining, opened=state.opened.union({other_valve.name}))
                    new_states.append(new_state)
                    all_states.append(new_state)
    max_flow = 0
    for state in all_states:
        max_flow = max(max_flow, state.flow)
    cache[rel_valves] = max_flow
    return max_flow


def main():
    valves = read_input("day16.txt")
    relevant_valves: set[Valve] = set(filter(lambda v: v.rate > 0, valves.values()))
    relevant_valves.add(valves["AA"])
    for valve in relevant_valves:
        valve.calculate_paths(valves)

    max_flow = 0
    cache = {}
    for valve_subset in powerset(relevant_valves):
        s = frozenset(valve_subset)
        s_comp = frozenset(relevant_valves.difference(s))
        if len(s) < 6 or len(s) > 9:
            continue
        max_flow = max(max_flow, best_flow(valves, s, 26, cache) + best_flow(valves, s_comp, 26, cache))
    print(max_flow)


def read_input(file_name):
    valves = {}
    with open(file_name, "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            words = line.split(" ")
            valve = Valve(name=words[1], rate=int(words[4][5:-1]))
            for i in range(9, len(words) - 1):
                valve.tunnels.add(words[i][:-1])
            valve.tunnels.add(words[-1])
            valves[valve.name] = valve
    return valves


if __name__ == "__main__":
    main()