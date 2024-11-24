from cmu_graphics import *
import random
import copy

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.number = num
        self.color = 'red' if self.suit == 'heart' or self.suit == 'diamond' else 'black'

def onAppStart(app):
    app.width = 1500
    app.height = 750
    app.sidebarWidth = app.width/6
    app.headerHeight = app.height/5
    app.cardHeight = 150
    app.verticalCardSpacing = 20
    makeFullDeck(app) # makes app.fullDeck in a set of tuples
    app.sideDeck = copy.deepcopy(app.fullDeck)
    makeGraphicsDict(app)
    app.numPiles = 4
    # makeInitialPiles(app)
    app.piles = [[('heart', 13)], [('spade', 4), ('heart', 3)], [('diamond', 13), ('diamond', 1), ('diamond', 3)], [('diamond', 12), ('clover', 12), ('heart', 6), ('spade', 1)]]
    app.doneSlots = [('spade',0),('heart',0),('clover',0),('diamond',0)] # use 0 cuz 1 is next after that

def redrawAll(app):
    drawSideBar(app)
    drawSideDeck(app)
    drawPiles(app)

def onKeyPress(app, key):
    if key == 1:
        isMoveValid(app, 0)
    elif key == 2:
        isMoveValid(app, 1)
    elif key == 4:
        isMoveValid(app, 2)
    elif key == 5:
        isMoveValid(app, 3)
    elif key == 3:
        pass
        # flipDeck(app)
    elif key == 6:
        isMoveValid(app, 'sideDeck')
    elif key == 'r':
        pass
        # reset(app)


def makeFullDeck(app): # making a list of all the cards in a deck of normal playing cards, each card represented as a tuple.
    suits = ['clover', 'spade', 'heart', 'diamond']
    numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    app.fullDeck = []
    for suit in suits:
        for number in numbers:
            app.fullDeck.append((suit,number))

def makeInitialPiles(app): # setting up the piles of a new game
    app.piles = []
    for _ in range(app.numPiles):
        app.piles.append([])
    for i in range(len(app.piles)): # i is the pile we are on (ex. pile 1, pile 2, etc.)
        numCardsInPile = i+1
        for _ in range(numCardsInPile):
            lenDeckLeft = len(app.sideDeck)
            randomCardIndex = random.randint(0,lenDeckLeft-1) #from 0 to the length of what cards are left-1: random int inclusive (there are 52 cards at first)
            app.piles[i].append(app.sideDeck[randomCardIndex])
            app.sideDeck.pop(randomCardIndex) # taking the card placed in the pile out of the sideDeck (so cannot be randomly chosen again)

def drawSideBar(app):
    sidebarX = app.width - app.sidebarWidth
    drawLine(sidebarX, 0, sidebarX, app.height)

def drawSideDeck(app):
    backGraphicURL = app.cardGraphics['back']
    sideDeckX = app.width - app.sidebarWidth/2
    drawImage(backGraphicURL, sideDeckX, app.headerHeight, 
              width=app.cardBackWidth, height=app.cardHeight, align='center')

def drawPiles(app):
    spaceForPiles = app.width - app.sidebarWidth
    spaceBetweenPiles = spaceForPiles/(app.numPiles+1)
    for pile in range(len(app.piles)):
        for card in range(len(app.piles[pile])):
            if card == len(app.piles[pile])-1: # if the card is the last one
                #draw card
                cardGraphicURL = app.cardGraphics[app.piles[pile][card]]
            else:
                #draw back card
                cardGraphicURL = app.cardGraphics[('back')]
            cardX = spaceBetweenPiles*(pile+1)
            cardY = app.headerHeight + app.verticalCardSpacing*card
            drawImage(cardGraphicURL, cardX, cardY, 
                      width=app.cardWidth, height=app.cardHeight, align='center')

def isMoveValid(app, pileFrom): # pileFrom is the index into app.piles or 'sideDeck'
    if pileFrom == 'sideDeck':
        print('change from sideDeck to copy of that that we are updating as we flip')
        cardToMove = app.sideDeck.pop()
    else:
        cardToMove = app.piles[pileFrom][-1]
    cardToMoveSuit = cardToMove[0]
    cardToMoveColor = getCardColor(app, cardToMove)
    cardToMoveNum = cardToMove[1]
    for slot in range(len(app.doneSlots)):
        currSlotSuit = app.doneSlots[slot][0]
        currSlotNum = app.doneSlots[slot][1]
        if currSlotSuit == cardToMoveSuit:
            if currSlotNum+1 == cardToMoveNum:
                print('success')
                # makeMove(app)

    for pile in range(app.numPiles):
        if pile == pileFrom:
            continue
        openCardinPile = app.piles[pile][-1]
        openCardinPileColor = getCardColor(openCardinPile)
        openCardinPileNum = openCardinPile[1]
        if cardToMoveColor == openCardinPileColor: # needs to be alternating colors
            return False
        elif not cardToMoveNum -1 == openCardinPileNum:
            return False
        else:
            print('success')
            # makeMove(app)
            return True

def getCardColor(card):
    suit = card[0]
    return 'red' if suit == 'heart' or suit == 'diamond' else 'black'


def makeGraphicsDict(app): #storing all the graphics info and calculating the card sizes
    cardBackGraphicWidth, cardBackGraphicHeight = getImageSize('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Card_back_01.svg/312px-Card_back_01.svg.png?20071017165047')
    cardGraphicWidth, cardGraphicHeight = getImageSize('https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/English_pattern_2_of_clubs.svg/800px-English_pattern_2_of_clubs.svg.png')
    cardSizeFactor = app.cardHeight/cardGraphicHeight # this is the multiplication factor from the actual wanted height to the height of the OG graphic
    cardBackSizeFactor = app.cardHeight/cardBackGraphicHeight # this is the multiplication factor from the actual wanted height to the height of the OG graphic
    app.cardWidth = cardSizeFactor * cardGraphicWidth
    app.cardBackWidth = cardBackSizeFactor * cardBackGraphicWidth
    app.cardGraphics = {('back'): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Card_back_01.svg/312px-Card_back_01.svg.png?20071017165047', 
                        ('clover', 2): 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/English_pattern_2_of_clubs.svg/800px-English_pattern_2_of_clubs.svg.png',
                        ('clover', 3): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_3_of_clubs.svg/800px-English_pattern_3_of_clubs.svg.png', 
                        ('clover', 4): 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/English_pattern_4_of_clubs.svg/800px-English_pattern_4_of_clubs.svg.png', 
                        ('clover', 5): 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/English_pattern_5_of_clubs.svg/800px-English_pattern_5_of_clubs.svg.png', 
                        ('clover', 6): 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/English_pattern_6_of_clubs.svg/800px-English_pattern_6_of_clubs.svg.png', 
                        ('clover', 7): 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/English_pattern_7_of_clubs.svg/800px-English_pattern_7_of_clubs.svg.png', 
                        ('clover', 8): 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/English_pattern_8_of_clubs.svg/800px-English_pattern_8_of_clubs.svg.png', 
                        ('clover', 9): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_9_of_clubs.svg/800px-English_pattern_9_of_clubs.svg.png', 
                        ('clover', 10): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/English_pattern_10_of_clubs.svg/800px-English_pattern_10_of_clubs.svg.png', 
                        ('clover', 11): 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/English_pattern_jack_of_clubs.svg/800px-English_pattern_jack_of_clubs.svg.png', 
                        ('clover', 12): 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/English_pattern_queen_of_clubs.svg/800px-English_pattern_queen_of_clubs.svg.png', 
                        ('clover', 13): 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/English_pattern_king_of_clubs.svg/800px-English_pattern_king_of_clubs.svg.png', 
                        ('spade', 1): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/English_pattern_ace_of_spades.svg/800px-English_pattern_ace_of_spades.svg.png', 
                        ('spade', 2): 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/English_pattern_2_of_spades.svg/800px-English_pattern_2_of_spades.svg.png', 
                        ('spade', 3): 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/English_pattern_3_of_spades.svg/800px-English_pattern_3_of_spades.svg.png', 
                        ('spade', 4): 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/English_pattern_4_of_spades.svg/800px-English_pattern_4_of_spades.svg.png', 
                        ('spade', 5): 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/English_pattern_5_of_spades.svg/800px-English_pattern_5_of_spades.svg.png', 
                        ('spade', 6): 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/English_pattern_6_of_spades.svg/800px-English_pattern_6_of_spades.svg.png', 
                        ('spade', 7): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/English_pattern_7_of_spades.svg/800px-English_pattern_7_of_spades.svg.png', 
                        ('spade', 8): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/English_pattern_8_of_spades.svg/800px-English_pattern_8_of_spades.svg.png', 
                        ('spade', 9): 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/English_pattern_9_of_spades.svg/800px-English_pattern_9_of_spades.svg.png', 
                        ('spade', 10): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_10_of_spades.svg/800px-English_pattern_10_of_spades.svg.png', 
                        ('spade', 11): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_jack_of_spades.svg/800px-English_pattern_jack_of_spades.svg.png', 
                        ('spade', 12): 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/English_pattern_queen_of_spades.svg/800px-English_pattern_queen_of_spades.svg.png', 
                        ('spade', 13): 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/English_pattern_king_of_spades.svg/800px-English_pattern_king_of_spades.svg.png', 
                        ('heart', 1): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/English_pattern_ace_of_hearts.svg/800px-English_pattern_ace_of_hearts.svg.png', 
                        ('heart', 2): 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/English_pattern_2_of_hearts.svg/800px-English_pattern_2_of_hearts.svg.png', 
                        ('heart', 3): 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/English_pattern_3_of_hearts.svg/800px-English_pattern_3_of_hearts.svg.png', 
                        ('heart', 4): 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/English_pattern_4_of_hearts.svg/800px-English_pattern_4_of_hearts.svg.png', 
                        ('heart', 5): 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/English_pattern_5_of_hearts.svg/800px-English_pattern_5_of_hearts.svg.png', 
                        ('heart', 6): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_6_of_hearts.svg/800px-English_pattern_6_of_hearts.svg.png', 
                        ('heart', 7): 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/English_pattern_7_of_hearts.svg/800px-English_pattern_7_of_hearts.svg.png', 
                        ('heart', 8): 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/English_pattern_8_of_hearts.svg/800px-English_pattern_8_of_hearts.svg.png', 
                        ('heart', 9): 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/English_pattern_9_of_hearts.svg/800px-English_pattern_9_of_hearts.svg.png', 
                        ('heart', 10): 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/English_pattern_10_of_hearts.svg/800px-English_pattern_10_of_hearts.svg.png', 
                        ('heart', 11): 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/English_pattern_jack_of_hearts.svg/800px-English_pattern_jack_of_hearts.svg.png', 
                        ('heart', 12): 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/English_pattern_queen_of_hearts.svg/800px-English_pattern_queen_of_hearts.svg.png', 
                        ('heart', 13): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_king_of_hearts.svg/800px-English_pattern_king_of_hearts.svg.png', 
                        ('diamond', 1): 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/800px-English_pattern_ace_of_diamonds.svg.png', 
                        ('diamond', 2): 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/English_pattern_2_of_diamonds.svg/800px-English_pattern_2_of_diamonds.svg.png', 
                        ('diamond', 3): 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/English_pattern_3_of_diamonds.svg/800px-English_pattern_3_of_diamonds.svg.png', 
                        ('diamond', 4): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/English_pattern_4_of_diamonds.svg/800px-English_pattern_4_of_diamonds.svg.png', 
                        ('diamond', 5): 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/English_pattern_5_of_diamonds.svg/800px-English_pattern_5_of_diamonds.svg.png', 
                        ('diamond', 6): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/English_pattern_6_of_diamonds.svg/800px-English_pattern_6_of_diamonds.svg.png', 
                        ('diamond', 7): 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/English_pattern_7_of_diamonds.svg/800px-English_pattern_7_of_diamonds.svg.png', 
                        ('diamond', 8): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/English_pattern_8_of_diamonds.svg/800px-English_pattern_8_of_diamonds.svg.png', 
                        ('diamond', 9): 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/English_pattern_9_of_diamonds.svg/800px-English_pattern_9_of_diamonds.svg.png', 
                        ('diamond', 10): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_10_of_diamonds.svg/800px-English_pattern_10_of_diamonds.svg.png', 
                        ('diamond', 11): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/English_pattern_jack_of_diamonds.svg/800px-English_pattern_jack_of_diamonds.svg.png', 
                        ('diamond', 12): 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_queen_of_diamonds.svg/800px-English_pattern_queen_of_diamonds.svg.png', 
                        ('diamond', 13): 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/English_pattern_king_of_diamonds.svg/800px-English_pattern_king_of_diamonds.svg.png'}

runApp()
