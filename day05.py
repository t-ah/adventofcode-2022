from collections import deque

def main():
    stacks, instructions = read_input()
    for instruction in instructions:
        move(stacks, instruction)
    print("".join([stack[0] for stack in stacks]))

    stacks, instructions = read_input()
    for instruction in instructions:
        move_multiple(stacks, instruction)
    print("".join([stack[0] for stack in stacks]))


def read_input():
    with open("day05.txt", "r") as f:
        parts = f.read().split("\n\n")
        stacks = [deque() for _ in range(9)]
        for line in parts[0].split("\n")[:-1]:
            for stack_i in range(9):
                line_i = 1 + (4 * stack_i)
                if line[line_i] != " ":
                    stacks[stack_i].append(line[line_i])
    return stacks, parts[1].split("\n")


def move(stacks: list, instruction: str):
    instr_parts = instruction.split(" ")
    qty, src, target = int(instr_parts[1]), int(instr_parts[3]) - 1, int(instr_parts[5]) - 1
    for _ in range(qty):
        stacks[target].appendleft(stacks[src].popleft())


def move_multiple(stacks: list, instruction: str):
    instr_parts = instruction.split(" ")
    qty, src, target = int(instr_parts[1]), int(instr_parts[3]) - 1, int(instr_parts[5]) - 1
    temp = deque()
    for _ in range(qty):
        temp.appendleft(stacks[src].popleft())
    stacks[target].extendleft(temp)


if __name__ == "__main__":
    main()