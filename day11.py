class Monkey():
    def __init__(self, text):
        parts = text[1].split(" ")
        self.items = [8 * [int(x.replace(",", ""))] for x in parts[4:]]
        self.operation = text[2][19:]
        self.test = int(text[3][21:])
        self.throw_true = int(text[4][29])
        self.throw_false = int(text[5][30])
        self.inspection_count = 0


def main():
    with open("day11.txt", "r") as f:
        blocks = [b.split("\n") for b in f.read().split("\n\n")]
    simulate(blocks, 20, True)
    simulate(blocks, 10000, False)


def simulate(blocks: list, n: int, simple: bool):
    monkeys = {i: Monkey(b) for i, b in enumerate(blocks)}
    for _ in range(n):
        round(monkeys, simple)
    inspections = sorted([m.inspection_count for m in monkeys.values()])
    print(inspections[-1] * inspections[-2])


def round(monkeys: dict[int, Monkey], simple: bool):
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        monkey.inspection_count += len(monkey.items)
        items, monkey.items = monkey.items, []
        for item in items:
            new_item = [eval(monkey.operation,{"old": item[item_id]}) for item_id in range(8)]
            if simple:
                new_item = list(map(lambda x: x // 3, new_item))
            else:
                new_item = [new_item[item_id] % monkeys[item_id].test for item_id in range(8)]
            if new_item[i] % monkey.test == 0:
                monkeys[monkey.throw_true].items.append(new_item)
            else:
                monkeys[monkey.throw_false].items.append(new_item)


if __name__ == "__main__":
    main()