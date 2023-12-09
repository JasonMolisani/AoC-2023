def sumExtrapolatedValues(lines):
    sum = 0
    for line in lines.split("\n"):
        sum += extrapolateNextValue(*list(map(int, line.split())))
    return sum


def extrapolateNextValue(*nums):
    if all(num == 0 for num in nums):
        return 0
    prevNum = None
    differences = []
    for num in nums:
        if prevNum is None:
            prevNum = num
            continue
        differences.append(num-prevNum)
        prevNum = num
    return prevNum + extrapolateNextValue(*differences)


puzzleInput = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

print(sumExtrapolatedValues(puzzleInput))
