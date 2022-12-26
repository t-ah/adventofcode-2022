# TODO: cleanup

class Face:
    def __init__(self, pos):
        self.pos = pos
        self.neighbours: dict[int, tuple["Face", int]] = dict()
        self.neighbour_directions: dict["Face", int] = dict()

    def add_neighbour(self, face: "Face", direction: int, turns: int):
        if direction in self.neighbours:
            return
        self.neighbours[direction] = (face, turns)
        self.neighbour_directions[face] = direction

    def get_dir_of_neighbour(self, face: "Face"):
        return self.neighbour_directions[face]


directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


def main():
    # part1, part2 = read_input("day22_test.txt")
    # face_len = 4
    part1, part2 = read_input("day22.txt")
    face_len = 50
    board = part1.split("\n")
    len_x = max([len(line) for line in board])
    len_y = len(board)
    board = [line.ljust(len_x, " ") for line in board]

    instructions = part2.replace("L", "#L#").replace("R", "#R#").split("#")

    row_indices = []
    for line in board:
        start = min(filter(lambda x: x != -1, [line.find("."), line.find("#")]))
        end = max(line.rfind("."), line.rfind("#"))
        row_indices.append((start, end))

    position = (board[0].index("."), 0)
    direction_i = 0

    for instruction in instructions:
        if instruction == "L":
            direction_i = (direction_i - 1) % 4
        elif instruction == "R":
            direction_i = (direction_i + 1) % 4
        else:
            distance = int(instruction)
            move = directions[direction_i]
            next_pos = position
            for _ in range(distance):
                potential_pos = moved(next_pos, move, len_x, len_y)
                while board[potential_pos[1]][potential_pos[0]] == " ":  # skip whitespace
                    potential_pos = moved(potential_pos, move, len_x, len_y)
                if board[potential_pos[1]][potential_pos[0]] == "#":
                    break
                else:
                    next_pos = potential_pos
            position = next_pos
    print((1000 * (position[1] + 1) + (4 * (position[0] + 1))) + direction_i)

    # Act II

    faces = dict()
    for x in range(0, len(board[0]), face_len):
        for y in range(0, len(board), face_len):
            if board[y][x] != " ":
                faces[(x, y)] = Face((x, y))
    assert(len(faces) == 6)

    for (x, y), f in faces.items():
        for di, d in enumerate(directions):
            new_pos = (x + (face_len * d[0]), y + (face_len * d[1]))
            if new_pos in faces:
                f.add_neighbour(faces[new_pos], di, 0)

    for _ in range(6):  # TODO test 4 and 5
        for face in faces.values():
            new_neighbours = []
            for direction_face_to_n1, (n1, turns1) in face.neighbours.items():
                side_mods = (-1, 1)
                for side_mod in side_mods:
                    relevant_side = (direction_face_to_n1 + side_mod + turns1) % 4
                    if relevant_side in n1.neighbours:
                        n2, turns2 = n1.neighbours[relevant_side]
                        new_n = (face, (n2, (direction_face_to_n1 + side_mod) % 4, (turns1 + turns2 - side_mod) % 4))
                        new_neighbours.append(new_n)
                        # face.add_neighbour(n2, (direction_face_to_n1 + side_mod) % 4, turns1 + turns2 + side_mod)
            for n in new_neighbours:
                n[0].add_neighbour(*n[1])

    for p, f in faces.items():
        print(p, [(i, other_f.pos, turns) for i, (other_f, turns) in f.neighbours.items()])
        assert(len(f.neighbours) == 4)

    position = (board[0].index("."), 0)
    direction_i = 0
    for instruction in instructions:
        if instruction == "L":
            direction_i = (direction_i - 1) % 4
        elif instruction == "R":
            direction_i = (direction_i + 1) % 4
        else:
            distance = int(instruction)
            next_pos = position
            next_dir_i = direction_i
            for _ in range(distance):
                move_dir = directions[next_dir_i]
                if leave_face(next_pos, move_dir, faces, face_len):
                    potential_dir_i, potential_pos = wrap(next_pos, next_dir_i, faces, face_len)
                else:
                    potential_dir_i = next_dir_i
                    potential_pos = moved(next_pos, move_dir, len_x, len_y)
                if board[potential_pos[1]][potential_pos[0]] == "#":
                    break
                else:
                    print(potential_dir_i, potential_pos)
                    next_pos = potential_pos
                    next_dir_i = potential_dir_i
            position, direction_i = next_pos, next_dir_i
    print((1000 * (position[1] + 1) + (4 * (position[0] + 1))) + direction_i)


def leave_face(pos, move_dir, faces, face_len):
    origin_x = pos[0] - (pos[0] % face_len)
    origin_y = pos[1] - (pos[1] % face_len)
    new_x, new_y = pos[0] + move_dir[0], pos[1] + move_dir[1]
    return new_x < origin_x or new_y < origin_y or new_x >= origin_x + face_len or new_y >= origin_y + face_len


def wrap(pos, move_dir_i, faces, face_len):
    move_dir = directions[move_dir_i]
    origin_x = pos[0] - (pos[0] % face_len)
    origin_y = pos[1] - (pos[1] % face_len)
    new_x, new_y = pos[0] + move_dir[0], pos[1] + move_dir[1]
    face = faces[(origin_x, origin_y)]
    next_face, turns = face.neighbours[move_dir_i]
    new_direction_i = (move_dir_i + turns) % 4
    if new_direction_i == 0:
        new_x = next_face.pos[0]
    elif new_direction_i == 2:
        new_x = next_face.pos[0] + face_len - 1
    elif new_direction_i == 1:
        new_y = next_face.pos[1]
    elif new_direction_i == 3:
        new_y = next_face.pos[1] + face_len - 1

    # (10, 3) -> (10, 4)
    # (11, 5) -> (14, 8)
    offset = (pos[0] % face_len) if move_dir_i in (1, 3) else (pos[1] % face_len)  # relevant offset depends on side where we left
    base = next_face.pos[1] if new_direction_i in (0, 2) else next_face.pos[0]
    print(base, offset)
    if turns == 0:
        base += offset
    elif turns == 2:
        base += face_len - 1 - offset
    elif turns == 1 and move_dir_i in (0, 2):
        base += face_len - 1 - offset
    elif turns == 3 and move_dir_i in (1, 3):
        base += face_len - 1 - offset
    else:
        base += offset

    # base += (face_len - 1 - offset) if turns in (1, 2) else offset
    if new_direction_i in (0, 2):
        new_y = base
    else:
        new_x = base

    # if new_direction_i in (0, 2):
    #     if turns == 3:
    #         new_y = next_face.pos[1] + (pos[0] % face_len)
    #     elif turns == 0:
    #         new_y = next_face.pos[1] + (pos[1] % face_len)
    #     elif turns == 1:
    #         new_y = next_face.pos[1] + face_len - 1 - (pos[0] % face_len)
    #     else:  # turns == 2
    #         new_y = next_face.pos[1] + face_len - 1 - (pos[1] % face_len)
    # else:
    #     if turns == 3:
    #         new_x = next_face.pos[0] + (pos[1] % face_len)
    #     elif turns == 0:
    #         new_x = next_face.pos[0] + (pos[0] % face_len)
    #     elif turns == 1:
    #         new_x = next_face.pos[0] + face_len - 1 - (pos[1] % face_len)
    #     else:  # turns == 2
    #         new_x = next_face.pos[0] + face_len - 1 - (pos[0] % face_len)

    print(">> wrapping to", new_direction_i, (new_x, new_y), f"turns={turns}, offset={offset}")
    return new_direction_i, (new_x, new_y)

        # for o in origins:
        #     for di in range(4):
        #         if (o, di) in neighbours:  # n1 to contact
        #             neighbour_o, turns = neighbours[(o, di)]
        #             my_direction = -1
        #             for my_di in range(4):
        #                 if (neighbour_o, my_di) not in neighbours:
        #                     continue
        #                 if neighbours[(neighbour_o, my_di)] == (o, _):
        #                     my_direction = my_di
        #             if my_direction == -1:
        #                 raise Exception("oh no")
        #
        #             for di2 in filter(lambda k: k != di, range(4)):
        #                 if (o, di2) in neighbours:  # n2 to tell n1 about
        #                     if my_direction == 0:
        #                         if di2 == 1:


def lookup_direction(face_dir, to_which_side):
    if (face_dir, to_which_side) in ((3, 2), (1, 0), (0, 3), (2, 1)):
        return 1
    else:
        return -1


# for d in directions:
    #     current = position
    #     while True:
    #         new_pos = (current[0] + (50*d[0])), current[1] + (50*d[1])
    #         if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= len_x or new_pos[1] >= len_y:
    #             break
    #         if board[new_pos[1]][new_pos[0]] != " ":
    #             neighbours[current, d] = (new_pos, 0)
    #         else:
    #             break

    # for instruction in instructions:
    #     if instruction == "L":
    #         direction_i = (direction_i - 1) % 4
    #     elif instruction == "R":
    #         direction_i = (direction_i + 1) % 4
    #     else:
    #         distance = int(instruction)
    #         move = directions[direction_i]
    #         next_pos = position
    #         for _ in range(distance):
    #             potential_pos = moved_cube(next_pos, move, len_x, len_y, row_indices)
    #             while board[potential_pos[1]][potential_pos[0]] == " ":  # skip whitespace
    #                 potential_pos = moved_cube(potential_pos, move, len_x, len_y, row_indices)
    #             if board[potential_pos[1]][potential_pos[0]] == "#":
    #                 break
    #             else:
    #                 next_pos = potential_pos
    #         position = next_pos
    # print((1000 * (position[1] + 1) + (4 * (position[0] + 1))) + direction_i)


def moved(pos, move, len_x, len_y) -> tuple:
    return (pos[0] + move[0]) % len_x, (pos[1] + move[1]) % len_y


# def moved_cube(pos, move, len_x, len_y, row_indices) -> tuple:
#     real_x = pos[0] - row_indices[pos[0]][0]
#     new_pos = (pos[0] + move[0]) % len_x, (pos[1] + move[1]) % len_y
#     if move[0] != 0:  # move in x
#         pass
#     else:  # move in y
#         pass


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n\n")


if __name__ == "__main__":
    main()
