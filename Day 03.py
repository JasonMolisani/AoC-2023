def isPart(schemArr, partRow, partColStart, partColEnd):
    minR = max(0, partRow-1)
    maxR = min(len(schemArr)-1, partRow+1)
    minC = max(0, partColStart-1)
    maxC = min(len(schemArr[0])-1, partColEnd+1)
    r = minR
    while r <= maxR:
        c = minC
        while c <= maxC:
            if not schemArr[r][c].isdigit() and not schemArr[r][c] == ".":
                return True
            c += 1
        r += 1
    return False

def sumParts(schematic):
    schemArr = schematic.split("\n")
    ans = 0
    maxRow = len(schemArr)
    maxCol = len(schemArr[0])
    for r in range(maxRow):
        c = 0
        partNum = ""
        while c < maxCol:
            if schemArr[r][c].isdigit():
                partNum += schemArr[r][c]
            elif not partNum == "":
                if isPart(schemArr, r, c-len(partNum), c-1):
                    ans += int(partNum)
                partNum = ""
            c += 1
        # process part numbers that continue to the end of the row
        if not partNum == "":
            if isPart(schemArr, r, c-len(partNum), c-1):
                ans += int(partNum)
            partNum = ""
    return ans

schematic = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

print(sumParts(schematic))
