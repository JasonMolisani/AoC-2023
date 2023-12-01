def calibrationSum(lines):
    sum = 0
    for line in lines.split("\n"):
        sum += int(firstDigit(line)+lastDigit(line))
    return sum

def firstDigit(characterString):
    for i in range(0,len(characterString)):
        if characterString[i].isdigit():
            return characterString[i]
    return ""

def lastDigit(characterString):
    for i in range(len(characterString)-1,-1,-1):
        if characterString[i].isdigit():
            return characterString[i]
    return ""

lines = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

print(calibrationSum(lines))
