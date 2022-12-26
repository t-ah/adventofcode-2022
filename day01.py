def main():
    with open("day01.txt", "r") as f:
        blocks = f.read().split("\n\n")
        cals = [list(map(int, x.split("\n"))) for x  in blocks]

        print(max(map(sum, cals)))

        print(sum(sorted(map(sum, cals))[-3:]))


if __name__ == "__main__":
    main()