def main():
    with open("day10.txt", "r") as f:
        lines = f.read().split("\n")
    x = [1]
    for line in lines:
        x.append(x[-1])
        if line != "noop":
            x.append(x[-1] + int(line.split(" ")[1]))
    
    print(sum(x[i - 1] * i for i in (20, 60, 100, 140, 180, 220)))
    
    rows = []
    for row in range(6):
        rows.append([])
        for col in range(40):
            rows[-1].append("#" if x[row * 40 + col] in (col - 1, col, col + 1) else ".")
    for row in rows:
        print("".join(row))


if __name__ == "__main__":
    main()