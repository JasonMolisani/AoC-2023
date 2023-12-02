def parseDraw(draw):
    red = 0
    green = 0
    blue = 0
    for colors in draw.split(","):
        (count, color) = colors.strip().split(" ")
        if color == "red":
            red += int(count)
        elif color == "green":
            green += int(count)
        elif color == "blue":
            blue += int(count)
    return (red, green, blue)

'''
Takes in a string in the following form:
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

returns the game number if all draws are less than the
maximum numbers, otherwise returns 0
'''
def validateGame(gameString, maxRed, maxGreen, maxBlue):
    (game, results) = gameString.split(":")
    game = int(game[5:])
    results = results.split(";")
    for draw in results:
        colors = parseDraw(draw)
        if colors[0] > maxRed:
            return 0
        elif colors[1] > maxGreen:
            return 0
        elif colors[2] > maxBlue:
            return 0
    return game
        

def sumValidGames(lines):
    validGameSum = 0
    for line in lines.split("\n"):
        validGameSum += validateGame(line, 12, 13, 14)
    return validGameSum

lines = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

print(sumValidGames(lines))
