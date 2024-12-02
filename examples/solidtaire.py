from cmu_graphics import *
import random
import copy
from PIL import Image
import os
import sys

# Increase recursion limit
sys.setrecursionlimit(10000)

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.number = num
        self.color = 'red' if self.suit == 'heart' or self.suit == 'diamond' else 'black'

def onAppStart(app):
    app.width = 1500
    app.height = 750
    app.sidebarWidth = app.width/6
    app.headerHeight = app.height/7
    app.cardHeight = 150
    app.verticalCardSpacing = 20
    makeFullDeck(app) # makes app.fullDeck in a set of tuples
    app.sideDeck = copy.deepcopy(app.fullDeck)
    app.sideDeckFlipped = []
    makeGraphicsDict(app)
    app.numPiles = 4
    app.piles = []
    
    # this is the test piles:
    app.piles = [[('heart', 1)], [('spade', 4), ('spade', 13)], [('diamond', 13), ('diamond', 1), ('diamond', 12)], [('diamond', 12), ('clover', 12), ('clover', 6), ('spade', 11)]]
    app.doneSlots = [('spade',0),('heart',0),('clover',0),('diamond',0)] # use 0 cuz 1 is next after that
    app.sideCard = 'None'
    app.sideBarVerticalCardSpacing = 200
    app.pilesVisibility = [1 for _ in range(app.numPiles)] # this indicates how many cards in the pile are visible
    app.isMovingAnimation = False
    app.currentlyMovingDetails = ()
    app.currentlyMovingAniLocation = (None, None)
    app.stepsPerSecond = 500
    app.isWrongMoveAnimation = False
    app.cardAngleShake = 5
    app.cardSlideRate = 20
    app.errorCount = 0
    app.isHintMode = False
    app.highlightStartLocation = 0
    app.highlightEndLocation = 0
    # button stuff
    app.buttonHeight = app.headerHeight - 50
    app.buttonWidth = app.width / 15
    app.numButtonCols = 3 # not changeable easily
    app.numButtonRows = 2 # not changeable easily
    app.buttonSpacingOffEdgeX = app.buttonWidth/2 + 50 # need to do this cuz the align of the buttons are center
    app.buttonSpacingOffEdgeY = app.headerHeight/2 # align of the buttons are center so center the button in the header
    app.buttonLabels = [['pile 1', 'pile2', 'flip deck'], ['pile 3', 'pile4', 'side card']]
    app.selectedButtonAnimation = None
    app.selectedButtonAniPadding = 10
    app.percentageTongue = 0
    # not button stuff anymore
    while app.piles == [] or isInitialPilesSolvable(app) == False:
        makeInitialPiles(app)

def game_redrawAll(app):
    drawSideBar(app)
    drawSideDeck(app)
    drawPiles(app)
    drawSideCard(app)
    drawDoneSlots(app)
    drawButtons(app)
    drawLabel(app.errorCount, 200, 200)
    if app.isMovingAnimation:
        drawAnimateCardSlide(app)
    if app.isWrongMoveAnimation:
        drawAnimateWrongShake(app)
    if app.isHintMode:
        drawHint(app)
    
def game_onKeyPress(app, key):
    if key == '1' or key == '2' or key == '4' or key == '5' or key == '6':
        if key == '1':
            pileFrom = 0
        elif key == '2':
            pileFrom = 1
        elif key == '4':
            pileFrom = 2
        elif key == '5':
            pileFrom = 3
        elif key == '6':
            pileFrom = 'sideCard'


        if isMoveValid(app, pileFrom) != None:
            print('moveValid')
            toSlotOrPile, movedTo = isMoveValid(app, pileFrom)
            makeMove(app, pileFrom, toSlotOrPile, movedTo)
        else:
            print('notvalid')
            app.wrongMoveAnimation = True
        
    elif key == '3':
        flipDeck(app)
    elif key == 'r':
        pass
        # reset(app)
    elif key == 'h':
        app.isHintMode = not app.isHintMode

    if app.isHintMode: # checks on every key press 
        findPossibleMovesHint(app)
        
    if winCondition(app): # is this the right place to put this???
        setActiveScreen('endWin')

def game_onStep(app):
    if app.isMovingAnimation:
        xMoveRateSign = app.currentlyMovingDetails[1]
        yMoveRate = app.currentlyMovingDetails[2]
        endLocation = app.currentlyMovingDetails[4]
        app.currentlyMovingAniLocation[0] += xMoveRateSign*app.cardSlideRate
        app.currentlyMovingAniLocation[1] += yMoveRate*app.cardSlideRate
        if xMoveRateSign < 0: # moving right to left
            if app.currentlyMovingAniLocation[0] <= endLocation[0]:
                app.isMovingAnimation = False 
        else: # moving left to right
            if app.currentlyMovingAniLocation[0] >= endLocation[0]:
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
    print(app.piles)
    app.piles = []
    print(app.piles)
    for _ in range(app.numPiles):
        app.piles.append([])
    for i in range(len(app.piles)): # i is the pile we are on (ex. pile 1, pile 2, etc.)
        numCardsInPile = i+1
        for _ in range(numCardsInPile):
            lenDeckLeft = len(app.sideDeck)
            randomCardIndex = random.randint(0,lenDeckLeft-1) #from 0 to the length of what cards are left-1: random int inclusive (there are 52 cards at first)
            app.piles[i].append(app.sideDeck[randomCardIndex])
            app.sideDeck.pop(randomCardIndex) # taking the card placed in the pile out of the sideDeck (so cannot be randomly chosen again)
            random.shuffle(app.sideDeck) # shuffles the sideDeck once initially

def drawButtons(app):
    for row in range(app.numButtonRows):
        for col in range(app.numButtonCols):
            buttonX, buttonY = getButtonXY(app, row, col)
            drawRect(buttonX, buttonY, app.buttonWidth, app.buttonHeight,
                          align = 'center', fill = None, border = 'black')
            drawLabel(app.buttonLabels[row][col], buttonX, buttonY, align = 'center')

def getButtonXY(app, row, col):
    # finding buttonY
    if row == 0:
        buttonY = app.buttonSpacingOffEdgeY
    elif row == 1:
        buttonY = app.height - app.buttonSpacingOffEdgeY
    # finding buttonX
    if col == 0:
        buttonX = app.buttonSpacingOffEdgeX
    elif col == 1:
        buttonX = app.width/2
    elif col == 2:
        buttonX = app.width - app.buttonSpacingOffEdgeX
    
    return buttonX, buttonY

def drawSideBar(app):
    sidebarX = app.width - app.sidebarWidth
    drawLine(sidebarX, 0, sidebarX, app.height)

def drawSideDeck(app):
    img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[('back')]))
    backGraphicURL = CMUImage(img)
    sideDeckX = app.width - app.sidebarWidth/2
    if app.sideDeck != []:
        drawImage(backGraphicURL, sideDeckX, app.headerHeight + app.cardHeight/2, 
                  width=app.cardBackWidth, height=app.cardHeight, align='center')

def drawPiles(app):
    spaceForPiles = app.width - app.sidebarWidth
    spaceBetweenPiles = spaceForPiles/(app.numPiles+1)
    for pile in range(len(app.piles)):
        
        numCardsVisible = app.pilesVisibility[pile]
        cardX = spaceBetweenPiles*(pile+1)
        
        if app.piles[pile] == []: # if the pile is empty, draw an empty card
            img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics['empty']))
            cardGraphicURL = CMUImage(img)
            drawImage(cardGraphicURL, cardX, app.headerHeight + app.cardHeight/2, 
                        width=app.cardWidth, height=app.cardHeight, align='center')
            continue
        
        for card in range(len(app.piles[pile])):
            if card < len(app.piles[pile])-numCardsVisible: # if the card is not supposed to be visible (one of the first ones)
                #draw back card
                img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[('back')]))
                cardGraphicURL = CMUImage(img)
            else:
                #draw card
                img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[app.piles[pile][card]]))
                cardGraphicURL = CMUImage(img)
                # cardGraphicURL = app.cardGraphics[app.piles[pile][card]]
        
            cardY = app.headerHeight + app.verticalCardSpacing*card

            if card == len(app.piles[pile])-1 and app.isWrongMoveAnimation:
                drawAnimateWrongShake(app, app.piles[pile][card], cardX, cardY)
            
            # we are skipping drawing the card if it was just moved to new location and the sliding animation is not yet done
            if app.isMovingAnimation and app.currentlyMovingDetails[0] == app.piles[pile][card]:
                continue
            
            drawImage(cardGraphicURL, cardX, cardY + app.cardHeight/2, 
                      width=app.cardWidth, height=app.cardHeight, align='center')

def flipDeck(app):
    if app.sideDeck == []:
        print('ok')
        random.shuffle(app.sideDeckFlipped)
        app.sideDeck = copy.deepcopy(app.sideDeckFlipped)
        app.sideDeckFlipped = []
    cardFlipped = app.sideDeck.pop()
    app.sideCard = cardFlipped
    app.sideDeckFlipped.append(cardFlipped)

def isMoveValid(app, pileFrom): # pileFrom is the index into app.piles or 'sideDeck'
    if pileFrom == 'sideCard':
        if app.sideCard == 'None':
            print('Cannot do! No sidecard flipped!')
            app.errorCount += 1
            return None
        else:
            cardToMove = app.sideCard
    elif app.piles[pileFrom] == []: # this is if the pile is empty
        app.errorCount += 1
        return None
    else:
        numCardsOpenInPile = app.pilesVisibility[pileFrom] #this is the card # (counting from the back) that should be checked (the first visible card in the pile)
        print('numCardsOpen', numCardsOpenInPile, "pileFrom", pileFrom)
        cardToMove = app.piles[pileFrom][-1*numCardsOpenInPile]
        print('cardToMove', cardToMove)
    cardToMoveSuit = cardToMove[0]
    cardToMoveColor = getCardColor(cardToMove)
    cardToMoveNum = cardToMove[1]
    
    for slot in range(len(app.doneSlots)):
        print('inslotloop')
        currSlotSuit = app.doneSlots[slot][0]
        currSlotNum = app.doneSlots[slot][1]
        if currSlotSuit == cardToMoveSuit:
            print(currSlotSuit, cardToMove)
            if currSlotNum+1 == cardToMoveNum:
                print('successful')
                return 'slot', slot
            print('not success', currSlotNum+1, cardToMoveNum)

    for pile in range(app.numPiles):
        if pile == pileFrom:
            print('skipping over', pile)
            continue
        if app.piles[pile] == []: 
            if cardToMoveNum == 13: # if the pile is empty, king can go in it
                return 'pile', pile
            else: # skip over any piles that are empty
                continue 
        lastCardinPile = app.piles[pile][-1]
        lastCardinPileColor = getCardColor(lastCardinPile)
        lastCardinPileNum = lastCardinPile[1]
        if cardToMoveColor != lastCardinPileColor and cardToMoveNum +1 == lastCardinPileNum:
            print('I did it!')
            return 'pile', pile
        if cardToMoveColor == lastCardinPileColor:
            print('failed due to color, pile', pile)
        elif cardToMoveNum +1 != lastCardinPileNum:
            print('failed due to num, cardToMoveNum', cardToMoveNum, 'lastCardinPileNum', lastCardinPileNum, 'pile', pile)
    print('outtaloop!')
    app.errorCount += 1
    return None

def getCardColor(card):
    suit = card[0]
    return 'red' if suit == 'heart' or suit == 'diamond' else 'black'

def getCardLocation(app, slotOrPile, stackIndex, cardIndexFromLow): #cardIndex is the index of card in a pile from low to high
    # these are to help calculate the card locations
    spaceForPiles = app.width - app.sidebarWidth
    spaceBetweenPiles = spaceForPiles/(app.numPiles+1)

    if stackIndex == 'sideCard':
        # below is all to get the location
        locationX = app.width - app.sidebarWidth/2
        locationY = app.headerHeight + app.sideBarVerticalCardSpacing + app.cardHeight/2
        location = (locationX, locationY)

    elif slotOrPile == 'slot':
        # below is all to get the location
        spaceForSlots = app.width - app.sidebarWidth
        spaceBetweenSlots = spaceForSlots/(len(app.doneSlots)+1)
        locationX = spaceBetweenSlots*(stackIndex+1)
        locationY = app.height - app.headerHeight - app.cardHeight/2
        location = (locationX, locationY)
    elif slotOrPile == 'pile':
        # below is all to get the location
        locationX = spaceBetweenPiles*(stackIndex+1) # +1 because the first one should be one space into the screen already (not at the very edge)
        numCardsInPile = len(app.piles[stackIndex])
        locationY = app.headerHeight + app.verticalCardSpacing*(numCardsInPile-1-cardIndexFromLow) + app.cardHeight/2 # -1 cuz the first card is 0*spacing
        location = (locationX, locationY)
    return location
    
def makeMove(app, pileFrom, toSlotOrPile, movedTo):
    if isinstance(pileFrom, int):
        numMovingCards = app.pilesVisibility[pileFrom]
        if len(app.piles[pileFrom]) - numMovingCards == 0:
            app.pilesVisibility[pileFrom] = 0
        else:
            app.pilesVisibility[pileFrom] = 1
    else:
        numMovingCards = 1
    # fromLocationList = []
    # toLocationList = []
    

    if pileFrom == 'sideCard':
            cardsMoving = app.sideDeckFlipped.pop()
            flipDeck(app)
    else:
        # do the location getting before popping so that we have the right number of cards in pile (pre-pop)
        cardsMoving = app.piles[pileFrom][-numMovingCards:] # chatGPT gave me the idea to use slicing instead of pop
        app.piles[pileFrom] = app.piles[pileFrom][:-numMovingCards-1]
        print('cardsMoving', cardsMoving)
    
    if toSlotOrPile == 'slot':
        app.doneSlots[movedTo] = cardsMoving[0] # just index 0 cuz we know only one card can move into the slot
    elif toSlotOrPile == 'pile':
        app.piles[movedTo].extend(cardsMoving)
        app.pilesVisibility[movedTo] += numMovingCards

    for cardBackIndex in range(numMovingCards-1, 0, -1): # cardBackIndex is the index from back to front of the card being moved
        print('THIS IS THE CARDBACK INDEX', cardBackIndex)
        if toSlotOrPile != 'slot':
            cardMoving = cardsMoving[cardBackIndex]
        fromLocation = getCardLocation(app, 'pile', pileFrom, cardBackIndex) # it's always going to come from a pile cannot come from a slot
        fromLocationX = fromLocation[0]
        fromLocationY = fromLocation[1]
        # fromLocationList.append(fromLocation)

        
        
        toLocation = getCardLocation(app, toSlotOrPile, movedTo, 0)
        toLocationX = toLocation[0]
        toLocationY = toLocation[1]
        # toLocationList.append(toLocation)
        
        app.isMovingAnimation = True
        movedVertically = toLocationY - fromLocationY
        movedHorizontally = toLocationX - fromLocationX
        if movedVertically < 0:
            yMoveRateSign = -1
        else:
            yMoveRateSign = 1
        
        # the if, else is to prevent from division by 0
        if movedHorizontally == 0:
            yMoveRate = yMoveRateSign
        else:
            yMoveRate = abs(movedVertically / movedHorizontally)*yMoveRateSign # this is the rate of y in comparison to 1 move of x
        
        if movedHorizontally < 0:
            xMoveRateSign = -1
        else:
            xMoveRateSign = 1
        app.currentlyMovingDetails = (cardMoving, xMoveRateSign, yMoveRate, fromLocation, toLocation)
        app.currentlyMovingAniLocation = list(fromLocation) # need to turn into list so that it's mutable

def drawSideCard(app):
    if app.sideCard != 'None':
        img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[app.sideCard]))
        cardGraphicURL = CMUImage(img)
        sideCardX = app.width - app.sidebarWidth/2
        drawImage(cardGraphicURL, sideCardX, app.headerHeight + app.sideBarVerticalCardSpacing + app.cardHeight/2, 
                  width=app.cardWidth, height=app.cardHeight, align='center')

def drawDoneSlots(app):
    spaceForSlots = app.width - app.sidebarWidth
    spaceBetweenSlots = spaceForSlots/(len(app.doneSlots)+1)
    
    for slot in range(len(app.doneSlots)):
        card = app.doneSlots[slot]
        doneSlotX = spaceBetweenSlots*(slot+1)
        img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[card]))
        cardGraphicURL = CMUImage(img)
        if app.isMovingAnimation and app.currentlyMovingDetails[0] == card:

            continue
        drawImage(cardGraphicURL, doneSlotX, app.height - app.headerHeight - app.cardHeight/2,
                  width=app.cardWidth, height=app.cardHeight, align='center')

def winCondition(app):
    for slot in range(len(app.doneSlots)):
        if app.doneSlots[slot][1] != 13:
            return False
    return True

def isInitialPilesSolvable(app):
    if winCondition(app):
        return True
    else:
        print(app.piles)
        for pileFrom in range(app.numPiles):
            if isMoveValid(app, pileFrom) != None:
                savedState = memorizeCurrentAppState(app) # ChatGPT prompted this idea to use a saved state
                toSlotOrPile, movedTo = isMoveValid(app, pileFrom)
                makeMove(app, pileFrom, toSlotOrPile, movedTo)
                if isInitialPilesSolvable(app):
                    return True
                undo(app, savedState) # ChatGPT prompted this idea to have an undo function
        for _ in range(len(app.sideDeck) + len(app.sideDeckFlipped)):
            flipDeck(app)
            if isMoveValid(app, 'sideCard') != None:
                savedState = memorizeCurrentAppState(app)
                toSlotOrPile, movedTo = isMoveValid(app, 'sideCard')
                makeMove(app, 'sideCard', toSlotOrPile, movedTo)
                if isInitialPilesSolvable(app):
                    return True
                undo(app, savedState)
    return False

def memorizeCurrentAppState(app):
    currentAppStateDict = {'app.piles':copy.deepcopy(app.piles), 
                           'app.sideDeck': copy.deepcopy(app.sideDeck),
                           'app.sideDeckFlipped': copy.deepcopy(app.sideDeckFlipped), 
                           'app.doneSlots': copy.deepcopy(app.doneSlots)}
    return currentAppStateDict

def undo(app, savedState):
    app.piles = savedState['app.piles']
    app.sideDeck = savedState['app.sideDeck']
    app.sideDeckFlipped = savedState['app.sideDeckFlipped']
    app.doneSlots = savedState['app.doneSlots']

def drawAnimateCardSlide(app):
    cardMoving = app.currentlyMovingDetails[0]
    img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[cardMoving]))
    cardGraphicURL = CMUImage(img)
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
    # Card Outline Graphic Source: https://www.clker.com/cliparts/5/9/8/1/13959626591670826938Playing%20Card%20Template.svg.med.png
    app.cardGraphics = dict()
    for suit in ['clover', 'spade', 'heart', 'diamond']:
        for num in range(14):
            cardTuple = (suit, num)
            
            # this is to fix the conversion cuz I call it clover and the images call it clubs
            if suit == 'clover':
                suitName = 'club'
            else:
                suitName = suit
            
            if num == 0:
                graphicName = 'EmptyCard.png'
            else:
                if num == 1:
                    graphicNameNum = 'ace'
                elif num == 11:
                    graphicNameNum = 'jack'
                elif num == 12:
                    graphicNameNum = 'queen'
                elif num == 13:
                    graphicNameNum = 'king'
                else:
                    graphicNameNum = str(num)
                graphicName = f'English_pattern_{graphicNameNum}_of_{suitName}s.png'
            app.cardGraphics[cardTuple] = graphicName
    app.cardGraphics[('back')] = 'cardBack.png'
    app.cardGraphics['empty'] = 'EmptyCard.png'

def endWin_redrawAll(app):
    drawLabel('You WON!', 200, 200)

def findPossibleMovesHint(app):
    if isMoveValid(app, 'sideCard') != None:
        app.highlightStartLocation = getCardLocation(app, 'pile', 'sideCard')
        slotOrPile, stackIndex = isMoveValid(app, 'sideCard')
        app.highlightEndLocation = getCardLocation(app, slotOrPile, stackIndex)
        return

    for pile in range(len(app.piles)): # only need loop thru the piles cuz just choose a pile and automatically looks at last
        if isMoveValid(app, pile) != None:
            app.highlightStartLocation = getCardLocation(app, 'pile', pile)
            slotOrPile, stackIndex = isMoveValid(app, pile)
            app.highlightEndLocation = getCardLocation(app, slotOrPile, stackIndex)
            return
    #if none work:
    app.highlightStartLocation = (app.width - app.sidebarWidth/2, app.headerHeight)
    app.highlightEndLocation = None

def drawHint(app):
    #startLocationCircle:
    startX, startY = app.highlightStartLocation[0], app.highlightStartLocation[1]
    drawCircle(startX, startY, 100)
    #endLocationCircle
    if app.highlightEndLocation != None: # this is incase no possible moves, so only one highlight on the sidedeck
        endX, endY = app.highlightEndLocation[0], app.highlightEndLocation[1]
        drawCircle(endX, endY, 100)



runAppWithScreens(initialScreen='game')