def main():
    solve("dayDAY-NR_test.txt")
    solve("dayDAY-NR.txt")


def solve(file_name: str):
    lines = read_input(file_name)
    # TODO


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()
