def findCombProd(boatInfo):
    (time, dist) = boatInfo.split("\n")
    time = list(map(int, time[9:].strip().split()))
    dist = list(map(int, dist[9:].strip().split()))
    prod = 1
    for i in range(len(time)):
        waysToWin = 0
        for t in range(1, time[i]):
            if dist[i] < t*(time[i]-t):
                waysToWin += 1
        prod *= waysToWin
    return prod

def findWaysToWinOneRace(boatInfo):
    (time, dist) = boatInfo.split("\n")
    temp = ""
    for numStr in time[9:].strip().split():
        temp += numStr
    time = int(temp)
    temp = ""
    for numStr in dist[9:].strip().split():
        temp += numStr
    dist = int(temp)
    minPress = 0
    maxPress = time
    for t in range(1, time):
        if dist < t*(time-t):
            minPress = t
            break
    for t in range(time, 0, -1):
        if dist < t*(time-t):
            maxPress = t
            break
    return maxPress - minPress + 1

boatInfo = """Time:        40     70     98     79
Distance:   215   1051   2147   1005"""

print(findWaysToWinOneRace(boatInfo))
