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

boatInfo = """Time:        40     70     98     79
Distance:   215   1051   2147   1005"""

print(findCombProd(boatInfo))
