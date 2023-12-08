'''
Solution to Day 5, Part 2 of the 2023 Advent of Code calendar
'''

'''
If a map has multiple adjacent ranges that have the same modifying
value, this will combine them into a single larger range
'''
def consolidateMap(srcDstMap):
    rangesToAdd = {}
    keysToRemove = []
    for key in srcDstMap:
        for otherKey in srcDstMap:
            if key == otherKey:
                continue
            if key[1] == (otherKey[0]-1):
                if srcDstMap[key] == srcDstMap[otherKey]:
                    rangesToAdd[(key[0],otherKey[1])] = srcDstMap[key]
                    keysToRemove += [key]
                    keysToRemove += [otherKey]
    for key in keysToRemove:
        del srcDstMap[key]
    for key in rangesToAdd:
        srcDstMap[key] = rangesToAdd[key]
    return srcDstMap


'''
Parses the input strings into a dictionary that maps a range of
source values to the number that is added to them to generate the
destination value.
'''
def parseMap(stringMap):
    ans = {}
    for line in stringMap.split("\n"):
        (dest, source, rng) = map(int, line.split())
        ans[(source, source+rng-1)] = dest-source
    return consolidateMap(ans)


'''
When using the generated map, you look for a key whose range
encompasses the source and add the corresponding value for that
range to get the destination. If there is no key with a range
encompassing the source, then the destination is the same as the
source.
'''
def applyMap(source, srcDstMap):
    for key in srcDstMap.keys():
        if source >= key[0] and source <= key[1]:
            return source + srcDstMap[key]
    return source


'''
Compares two ranges, specified as ordered pairs of inclusive endpoints
with the lower endpoint as the first value of the pair

Returns an int corresponding to each possibility of endpoint order:
0 - rangeOne is entirely before rangeTwo
1 - rangeOne contains just the low endpoint of rangeTwo
2 - rangeOne contains the entirety of rangeTwo
3 - rangeOne is entirely contained within rangeTwo
4 - rangeOne contains just the high endpoint of rangeTwo
5 - rangeOne is entirely after rangeTwo
'''
def compareRanges(rangeOne, rangeTwo):
    if rangeOne[1] < rangeTwo[0]:
        return 0
    elif rangeOne[0] > rangeTwo[1]:
        return 5
    elif rangeOne[0] >= rangeTwo[0] and rangeOne[1] <= rangeTwo[1]:
        return 3
    elif rangeOne[0] <= rangeTwo[0] and rangeOne[1] >= rangeTwo[1]:
        return 2
    elif rangeOne[0] < rangeTwo[0]:
        return 1
    else:
        return 4


'''
takes a map that goes from a-b and a map from b-c and generates a
new map that goes directly from a-c
'''
def combineMaps(abMap, bcMap):
    acMap = {}
    bcKeysCovered = []
    bcPartialKeys = {}
    for abKey in abMap.keys():
        rangesToConsolidate = [(abKey[0]+abMap[abKey], abKey[1]+abMap[abKey])]
        while len(rangesToConsolidate) > 0:
            currRange = rangesToConsolidate.pop()
            foundOverlap = False
            for bcKey in bcMap.keys():
                if bcKey in bcKeysCovered:
                    # once we found overlap with a range we should be checking the remaining portion in bcPartialKeys
                    continue
                overlapType = compareRanges(currRange,bcKey)
                if overlapType == 0 or overlapType == 5:
                    # no overlap
                    continue
                elif overlapType == 2:
                    # currRange contains everything in bcKey
                    if currRange[0] != bcKey[0]:
                        rangesToConsolidate.append((currRange[0], bcKey[0]-1))
                    if currRange[1] != bcKey[1]:
                        rangesToConsolidate.append((bcKey[1]+1, currRange[1]))
                    acMap[(bcKey[0]-abMap[abKey], bcKey[1]-abMap[abKey])] = abMap[abKey] + bcMap[bcKey]
                    bcKeysCovered.append(bcKey)
                    foundOverlap = True
                    break
                elif overlapType == 3:
                    # currRange is contained entirely in bcKey
                    if currRange[0] != bcKey[0]:
                        bcPartialKeys[(bcKey[0], currRange[0]-1)] = bcMap[bcKey]
                    if currRange[1] != bcKey[1]:
                        bcPartialKeys[(currRange[1]+1, bcKey[1])] = bcMap[bcKey]
                    acMap[(currRange[0]-abMap[abKey], currRange[1]-abMap[abKey])] = abMap[abKey] + bcMap[bcKey]
                    bcKeysCovered.append(bcKey)
                    foundOverlap = True
                    break
                elif overlapType == 1:
                    # currRange contains the start of bcKey
                    rangesToConsolidate.append((currRange[0], bcKey[0] - 1))
                    bcPartialKeys[(currRange[1]+1, bcKey[1])] = bcMap[bcKey]
                    acMap[(bcKey[0]-abMap[abKey], currRange[1]-abMap[abKey])] = abMap[abKey] + bcMap[bcKey]
                    bcKeysCovered.append(bcKey)
                    foundOverlap = True
                    break
                elif overlapType == 4:
                    # currRange contains the end of bcKey
                    bcPartialKeys[(bcKey[0], currRange[0]-1)] = bcMap[bcKey]
                    rangesToConsolidate.append((bcKey[1]+1, currRange[1]))
                    acMap[(currRange[0]-abMap[abKey], bcKey[1]-abMap[abKey])] = abMap[abKey] + bcMap[bcKey]
                    bcKeysCovered.append(bcKey)
                    foundOverlap = True
                    break
            if foundOverlap:
                continue
            for parKey in bcPartialKeys.keys():
                overlapType = compareRanges(currRange,parKey)
                if overlapType == 0 or overlapType == 5:
                    # no overlap
                    continue
                elif overlapType == 2:
                    # currRange contains everything in parKey
                    if currRange[0] != parKey[0]:
                        rangesToConsolidate.append((currRange[0], parKey[0]-1))
                    if currRange[1] != parKey[1]:
                        rangesToConsolidate.append((parKey[1]+1, currRange[1]))
                    acMap[(parKey[0]-abMap[abKey], parKey[1]-abMap[abKey])] = abMap[abKey] + bcPartialKeys[parKey]
                    del bcPartialKeys[parKey]
                    foundOverlap = True
                    break
                elif overlapType == 3:
                    # currRange is contained entirely in parKey
                    if currRange[0] != parKey[0]:
                        bcPartialKeys[(parKey[0], currRange[0]-1)] = bcPartialKeys[parKey]
                    if currRange[1] != parKey[1]:
                        bcPartialKeys[(currRange[1]+1, parKey[1])] = bcPartialKeys[parKey]
                    acMap[(currRange[0]-abMap[abKey], currRange[1]-abMap[abKey])] = abMap[abKey] + bcPartialKeys[parKey]
                    del bcPartialKeys[parKey]
                    foundOverlap = True
                    break
                elif overlapType == 1:
                    # currRange contains the start of parKey
                    rangesToConsolidate.append((currRange[0], parKey[0] - 1))
                    bcPartialKeys[(currRange[1]+1, parKey[1])] = bcPartialKeys[parKey]
                    acMap[(parKey[0]-abMap[abKey], currRange[1]-abMap[abKey])] = abMap[abKey] + bcPartialKeys[parKey]
                    del bcPartialKeys[parKey]
                    foundOverlap = True
                    break
                elif overlapType == 4:
                    # currRange contains the end of parKey
                    bcPartialKeys[(parKey[0], currRange[0]-1)] = bcPartialKeys[parKey]
                    rangesToConsolidate.append((parKey[1]+1, currRange[1]))
                    acMap[(currRange[0]-abMap[abKey], parKey[1]-abMap[abKey])] = abMap[abKey] + bcPartialKeys[parKey]
                    del bcPartialKeys[parKey]
                    foundOverlap = True
                    break
            if not foundOverlap:
                # stick with default case
                acMap[(currRange[0]-abMap[abKey], currRange[1]-abMap[abKey])] = abMap[abKey]
    # map any bcRanges that weren't covered using the default case for abMap
    for key in bcMap.keys():
        if key in bcKeysCovered:
            continue
        acMap[key] = bcMap[key]
    # map any partial ranges using default case
    for key in bcPartialKeys.keys():
        acMap[key] = bcPartialKeys[key]
    return consolidateMap(acMap)


'''
This is the main function that reads the input and finds the lowest
location that corresponds to any of the initial seeds.
'''
def lowestLocation(almanac):
    # Parse the almanac into a list of seeds and a single map from seeds to locations
    (seeds, almanac) = almanac.split("\n\nseed-to-soil map:\n")
    seeds = list(map(int, seeds[7:].split()))
    (mapStr, almanac) = almanac.split("\n\nsoil-to-fertilizer map:\n")
    seedMap = parseMap(mapStr)
    (mapStr, almanac) = almanac.split("\n\nfertilizer-to-water map:\n")
    seedMap = combineMaps(seedMap,parseMap(mapStr))
    (mapStr, almanac) = almanac.split("\n\nwater-to-light map:\n")
    seedMap = combineMaps(seedMap,parseMap(mapStr))
    (mapStr, almanac) = almanac.split("\n\nlight-to-temperature map:\n")
    seedMap = combineMaps(seedMap,parseMap(mapStr))
    (mapStr, almanac) = almanac.split("\n\ntemperature-to-humidity map:\n")
    seedMap = combineMaps(seedMap,parseMap(mapStr))
    (mapStr, almanac) = almanac.split("\n\nhumidity-to-location map:\n")
    seedMap = combineMaps(seedMap,parseMap(mapStr))
    seedMap = combineMaps(seedMap,parseMap(almanac))

    # Generate the locations for each initial seed
    loc = []
    for seed in seeds:
        loc += [applyMap(seed, seedMap)]

    # Return the lowest location
    return min(loc)

almanac = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

print(lowestLocation(almanac))
