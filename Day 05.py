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
    seedRanges = []
    for i in range(0, len(seeds), 2):
        seedRanges.append((seeds[i],seeds[i]+seeds[i+1]-1))
    loc = []
    for seedRange in seedRanges:
        checkedRangeMin = False
        for key in seedMap.keys():
            overlapType = compareRanges(seedRange, key)
            if overlapType == 0 or overlapType == 5:
                # no overlap
                continue
            elif overlapType == 2 or overlapType == 1:
                # seedRange contains everything in key or
                # seedRange contains the start of key
                loc.append(applyMap(key[0], seedMap))
            elif overlapType == 3 or overlapType == 4:
                # seedRange is contained entirely in key or
                # seedRange contains the end of key
                checkedRangeMin = True
                loc.append(applyMap(seedRange[0], seedMap))
        if not checkedRangeMin:
            # Even if not covered in the overlap, we need to
            # check the start of a seedRange in case the default
            # mapping is the lowest location
            loc.append(applyMap(seedRange[0], seedMap))

    # Return the lowest location
    return min(loc)

almanac = """seeds: 3037945983 743948277 2623786093 391282324 195281306 62641412 769611781 377903357 2392990228 144218002 1179463071 45174621 2129467491 226193957 1994898626 92402726 1555863421 340215202 426882817 207194644

seed-to-soil map:
3078006360 2182201339 30483272
803630304 624445326 165226844
2393736333 2745251526 281120946
717936870 789672170 85693434
598717319 410599330 27984688
3999095007 2024628810 157572529
3605588191 3026372472 22322803
3555659576 2678166775 3396919
968857148 438584018 1780307
3216227818 2212684611 87459567
2302084376 4122083708 91651957
970637455 0 188112122
507182228 299146916 40412346
1372302034 1689624457 202945009
1370123632 191483770 2178402
324787204 193662172 105484744
3116425470 2671328191 6838584
626702007 875365604 82756204
1575247043 978774853 317322423
3134996187 4213735665 81231631
2024628810 2681563694 63687832
714565222 188112122 3371648
547594574 1620884480 51122745
3529388087 3374604163 26271489
709458211 973428243 5107011
2713008276 3985570976 98361735
2088316642 3048695275 213767734
3627910994 2300144178 371184013
2674857279 4083932711 38150997
1229789645 958121808 15306435
4156667536 3328662676 45941487
0 1296097276 324787204
3108489632 3320726838 7935838
4202609023 3667512001 92358273
1352266801 978535254 239599
1352506400 1672007225 17617232
1245096080 440364325 107170721
2811370011 3400875652 266636349
430271948 547535046 76910280
1158749577 339559262 71040068
3559056495 3262463009 46531696
3123264054 3308994705 11732133
3303687385 3759870274 225700702

soil-to-fertilizer map:
2937874770 2957653952 339980892
1886469734 2145122669 192293654
3277855662 822424488 19779182
2622882196 2393077006 314992574
3449876679 3769116301 525850995
583550735 842203670 1302918999
2145755543 345297835 477126653
2078763388 2890661797 66992155
2650514 2708069580 182592217
0 2337416323 2650514
530540566 2340066837 53010169
185242731 0 345297835
3975727674 3449876679 319239622

fertilizer-to-water map:
861477134 5168332 68211907
136969509 2229711837 29094441
2823248929 1150509810 118368045
3678888284 3073610919 53498438
3948051821 3682691325 96234592
1302827191 2387840795 504257794
1198743248 1926818347 104083943
1807084985 1104177008 46332802
2143096098 619653304 259805223
2063436946 2385211148 2629647
2066066593 445026117 35759449
358008423 537865723 81787581
621204445 0 5168332
2724438904 1861632296 65186051
1853417787 2258806278 126404870
3933311080 4141091197 14740741
851739278 2892098589 9737856
4044286413 3029323079 44287840
1979822657 1778018007 83614289
2101826042 2084781230 3070511
4088574253 4268409625 26557671
929689041 111346117 211974050
3566310597 4155831938 112577687
439796004 2030902290 53878940
166063950 1490707297 191944473
8760514 888219041 128208995
3794695843 3778925917 57203243
3029323079 3127109357 409045756
2792635116 77722143 30613813
3438368835 4013149435 127941762
3732386722 3620382204 62309121
2402901321 1682651770 95366237
0 879458527 8760514
493674944 2901836445 39780529
3851899086 3536155113 81411994
2498267558 1268877855 221829442
4117947021 3836129160 177020275
2789624955 108335956 3010161
1141663091 480785566 57080157
2104896553 406826572 38199545
533455473 1016428036 87748972
626372777 2087851741 141860096
2720097000 73380239 4341904
4115131924 3617567107 2815097
768232873 323320167 83506405

water-to-light map:
3846882465 367033980 98093832
1878565977 3292746518 62917983
4255729420 661438934 39237876
469590509 2191298319 301681796
381948234 1999013894 87642275
3688496086 199351627 156562666
1300818753 2086656169 104642150
806539912 2798447654 224466318
1265336919 355914293 11119687
1405460903 1914042148 28882526
2577391070 1942924674 56089220
3680239306 4136990116 8256780
1941483960 700676810 607954854
3845058752 3022913972 1823713
4239658038 1308631664 16071382
2566162195 4254580741 11228875
1671792383 3831845903 10462472
3944976297 3842308375 294681741
3290662499 3160062910 132683608
2549438814 1324703046 16723381
3423346107 1341426427 27108304
1031006230 3355664501 234330689
1276456606 4145246896 24362147
3450454411 54538430 144813197
1682254855 465127812 196311122
54538430 1403802338 272790856
2633480290 2492980115 305467539
3595267608 4169609043 84971698
3242064105 3644614138 48598394
3077581200 4265809616 29157680
771272305 1368534731 35267607
1434343429 1676593194 237448954
327329286 3589995190 54618948
3106738880 3024737685 135325225
2938947829 3693212532 138633371

light-to-temperature map:
2777813298 2971073270 586210802
1687968665 0 334152507
4159107034 3882460035 135860262
0 2095520416 192800212
3640671099 3557284072 3145370
2455782705 3560429442 322030593
2022121172 1272848785 266199456
773517036 914869331 357979454
1131496490 1539048241 556472175
3364024100 4018320297 60669366
3643816469 2455782705 515290565
192800212 334152507 580716824
3424693466 4078989663 215977633

temperature-to-humidity map:
4072523312 605654847 17750681
1174610018 540191835 65463012
2038455907 3792024734 100202248
2539396783 866566556 128459181
96342672 2296045868 14715058
3827330744 1522255720 106701221
3816190028 4081148893 11140716
1706101724 3892226982 188921911
3780839952 623405528 35350076
765616949 1813669629 408993069
4225769488 3778728770 13295964
2752105545 1645897858 167771771
2138658155 1121517092 400738628
4239065452 4155853973 55901844
3934031965 96342672 35726394
3005272654 658755604 22724553
3989311833 4211755817 83211479
280430452 3186777866 320785315
111057730 2310760926 65268270
176326000 3659551759 104104452
1895023635 1628956941 16940917
4093334384 3507563181 132435104
3027997207 132069066 179421352
1477400307 311490418 228701417
2934949875 2225723089 70322779
601215767 681480157 100836818
2919877316 3763656211 15072559
3969758359 3639998285 19553474
3207418559 2613356473 573421393
4090273993 2222662698 3060391
1911964552 995025737 126491355
2667855964 782316975 84249581
1240073030 2376029196 237327277
702052585 4092289609 63564364

humidity-to-location map:
2848734682 2982177676 22285660
3380476660 3717224958 24199873
3201930685 734568132 100088122
764851360 4087339561 71173655
188169313 2953711255 28466421
3189375901 2832231336 12554784
3369909102 47909639 10567558
47909639 3741424831 99762378
2871020342 58477197 7400020
3042878026 3409715295 146497875
1196348942 2734551883 97679453
3418711171 3387790447 21924848
1587973141 573552831 65833150
1121006696 889063447 75342246
1294028395 567796360 5756471
3302018807 499906065 67890295
2915035031 2921050411 32660844
1982422286 3064299481 301982155
704786709 4084864539 2475022
299076626 834656254 54407193
3623423724 2182055199 207702290
388851709 2881400789 39649622
147672017 3592293988 40497296
2947695875 639385981 95182151
707261731 3556213170 36080818
2284404441 2389757489 138657919
353483819 2146687309 35367890
2519626540 441189704 58319568
743342549 3366281636 21508811
2878420362 2844786120 36614669
216635734 4212526404 82440892
3440636019 1235194267 182787705
2577946108 964405693 270788574
1453221956 3877915244 70435137
836025015 1861705628 284981681
1299784866 499509272 396793
1859942766 3948350381 122479520
2423062360 3004463336 59836145
3404676533 4070829901 14034638
1399208768 4158513216 54013188
1300181659 342162595 99027109
1523657093 3652908910 64316048
3851243640 1417981972 443723656
3831126014 3632791284 20117626
1653806291 2528415408 206136475
428501331 65877217 276285378
2482898505 3841187209 36728035"""

print(lowestLocation(almanac))
