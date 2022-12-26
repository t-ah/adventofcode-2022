def solve(name, instr, blocked: set):
    for item in instr[name]:
        formula = item.split(" ")
        if len(formula) == 1:
            return int(float(formula[0]))
        if formula[0] in blocked or formula[1] in blocked:
            continue
        blocked.update({formula[0], formula[2]})
        if formula[1] == "+":
            r = solve(formula[0], instr, blocked) + solve(formula[2], instr, blocked)
        elif formula[1] == "-":
            r = solve(formula[0], instr, blocked) - solve(formula[2], instr, blocked)
        elif formula[1] == "*":
            r = solve(formula[0], instr, blocked) * solve(formula[2], instr, blocked)
        elif formula[1] == "/":
            r = solve(formula[0], instr, blocked) / solve(formula[2], instr, blocked)
        else:
            raise Exception("Unknown operator")
        return r
    raise Exception("No applicable formula.")


def requires(name: str, requirement: str, instr):
    formula = instr[name][0].split(" ")
    if len(formula) == 1:
        return False
    if formula[0] == requirement or formula[2] == requirement:
        return True
    return requires(formula[0], requirement, instr) or requires(formula[2], requirement, instr)


def main():
    instr = {line[:4]: [line[6:]] for line in read_input("day21.txt")}
    for key in list(instr.keys()):
        formula = instr[key][0].split(" ")
        if len(formula) == 3:
            if formula[1] == "+":
                instr[formula[0]].append(f"{key} - {formula[2]}")
                instr[formula[2]].append(f"{key} - {formula[0]}")
            elif formula[1] == "-":
                instr[formula[0]].append(f"{key} + {formula[2]}")
                instr[formula[2]].append(f"{formula[0]} - {key}")
            elif formula[1] == "*":
                instr[formula[0]].append(f"{key} / {formula[2]}")
                instr[formula[2]].append(f"{key} / {formula[0]}")
            elif formula[1] == "/":
                instr[formula[0]].append(f"{key} * {formula[2]}")
                instr[formula[2]].append(f"{formula[0]} / {key}")
    instr["humn"] = instr["humn"][1:]  # ignore the number
    # get the one part of the eq.
    parts = instr["root"][0].split(" ")
    eq = (parts[0], parts[2])
    if requires(eq[0], "humn", instr):
        eq = (eq[1], eq[0])  # make sure eq[0] is the fixed value
    target = solve(eq[0], instr, set())  # the val we need to match
    instr[eq[1]] = [str(target)]  # it's the val for the other name
    print(int(solve("humn", instr, {"humn"})))  # magic?


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()
