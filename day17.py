class RingBuffer:
    def __init__(self, content: list) -> None:
        self.content = content
        self.l = len(content)
        self.index = 0
    
    def get_item(self):
        r = self.content[self.index]
        self.index = (self.index + 1) % self.l
        return r


class Grid:
    def __init__(self) -> None:
        self.maxY = -1
        self.taken = set([(x, -1) for x in range(7)])

    def horizontal_move_accepted(self, block):
        for p in block:
            if p[0] < 0 or p[0] > 6 or p in self.taken:
                return False
        return True

    def downward_move_accepted(self, block):
        for p in block:
            if p in self.taken:
                return False
        return True

    def place(self, block):
        l = list(block)
        self.taken.update(l)
        self.maxY = max(self.maxY, max(l, key=lambda b: b[1])[1])

    def get_front(self):
        new_cells = set()
        front = set()
        for x in range(7):
            if (x, self.maxY) not in self.taken:
                new_cells.add((x, self.maxY))
            else:
                front.add((x, self.maxY))
        explored = set()
        while len(new_cells) > 0:
            current_cells = new_cells
            new_cells = set()
            for cell in current_cells:
                for adj in ((1, 0),(-1, 0),(0, -1), (0, 1)):
                    test = (cell[0] + adj[0], cell[1] + adj[1])
                    if test[0] >= 0 and test[0] < 7 and test[1] >= 0 and test[1] < self.maxY and not test in explored:
                        explored.add(test)
                        if test in self.taken:
                            front.add(test)
                        else:
                            new_cells.add(test)
        return tuple(sorted([(p[0], p[1] - self.maxY) for p in front]))

    def add_block(self, jets: RingBuffer, blocks: RingBuffer) -> tuple:
        block = blocks.get_item()
        b_origin = [2, self.maxY + 4]
        while True:
            jet = jets.get_item()
            moved_block = list(map(lambda b: (b[0] + b_origin[0] + jet, b[1] + b_origin[1]), block))
            if self.horizontal_move_accepted(moved_block):
                b_origin[0] += jet
            moved_block = list(map(lambda b: (b[0] + b_origin[0], b[1] + b_origin[1] - 1), block))
            if self.downward_move_accepted(moved_block):
                b_origin[1] -= 1
            else:
                moved_block = list(map(lambda b: (b[0] + b_origin[0], b[1] + b_origin[1]), block))
                self.place(moved_block)
                return self.get_front()


def main():
    solve(2022)
    solve(1000000000000)


def solve(iterations: int):
    jets = RingBuffer(list(map(lambda j: -1 if j == "<" else 1, read_input("day17.txt"))))
    blocks = RingBuffer([((0, 0), (1, 0), (2, 0), (3, 0)), ((1,0), (0, 1), (1, 1), (2, 1), (1, 2)), ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)), ((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (0, 1), (1, 0), (1, 1))])
    grid = Grid()
    front_cache = dict()
    added_height = 0
    more_iterations = 0
    for i in range(iterations):
        front = grid.add_block(jets, blocks)
        if (front, blocks.index, jets.index) in front_cache:
            last_seen, last_maxY = front_cache[(front, blocks.index, jets.index)]
            loop_size = i - last_seen
            loop_height = grid.maxY - last_maxY
            remaining_iterations = iterations - (i + 1)
            loops = remaining_iterations // loop_size
            added_height = loops * loop_height
            more_iterations = remaining_iterations % loop_size
            break
        front_cache[(front, blocks.index, jets.index)] = (i, grid.maxY)
    for _ in range(more_iterations):
        grid.add_block(jets, blocks)
    print(grid.maxY + 1 + added_height)


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read()


if __name__ == "__main__":
    main()