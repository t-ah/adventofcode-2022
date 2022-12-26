def main():
    with open("day02.txt", "r") as f:
        lines = f.readlines()
        scores = [get_score(l) for l in lines]
        print(sum(scores))

        scores = [get_real_score(l) for l in lines]
        print(sum(scores))


def get_score(line: str) -> int:
    moveA = ord(line[0]) - 65
    moveB = ord(line[2]) - 88

    if moveA == moveB: # draw
        return moveB + 4
    elif moveB == (moveA + 1) % 3: # you win
        return moveB + 7
    else: # you lose
        return moveB + 1


def get_real_score(line: str) -> int:
    moveA = ord(line[0]) - 65
    result = ord(line[2]) - 88
    moveB = (moveA + result + 2) % 3
    return 1 + moveB + (result * 3)


if __name__ == "__main__":
    main()