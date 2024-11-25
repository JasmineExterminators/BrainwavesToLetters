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
    app.sideDeckFlipped = []
    makeGraphicsDict(app)
    app.numPiles = 4
    app.piles = None
    # while app.piles == None or isInitialPilesSolvable(app) == 'False':
    #     makeInitialPiles(app)
    app.piles = [[('heart', 13)], [('spade', 4), ('spade', 12)], [('diamond', 13), ('diamond', 1), ('diamond', 3)], [('diamond', 12), ('clover', 12), ('heart', 6), ('spade', 1)]]
    app.doneSlots = [('spade',0),('heart',0),('clover',0),('diamond',0)] # use 0 cuz 1 is next after that
    app.sideCard = 'None'
    app.sideBarVerticalCardSpacing = 200
    app.pilesVisibility = [1 for _ in range(app.numPiles)] # this indicates how many cards in the pile are visible
    app.isMovingAnimation = False
    app.currentlyMovingDetails = ()
    app.currentlyMovingAniLocation = (None, None)
    app.stepsPerSecond = 10
    app.isWrongMoveAnimation = False
    app.cardAngleShake = 5

def game_redrawAll(app):
    drawSideBar(app)
    drawSideDeck(app)
    drawPiles(app)
    drawSideCard(app)
    drawDoneSlots(app)
    if app.isMovingAnimation:
        drawAnimateCardSlide(app)
    if app.isWrongMoveAnimation:
        drawAnimateWrongShake(app)

def game_onKeyPress(app, key):
    if key == '1':
        isMoveValid(app, 0)
        if not isMoveValid(app, 0):
            app.wrongMoveAnimation = True
    elif key == '2':
        isMoveValid(app, 1)
    elif key == '4':
        isMoveValid(app, 2)
    elif key == '5':
        isMoveValid(app, 3)
    elif key == '3':
        flipDeck(app)
    elif key == '6':
        isMoveValid(app, 'sideCard')
    elif key == 'r':
        pass
        # reset(app)
    if winCondition(app): # is this the right place to put this???
        setActiveScreen('endWin')

def game_onStep(app):
    if app.isMovingAnimation:
        xMoveRateSign = app.currentlyMovingDetails[1]
        yMoveRate = app.currentlyMovingDetails[2]
        endLocation = app.currentlyMovingDetails[4]
        app.currentlyMovingAniLocation[0] += xMoveRateSign
        app.currentlyMovingAniLocation[1] += yMoveRate
        if xMoveRateSign < 0: # moving right to left
            if app.currentlyMovingAniLocation[0] <= endLocation[0]:
                app.isMovingAnimation = False 

    elif app.isWrongMoveAnimation:
        app.cardAngleShake *= -1

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
        numCardsVisible = app.pilesVisibility[pile]
        for card in range(len(app.piles[pile])):
            if card < len(app.piles[pile])-numCardsVisible: # if the card is not supposed to be visible (one of the first ones)
                #draw back card
                cardGraphicURL = app.cardGraphics[('back')]
            else:
                #draw card
                cardGraphicURL = app.cardGraphics[app.piles[pile][card]]
        
            cardX = spaceBetweenPiles*(pile+1)
            cardY = app.headerHeight + app.verticalCardSpacing*card

            if card == len(app.piles[pile])-1 and app.isWrongMoveAnimation:
                drawAnimateWrongShake(app, app.piles[pile][card], cardX, cardY)
            
            drawImage(cardGraphicURL, cardX, cardY, 
                      width=app.cardWidth, height=app.cardHeight, align='center')

def flipDeck(app):
    cardFlipped = app.sideDeck.pop()
    app.sideCard = cardFlipped
    app.sideDeckFlipped.append(cardFlipped)

def isMoveValid(app, pileFrom): # pileFrom is the index into app.piles or 'sideDeck'
    if pileFrom == 'sideCard':
        if app.sideCard == 'None':
            print('Cannot do! No sidecard flipped!')
            return False
        else:
            cardToMove = app.sideCard
    else:
        cardToMove = app.piles[pileFrom][-1]
    cardToMoveSuit = cardToMove[0]
    cardToMoveColor = getCardColor(cardToMove)
    cardToMoveNum = cardToMove[1]
    for slot in range(len(app.doneSlots)):
        currSlotSuit = app.doneSlots[slot][0]
        currSlotNum = app.doneSlots[slot][1]
        if currSlotSuit == cardToMoveSuit:
            if currSlotNum+1 == cardToMoveNum:
                makeMove(app, pileFrom, 'slot', slot)

    for pile in range(app.numPiles):
        if pile == pileFrom:
            continue
        lastCardinPile = app.piles[pile][-1]
        lastCardinPileColor = getCardColor(lastCardinPile)
        lastCardinPileNum = lastCardinPile[1]
        if cardToMoveColor == lastCardinPileColor: # needs to be alternating colors
            print('failed cuz not right color')
            return False
        elif not cardToMoveNum +1 == lastCardinPileNum:
            print('failed cuz not right num', cardToMoveNum, lastCardinPileNum)
            return False
        else:
            makeMove(app, pileFrom, 'pile', pile)
            print('success move')
            return True

def getCardColor(card):
    suit = card[0]
    return 'red' if suit == 'heart' or suit == 'diamond' else 'black'

def makeMove(app, pileFrom, toSlotOrPile, movedTo):
    # these are to help calculate the card locations
    spaceForPiles = app.width - app.sidebarWidth
    spaceBetweenPiles = spaceForPiles/(app.numPiles+1)
    
    if pileFrom == 'sideCard':
        cardMoving = app.sideDeckFlipped.pop()
        flipDeck(app)
        # below is all to get the fromLocation
        fromLocationX = app.width - app.sidebarWidth/2
        fromLocationY = app.headerHeight + app.sideBarVerticalCardSpacing
        fromLocation = (fromLocationX, fromLocationY)
    else:
        cardMoving = app.piles[pileFrom].pop()
        # below is all to get the fromLocation
        fromLocationX = spaceBetweenPiles*(pileFrom+1)
        numCardsInPile = len(app.piles[pileFrom])+1 # +1 cuz we popped the last one already
        fromLocationY = app.headerHeight + app.verticalCardSpacing*(numCardsInPile-1) # -1 cuz the first card is 0*spacing
        fromLocation = (fromLocationX, fromLocationY)
    
    if toSlotOrPile == 'slot':
        app.doneSlots[movedTo] = cardMoving
        # below is all to get the toLocation
        spaceForSlots = app.width - app.sidebarWidth
        spaceBetweenSlots = spaceForSlots/(len(app.doneSlots)+1)
        toLocationX = spaceBetweenSlots*(movedTo+1)
        toLocationY = app.height - app.cardHeight
        toLocation = (toLocationX, toLocationY)
    elif toSlotOrPile == 'pile':
        app.piles[movedTo].append(cardMoving)
        app.pilesVisibility[movedTo] += 1
        # below is all to get the toLocation
        toLocationX = spaceBetweenPiles*(movedTo+1) # +1 because the first one should be one space into the screen already (not at the very edge)
        numCardsInPile = len(app.piles[movedTo])
        toLocationY = app.headerHeight + app.verticalCardSpacing*(numCardsInPile-1)
        toLocation = (toLocationX, toLocationY)
    
    app.isMovingAnimation = True
    movedVertically = toLocationY - fromLocationY
    movedHorizontally = toLocationX - fromLocationX
    if movedVertically < 0:
        yMoveRateSign = -1
    else:
        yMoveRateSign = 1
    yMoveRate = abs(movedVertically / movedHorizontally)*yMoveRateSign # this is the rate of y in comparison to 1 move of x
    if movedHorizontally < 0:
        xMoveRateSign = -1
    else:
        xMoveRateSign = 1
    app.currentlyMovingDetails = (cardMoving, xMoveRateSign, yMoveRate, fromLocation, toLocation)
    app.currentlyMovingAniLocation = list(fromLocation) # need to turn into list so that it's mutable

def drawSideCard(app):
    if app.sideCard != 'None':
        cardGraphicURL = app.cardGraphics[app.sideCard]
        sideCardX = app.width - app.sidebarWidth/2
        drawImage(cardGraphicURL, sideCardX, app.headerHeight + app.sideBarVerticalCardSpacing, 
                  width=app.cardWidth, height=app.cardHeight, align='center')

def drawDoneSlots(app):
    spaceForSlots = app.width - app.sidebarWidth
    spaceBetweenSlots = spaceForSlots/(len(app.doneSlots)+1)
    for slot in range(len(app.doneSlots)):
        card = app.doneSlots[slot]
        doneSlotX = spaceBetweenSlots*(slot+1)
        cardGraphicURL = app.cardGraphics[card]
        drawImage(cardGraphicURL, doneSlotX, app.height - app.cardHeight,
                  width=app.cardWidth, height=app.cardHeight, align='center')

def winCondition(app):
    for slot in range(len(app.doneSlots)):
        if len(app.doneSlots[slot]) != 13:
            return False
    return True

# def isInitialPilesSolvable(app):

def drawAnimateCardSlide(app):
    cardMoving = app.currentlyMovingDetails[0]
    cardGraphicURL = app.cardGraphics[cardMoving]
    drawImage(cardGraphicURL, app.currentlyMovingAniLocation[0], app.currentlyMovingAniLocation[1], 
              width=app.cardWidth, height=app.cardHeight, align='center')

def drawAnimateWrongShake(app, card, cardX, cardY):
    cardGraphicURL = app.cardGraphics[card]
    drawImage(cardGraphicURL, cardX, cardY, 
              width=app.cardWidth, height=app.cardHeight, align='center', rotateAngle=app.cardAngleShake)


def makeGraphicsDict(app): #storing all the graphics info and calculating the card sizes
    cardBackGraphicWidth, cardBackGraphicHeight = getImageSize('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Card_back_01.svg/312px-Card_back_01.svg.png?20071017165047')
    cardGraphicWidth, cardGraphicHeight = getImageSize('https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/English_pattern_2_of_clubs.svg/800px-English_pattern_2_of_clubs.svg.png')
    cardSizeFactor = app.cardHeight/cardGraphicHeight # this is the multiplication factor from the actual wanted height to the height of the OG graphic
    cardBackSizeFactor = app.cardHeight/cardBackGraphicHeight # this is the multiplication factor from the actual wanted height to the height of the OG graphic
    app.cardWidth = cardSizeFactor * cardGraphicWidth
    app.cardBackWidth = cardBackSizeFactor * cardBackGraphicWidth
    # Card Graphics Source: https://en.wikipedia.org/wiki/Standard_52-card_deck
    # Card Back Graphics Source: https://commons.wikimedia.org/wiki/File:Card_back_01.svg
    # Card Outline Graphic Source: 
    app.cardGraphics = {('back'): 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Card_back_01.svg/312px-Card_back_01.svg.png?20071017165047', 
                        ('clover', 0): 'https://www.clker.com/cliparts/5/9/8/1/13959626591670826938Playing%20Card%20Template.svg.med.png',
                        ('spade', 0): 'https://www.clker.com/cliparts/5/9/8/1/13959626591670826938Playing%20Card%20Template.svg.med.png',
                        ('diamond', 0): 'https://www.clker.com/cliparts/5/9/8/1/13959626591670826938Playing%20Card%20Template.svg.med.png',
                        ('heart', 0): 'https://www.clker.com/cliparts/5/9/8/1/13959626591670826938Playing%20Card%20Template.svg.med.png',
                        ('clover', 1): 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/English_pattern_ace_of_clubs.svg/800px-English_pattern_ace_of_clubs.svg.png',
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

def endWin_redrawAll(app):
    drawLabel('You WON!', 200, 200)

runAppWithScreens(initialScreen='game')