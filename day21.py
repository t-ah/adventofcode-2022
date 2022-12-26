import sympy  # check day21_v2 for a more "DIY" approach


def solve(name, instr, cache, build_cache: bool):
    if name in cache:
        return cache[name]
    formula = instr[name].split(" ")
    if len(formula) == 1:
        r = int(formula[0])
    elif formula[1] == "+":
        r = solve(formula[0], instr, cache, build_cache) + solve(formula[2], instr, cache, build_cache)
    elif formula[1] == "-":
        r = solve(formula[0], instr, cache, build_cache) - solve(formula[2], instr, cache, build_cache)
    elif formula[1] == "*":
        r = solve(formula[0], instr, cache, build_cache) * solve(formula[2], instr, cache, build_cache)
    elif formula[1] == "/":
        r = solve(formula[0], instr, cache, build_cache) / solve(formula[2], instr, cache, build_cache)
    else:
        raise Exception("Unknown operator")
    if build_cache and not requires(name, "humn", instr):
        cache[name] = r
    return r


def requires(name: str, requirement: str, instr):
    formula = instr[name].split(" ")
    if len(formula) == 1:
        return False
    if formula[0] == requirement or formula[2] == requirement:
        return True
    return requires(formula[0], requirement, instr) or requires(formula[2], requirement, instr)


def main():
    instr = {line[:4]: line[6:] for line in read_input("day21.txt")}
    cache = {}
    print(int(solve("root", instr, cache, True)))

    parts = instr["root"].split(" ")
    eq = (parts[0], parts[2])
    if requires(eq[0], "humn", instr):
        eq = (eq[1], eq[0])  # make sure eq[0] is the fixed value
    target = solve(eq[0], instr, cache, False)
    eq = "Eq(" + str(int(target)) + "," + build_formula(eq[1], instr) + ")"
    print(sympy.solve(eq))


# this feels like cheating
def build_formula(name, instr) -> str:
    if name == "humn":
        return "x"
    formula = instr[name].split(" ")
    if len(formula) == 1:
        return formula[0]
    else:
        return "(" + build_formula(formula[0], instr) + formula[1] + build_formula(formula[2], instr) + ")"


# this is a bad one of course
def bad_bf(name, target, instr, cache):
    test = 0
    while True:
        cache["humn"] = test
        test_target = solve(name, instr, cache, False)
        if target == test_target:
            print(test)
            break
        cache["humn"] = -test
        test_target = solve(name, instr, cache, False)
        if target == test_target:
            print(-test)
            break
        test += 1


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    main()
