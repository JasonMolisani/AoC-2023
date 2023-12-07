class Hand:
    def __init__(self, line):
        (self.hand, bid) = line.split()
        self.bid = int(bid)
        self.handType = self.determineHandType()

    def __str__(self):
        return self.hand

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        if self.handType > other.handType:
            return True
        if self.handType < other.handType:
            return False
        for i in range(len(self.hand)):
            if self.hand[i] == other.hand[i]:
                continue
            if self.hand[i] == 'A':
                return False
            if other.hand[i] == 'A':
                return True
            if self.hand[i] == 'K':
                return False
            if other.hand[i] == 'K':
                return True
            if self.hand[i] == 'Q':
                return False
            if other.hand[i] == 'Q':
                return True
            if self.hand[i] == 'J':
                return False
            if other.hand[i] == 'J':
                return True
            if self.hand[i] == 'T':
                return False
            if other.hand[i] == 'T':
                return True
            return int(self.hand[i]) < int(other.hand[i])

    def __le__(self, other):
        return self == other or self < other

    '''
    Returns a number corresponding to the type of hand this is:
    0 - 5 of a kind
    1 - 4 of a kind
    2 - Full House
    3 - 3 of a kind
    4 - 2 pair
    5 - 1 pair
    6 - high card
    '''
    def determineHandType(self):
        cardQuantities = {}
        for card in self.hand:
            cardQuantities[card] = cardQuantities.get(card, 0) + 1
        if len(cardQuantities.values()) == 1:
            return 0
        elif len(cardQuantities.values()) == 2:
            if 4 in cardQuantities.values():
                return 1
            else:
                return 2
        elif len(cardQuantities.values()) == 3:
            if 3 in cardQuantities.values():
                return 3
            else:
                return 4
        elif len(cardQuantities.values()) == 4:
            return 5
        else:
            return 6

    def printableHandType(self):
        if self.handType == 0:
            return "5 of a kind"
        elif self.handType == 1:
            return "4 of a kind"
        elif self.handType == 2:
            return "Full House"
        elif self.handType == 3:
            return "3 of a kind"
        elif self.handType == 4:
            return "2 pair"
        elif self.handType == 5:
            return "1 pair"
        else:
            return "High Card"

def calcWinnings(hands):
    handArr = []
    for line in hands.split("\n"):
        handArr.append(Hand(line))
    handArr.sort()
    winnings = 0
    rank = 1
    for hand in handArr:
        winnings += hand.bid*rank
        rank += 1
    return winnings
            
hands = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

print(calcWinnings(hands))
