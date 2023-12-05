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
    return ans

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
This is the main function that reads the input and finds the lowest
location that corresponds to any of the initial seeds.
'''
def lowestLocation(almanac):
    # Split the almanac into the relevant sections
    (seeds, almanac) = almanac.split("\n\nseed-to-soil map:\n")
    (seedSoilMap, almanac) = almanac.split("\n\nsoil-to-fertilizer map:\n")
    (soilFertMap, almanac) = almanac.split("\n\nfertilizer-to-water map:\n")
    (fertWaterMap, almanac) = almanac.split("\n\nwater-to-light map:\n")
    (waterLightMap, almanac) = almanac.split("\n\nlight-to-temperature map:\n")
    (lightTempMap, almanac) = almanac.split("\n\ntemperature-to-humidity map:\n")
    (tempHumMap, humLocMap) = almanac.split("\n\nhumidity-to-location map:\n")

    # Convert the sections into usable lists and dictionaries
    seeds = list(map(int, seeds[7:].split()))
    seedSoilMap = parseMap(seedSoilMap)
    soilFertMap = parseMap(soilFertMap)
    fertWaterMap = parseMap(fertWaterMap)
    waterLightMap = parseMap(waterLightMap)
    lightTempMap = parseMap(lightTempMap)
    tempHumMap = parseMap(tempHumMap)
    humLocMap = parseMap(humLocMap)

    # Generate the locations for each initial seed
    loc = []
    for seed in seeds:
        temp = applyMap(seed, seedSoilMap)
        temp = applyMap(temp, soilFertMap)
        temp = applyMap(temp, fertWaterMap)
        temp = applyMap(temp, waterLightMap)
        temp = applyMap(temp, lightTempMap)
        temp = applyMap(temp, tempHumMap)
        temp = applyMap(temp, humLocMap)
        loc += [temp]

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
