def findMinSteps(lines):
    # Grab the directions and identify the minimum period before the directions start looping
    (RL, lines) = lines.split("\n\n")
    nodes = {}
    for line in lines.split("\n"):
        (name, pair) = line.split(" = (")
        (r, l) = pair[:-1].split(", ")
        nodes[name] = (r, l)
    currNode = "AAA"
    stepsTaken = 0
    while not currNode == "ZZZ":
        nextDir = RL[stepsTaken % len(RL)] == "R"
        currNode = nodes[currNode][nextDir]
        stepsTaken += 1
    return stepsTaken


puzzleInput = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

print(findMinSteps(puzzleInput))
