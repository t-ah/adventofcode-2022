conv_map = {3: "=", 4: "-", 5: "0"}


def main():
    solve("day25_test.txt")
    solve("day25.txt")


def base_5(n):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % 5))
        n //= 5
    return digits[::-1]


def solve(file_name: str):
    lines = read_input(file_name)
    numbers = [convert(x) for x in lines]
    target = sum(numbers)
    print("I", target)

    converted = base_5(target)
    carry = 0
    for i in reversed(range(len(converted))):
        n = converted[i]
        n += carry
        carry = 0
        if n > 2:
            carry = 1
            converted[i] = conv_map[n]
        else:
            converted[i] = str(n)
    if carry == 1:
        converted = ["1"] + converted
    print("II", "".join(converted))


def convert(s):
    r = 0
    exp = len(s)
    for c in s:
        exp -= 1
        if c in ("1", "2"):
            r += int(c) * pow(5, exp)
        elif c == "-":
            r -= pow(5, exp)
        elif c == "=":
            r -= 2 * pow(5, exp)
    return r


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()
