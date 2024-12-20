from cmu_graphics import *
import random
import copy
from PIL import Image
import os
import sys
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import cv2

# Increase recursion limit
sys.setrecursionlimit(2000)

PROBABILITY_BRAIN = 0

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
    app.probThreshold = -1
    app.piles = []
    
    app.doneSlots = [('spade',0),('heart',0),('clover',0),('diamond',0)] # use 0 cuz 1 is next after that
    app.sideCard = None
    app.sideBarVerticalCardSpacing = 200
    app.pilesVisibility = [1 for _ in range(app.numPiles)] # this indicates how many cards in the pile are visible
    app.isMovingAnimation = False
    app.currentlyMovingDetails = []
    app.currentlyMovingAniLocations = []
    app.currentlyMovingCardNames = []
    app.stepsPerSecond = 10
    app.isWrongMoveAnimation = False
    app.cardAngleShake = 5
    app.cardSlideRate = 150
    app.errorCount = 0
    app.isHintMode = False
    app.highlightStartLocation = 0
    app.highlightEndLocation = 0
    app.cardsConfetti = []
    # button stuff
    app.buttonHeight = app.headerHeight - 50
    app.buttonWidth = app.width / 15
    app.numButtonCols = 3 # not changeable easily
    app.numButtonRows = 2 # not changeable easily
    app.buttonSpacingOffEdgeX = app.buttonWidth/2 + 50 # need to do this cuz the align of the buttons are center
    app.buttonSpacingOffEdgeY = app.headerHeight/2 # align of the buttons are center so center the button in the header
    app.buttonLabels = [['Pile 1', 'Pile 2', 'Flip Deck'], ['Pile 3', 'Pile4', 'Side Card']]
    app.selectedButtonAnimation = None
    app.selectedButtonAniPadding = 10
    app.percentageTongue = 30
    # not button stuff anymore
    app.previousGameStates = []
    app.undoCount = 0
    app.giveUpUndoCount = 100
    makeInitialPiles(app)
    isSolvable = False
    while isSolvable == False:
        makeInitialPiles(app)
        piles = copy.deepcopy(app.piles)
        sideDeck = copy.deepcopy(app.sideDeck)
        if isInitialPilesSolvable(app) == True:
            isSolvable = True
            resetApp(app)
            app.piles = piles
            app.sideDeck = sideDeck
    app.cornerHistory = []
    getEyeTrackingReady(app)
    app.startScreenWords = [
    'BUTTONS INSTRUCTIONS',
    "You will see six buttons at the 6 corners/edges of the screen. Each of those buttons corresponds to a different move you can make!",
    'For example, the pile 1 button makes a move with whatever is in the first pile on the screen.', 
    'To make a move, look at the button, then think, move tongue.',
    '',
    'HOW TO PLAY SOLITAIRE',
    'To play solitaire, the goal is to build up from Ace to King (A > 2 > 3 > ... > K) in each suit in the four slots at the bottom of the screen.', 
    'You can make moves to build a chain of cards in each of the four piles at the top of the screen ',
    'as long as the cards alternate black and red suits and builds down in number (K>A).',
    'You can also flip the side deck on the right and this will show you a new card that you can try to play.', 
    '',
    'HINT FEATURE',
    "To enable hint mode, press 'h', this will display a green circle on the pile you should make a move with and ",
    "a red circle on the pile or slot the move you can make will go to"]
    

def start_redrawAll(app):
    spacingBetweenLines = 40
    lineNum = 0
    # image source: https://media.istockphoto.com/id/1400136454/photo/wood-plank-panel-texture-outdated-mahogany-table-background.jpg?s=612x612&w=0&k=20&c=qOa3uohMglKoK2pNxMmr7Y9UTyOmp92137gloikW5oM=
    drawImage('table.jpg', 0, 0, width=app.width, height=app.height)
    drawLabel('TOUCHLESS SOLITAIRE', app.width/2, app.height/9, size = 80, fill='white')
    for i in range(len(app.startScreenWords)):
        drawLabel(app.startScreenWords[i], app.width/8, 2*app.height/9+spacingBetweenLines*lineNum, fill= 'white', align = 'left', size = 20)
        lineNum +=1


def start_onKeyPress(app, key):
    setActiveScreen('game')

def game_redrawAll(app):
    # image source: https://media.istockphoto.com/id/1400136454/photo/wood-plank-panel-texture-outdated-mahogany-table-background.jpg?s=612x612&w=0&k=20&c=qOa3uohMglKoK2pNxMmr7Y9UTyOmp92137gloikW5oM=
    drawImage('table.jpg', 0, 0, width=app.width, height=app.height)
    
    drawSideDeck(app)
    drawPiles(app)
    drawSideCard(app)
    drawDoneSlots(app)
    drawButtons(app)
    if app.isMovingAnimation:
        drawAnimateCardSlide(app)
    if app.isWrongMoveAnimation:
        drawAnimateWrongShake(app)
    if app.isHintMode:
        drawHint(app)
    drawSideBar(app)
    
    
def game_onKeyPress(app, key):
    if key == '1' and PROBABILITY_BRAIN >= app.probThreshold or key == '2' and PROBABILITY_BRAIN >= app.probThreshold or key == '4' and PROBABILITY_BRAIN >= app.probThreshold or key == '5' and PROBABILITY_BRAIN >= app.probThreshold or key == '6' and PROBABILITY_BRAIN >= app.probThreshold:
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

            toSlotOrPile, movedTo = isMoveValid(app, pileFrom)
            makeMove(app, pileFrom, toSlotOrPile, movedTo)
    elif key == '3':
        flipDeck(app)
        
    if key == 'r':
        pass
        # reset(app)
    elif key == 'h':
        app.isHintMode = not app.isHintMode

    if app.isHintMode: # checks on every key press 
        findPossibleMovesHint(app)
        
    if winCondition(app): 
            setActiveScreen('endWin')

def game_onStep(app):
    global unsubscribe # chatGPT gave me the idea to set unsubscribe as a global var.
    unsubscribe = neurosity.calm(callback)
    
    corner = gettingGazeCorner(app)
    app.cornerHistory.append(corner)
    if len(app.cornerHistory)>3 and app.cornerHistory[-3:] == [None, None, None]:
        while len(app.cornerHistory) > 1 and app.cornerHistory[-1] == None:
            app.cornerHistory.pop()
        key = app.cornerHistory[-1]
    else:
        key = None
    if key != None:
        if key == '1' and PROBABILITY_BRAIN >= app.probThreshold or key == '2' and PROBABILITY_BRAIN >= app.probThreshold or key == '4' and PROBABILITY_BRAIN >= app.probThreshold or key == '5' and PROBABILITY_BRAIN >= app.probThreshold or key == '6' and PROBABILITY_BRAIN >= app.probThreshold:
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
                toSlotOrPile, movedTo = isMoveValid(app, pileFrom)
                makeMove(app, pileFrom, toSlotOrPile, movedTo)
        elif key == '3':
            flipDeck(app)
        if winCondition(app): 
            setActiveScreen('endWin')
    
    
    if app.isMovingAnimation:
        for cardIdx in range(len(app.currentlyMovingDetails)):
            xMoveRateSign = app.currentlyMovingDetails[cardIdx][1]
            yMoveRate = app.currentlyMovingDetails[cardIdx][2]
            endLocation = app.currentlyMovingDetails[cardIdx][4]
            app.currentlyMovingAniLocations[cardIdx][0] += xMoveRateSign*app.cardSlideRate
            app.currentlyMovingAniLocations[cardIdx][1] += yMoveRate*app.cardSlideRate
            if xMoveRateSign < 0: # moving right to left
                if app.currentlyMovingAniLocations[cardIdx][0] <= endLocation[0]:
                    app.isMovingAnimation = False 
            else: # moving left to right
                if app.currentlyMovingAniLocations[cardIdx][0] >= endLocation[0]:
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

def resetApp(app):
    app.piles = []
    app.sideDeck = copy.deepcopy(app.fullDeck)
    app.sideDeckFlipped = []
    app.doneSlots = [('spade',0),('heart',0),('clover',0),('diamond',0)]
    app.undoCount = 0
    app.sideCard = None
    app.pilesVisibility = [1 for _ in range(app.numPiles)] # this indicates how many cards in the pile are visible

def makeInitialPiles(app): # setting up the piles of a new game
    resetApp(app)

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
                          align = 'center', fill = None, border = 'white')
            drawLabel(app.buttonLabels[row][col], buttonX, buttonY, align = 'center', fill = 'white')

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
    # image source: https://e7.pngegg.com/pngimages/78/314/png-clipart-wood-stain-varnish-hardwood-line-angle-line-angle-wood-thumbnail.png
    drawImage('stick.png', sidebarX, 0, height = app.height, width = 100)

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
            # chatGPT gave me the idea for this 'continue' method
            if app.isMovingAnimation and app.piles[pile][card] in app.currentlyMovingCardNames:
                continue
            
            drawImage(cardGraphicURL, cardX, cardY + app.cardHeight/2, 
                      width=app.cardWidth, height=app.cardHeight, align='center')

def flipDeck(app):
    if app.sideDeck == [] and app.sideDeckFlipped == []:
        app.sideCard = None
        return
    elif app.sideDeck == []:
        app.sideDeck = copy.deepcopy(app.sideDeckFlipped)
        app.sideDeckFlipped = []
        app.sideCard = None
        return
    cardFlipped = app.sideDeck.pop()
    app.sideCard = cardFlipped
    app.sideDeckFlipped.append(cardFlipped)

def isMoveValid(app, pileFrom): # pileFrom is the index into app.piles or 'sideCard'
    # ============ THIS PART CHECKS IF PILE OR SIDECARD TO SLOT ===============
    if pileFrom == 'sideCard':
        if app.sideCard == None:
            app.errorCount += 1
            return None
        else:
            cardToMove = app.sideCard
    elif app.piles[pileFrom] == []: # this is if the pile is empty
        app.errorCount += 1
        return None
    else: # if from one of the piles 
        # cardToMove is last in pile (only last in pile can go into a slot, not the first visible if there is a chain)
        cardToMove = app.piles[pileFrom][-1]
    cardToMoveSuit = cardToMove[0]
    cardToMoveColor = getCardColor(cardToMove)
    cardToMoveNum = cardToMove[1]

    for slot in range(len(app.doneSlots)):
        currSlotSuit = app.doneSlots[slot][0]
        currSlotNum = app.doneSlots[slot][1]
        if currSlotSuit == cardToMoveSuit:
            if currSlotNum+1 == cardToMoveNum:
                return 'slot', slot

    # Only enter this part if above doesn't return anything (if there are no valid moves moving to piles)
    # =========== THIS PART CHECKS FOR NORMAL MOVES FROM PILE TO PILE OR SIDECARD TO PILE ============
    if pileFrom != 'sideCard': # if from one of the piles (no need to set cardToMove for sideCard cuz alr done above)
        # need to change the cardToMove to be the first visible in a pile because if moving from pile to pile, the whole chain needs to move 
        numCardsOpenInPile = app.pilesVisibility[pileFrom] #this is the card num (counting from the back) that should be checked (the first visible card in the pile)
        cardToMove = app.piles[pileFrom][-1*numCardsOpenInPile]
        cardToMoveSuit = cardToMove[0]
        cardToMoveColor = getCardColor(cardToMove)
        cardToMoveNum = cardToMove[1]

    for pile in range(app.numPiles):
        if pile == pileFrom:
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
            return 'pile', pile
    
    app.errorCount += 1
    return None

def getCardColor(card):
    suit = card[0]
    return 'red' if suit == 'heart' or suit == 'diamond' else 'black'

def getCardLocation(app, slotOrPile, stackIndex, cardIndexFromLow): #cardIndex is the index of card in a pile from low to high, if sideCard, just do None
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
    # ============ THIS PART IS TO GET THE INFO ABOUT THE CARD MOVING AND WHERE IT'S FROM ================
    if pileFrom == 'sideCard': # if from sideCard
        # Getting the number of moving cards (for sideCard it can only be on at a time)
        numMovingCards = 1
        # Getting the cards that are moving (it will always only be one but still must be in a list)
        cardsMoving = [app.sideDeckFlipped.pop()] # make sure it's in a list because we use extend list later.
        # Setting the sideCard to the previous card (as long as there was one)
        if app.sideDeckFlipped == []:
            app.sideCard = None
        else:
            # This was the problem!! Cannot just pop agaiin cuz the sideDeckFlipped is supposed to have app.sideCard in it!!!!!!!!!!!
            app.sideCard = app.sideDeckFlipped[-1]
    elif toSlotOrPile == 'slot': # if from a pile to a slot
        numMovingCards = 1
        cardsMoving = [app.piles[pileFrom].pop()] # just the last one cuz pile --> slot
        if app.piles[pileFrom] == []: # now empty pile
            app.pilesVisibility[pileFrom] = 0
        elif app.pilesVisibility[pileFrom] == 1: # if it's visibility was 1, stay at always 1 open (make sure it never goes to 0! (cuz we don't want a pile with no cards flipped over)
            pass
        else:
            app.pilesVisibility[pileFrom] -= 1

    else: # if from a pile to a pile
        # Getting the number of moving cards
        numMovingCards = app.pilesVisibility[pileFrom] # cuz whenever we move, we will move the whole visible chain in a pile
        # Setting the visibility to the right number (it will always be 1 because pile --> pile always move everything)
        app.pilesVisibility[pileFrom] = 1
        # do the location getting before popping so that we have the right number of cards in pile (pre-pop)
        # Getting the cards that are moving (a list of tuples)
        cardsMoving = app.piles[pileFrom][-numMovingCards:] # chatGPT gave me the idea to use slicing instead of pop
        # Removing the moving cards from it's initial pile
        app.piles[pileFrom] = app.piles[pileFrom][:-numMovingCards] # does not need to -1 again in numMovingCards cuz its a negative index
    
    # ============ THIS PART IS TO GET THE INFO ABOUT WHERE IT'S GOING ================
    if toSlotOrPile == 'slot':
        app.doneSlots[movedTo] = cardsMoving[0] # just index 0 cuz we know only one card can move into the slot
    elif toSlotOrPile == 'pile':
        app.piles[movedTo].extend(cardsMoving)
        app.pilesVisibility[movedTo] += numMovingCards
        # this is to make sure there's never more visible cards than there are cards in the pile
        if app.pilesVisibility[movedTo]  > len(app.piles[movedTo]):
            app.pilesVisibility[movedTo] = len(app.piles[movedTo])

    # ============ THIS PART IS TO GET THE LOCATIONS FROM AND TO AND ANIMATION INFO ================
    # Everytime enter makeMove, these variables will become empty again
    app.currentlyMovingDetails = []
    app.currentlyMovingAniLocations = []
    app.currentlyMovingCardNames = []
    # note that we'll hafta flip this list cuz the cardsMoving list is in order from front to back but we are looping through indexes from back to front in the for loop below
    cardsMoving = cardsMoving[::-1]
    for cardBackIndex in range(numMovingCards-1, -1, -1): # cardBackIndex is the index from back to front of the card being moved ex. if 2 cards moving, the indexes will be 1 then 0
        # extract the card we're currently calculating for, this is to put this info into the details list later
        cardMoving = cardsMoving[cardBackIndex]

        fromLocation = getCardLocation(app, 'pile', pileFrom, cardBackIndex-numMovingCards) # it's always going to come from a pile cannot come from a slot, also, need to do the -numMovingCards because we popped before calculating the location, note that this may give a negative number
        fromLocationX = fromLocation[0]
        fromLocationY = fromLocation[1]

        toLocation = getCardLocation(app, toSlotOrPile, movedTo, cardBackIndex)
        toLocationX = toLocation[0]
        toLocationY = toLocation[1]
        
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
        app.currentlyMovingDetails.append((cardMoving, xMoveRateSign, yMoveRate, fromLocation, toLocation)) # appending the tuple
        app.currentlyMovingAniLocations.append(list(fromLocation)) # need to turn into list so that it's mutable
        app.currentlyMovingCardNames.append(cardMoving) # this gets a list of just the card names that are currently moving
    
def drawSideCard(app):
    if app.sideCard != None:
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
        # chatGPT gave me the idea for this 'continue' method
        if app.isMovingAnimation and card in app.currentlyMovingCardNames:
            suit = card[0]
            num = card[1]
            img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[(suit, num-1)]))
            cardGraphicURL = CMUImage(img)
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
        if app.undoCount >= app.giveUpUndoCount:
            return False
        if len(app.sideDeck) + len(app.sideDeckFlipped) == 0:
            rangeNumber = 1
        else:
            rangeNumber = len(app.sideDeck) + len(app.sideDeckFlipped)
        for _ in range(rangeNumber):
            flipDeck(app)
            for pileFrom in range(app.numPiles):
                if app.sideCard != None and isMoveValid(app, 'sideCard') != None:
                    savedState = memorizeCurrentAppState(app)
                    toSlotOrPile, movedTo = isMoveValid(app, 'sideCard')
                    makeMove(app, 'sideCard', toSlotOrPile, movedTo)

                    if isInitialPilesSolvable(app) != False:
                        return True
                    undo(app, savedState)
                elif isMoveValid(app, pileFrom) != None:
                    savedState = memorizeCurrentAppState(app) # ChatGPT prompted this idea to use a separate saved state function
                    app.previousGameStates.append((app.piles, app.doneSlots))
                    if len(app.previousGameStates) > 2:
                        app.previousGameStates.pop(0)
                    
                    toSlotOrPile, movedTo = isMoveValid(app, pileFrom)
                    makeMove(app, pileFrom, toSlotOrPile, movedTo)

                    # this part is to check if this state has been seen before.
                    if toSlotOrPile == 'pile': # not if going into a slot
                        if (app.piles, app.doneSlots) in app.previousGameStates:
                            undo(app, savedState)
                            continue
                    
                    if isInitialPilesSolvable(app) != False:
                        return True
                    undo(app, savedState)
        return False

def memorizeCurrentAppState(app):
    currentAppStateDict = {'app.piles':copy.deepcopy(app.piles),
                            'app.sideCard': copy.deepcopy(app.sideCard),
                           'app.sideDeck': copy.deepcopy(app.sideDeck),
                           'app.sideDeckFlipped': copy.deepcopy(app.sideDeckFlipped), 
                           'app.doneSlots': copy.deepcopy(app.doneSlots),
                           'app.pilesVisibility': copy.deepcopy(app.pilesVisibility)}
    return currentAppStateDict

def undo(app, savedState):
    app.undoCount += 1
    app.piles = savedState['app.piles']
    app.sideCard = savedState['app.sideCard']
    app.sideDeck = savedState['app.sideDeck']
    app.sideDeckFlipped = savedState['app.sideDeckFlipped']
    app.doneSlots = savedState['app.doneSlots']
    app.pilesVisibility = savedState['app.pilesVisibility']
    if len(app.previousGameStates) > 0:
        app.previousGameStates.pop()

def drawAnimateCardSlide(app):
    for cardIdx in range(len(app.currentlyMovingDetails)): # cardIdx is the idx of the list of cards moving
        cardMoving = app.currentlyMovingDetails[cardIdx][0]
        img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[cardMoving]))
        cardGraphicURL = CMUImage(img)
        drawImage(cardGraphicURL, app.currentlyMovingAniLocations[cardIdx][0], app.currentlyMovingAniLocations[cardIdx][1], 
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
    # image source: https://media.istockphoto.com/id/1400136454/photo/wood-plank-panel-texture-outdated-mahogany-table-background.jpg?s=612x612&w=0&k=20&c=qOa3uohMglKoK2pNxMmr7Y9UTyOmp92137gloikW5oM=
    drawImage('table.jpg', 0, 0, width=app.width, height=app.height)
    drawLabel('You WON!', app.width/2, app.height/2, size = 100, fill = 'white')
    for card in app.cardsConfetti:
        img = Image.open(os.path.join('cardGraphicsPNG', app.cardGraphics[card]))
        cardGraphicURL = CMUImage(img)
        drawImage(cardGraphicURL, random.randint(0, app.width), random.randint(0, app.height), 
                    width=app.cardWidth, height=app.cardHeight, align='center')

def endWin_onStep(app):
    randomCardIndex = random.randint(0,len(app.fullDeck)-1)
    app.cardsConfetti.append(app.fullDeck[randomCardIndex])
    

def endWin_onKeyPress(app, key):
    quit()

def findPossibleMovesHint(app):
    if isMoveValid(app, 'sideCard') != None:
        app.highlightStartLocation = getCardLocation(app, 'pile', 'sideCard', None)
        slotOrPile, stackIndex = isMoveValid(app, 'sideCard')
        app.highlightEndLocation = getCardLocation(app, slotOrPile, stackIndex, 0)
        return

    for pile in range(len(app.piles)): # only need loop thru the piles cuz just choose a pile and automatically looks at last
        if isMoveValid(app, pile) != None:
            app.highlightStartLocation = getCardLocation(app, 'pile', pile, 0)
            slotOrPile, stackIndex = isMoveValid(app, pile)
            app.highlightEndLocation = getCardLocation(app, slotOrPile, stackIndex, 0)
            return
    #if none work:
    app.highlightStartLocation = (app.width - app.sidebarWidth/2, app.headerHeight)
    app.highlightEndLocation = None

def drawHint(app):
    #startLocationCircle:
    startX, startY = app.highlightStartLocation[0], app.highlightStartLocation[1]
    drawCircle(startX, startY, 50, fill='green')
    #endLocationCircle
    if app.highlightEndLocation != None: # this is incase no possible moves, so only one highlight on the sidedeck
        endX, endY = app.highlightEndLocation[0], app.highlightEndLocation[1]
        drawCircle(endX, endY, 50, fill = 'red')

def callback(data):
    global PROBABILITY_BRAIN
    PROBABILITY_BRAIN = data.get('probability')

def getEyeTrackingReady(app): # the contents of this function are from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    # Load cascades
    app.face_cascade = cv2.CascadeClassifier('examples/haarcascades/haarcascade_frontalface_default.xml')
    app.eye_cascade = cv2.CascadeClassifier('examples/haarcascades/haarcascade_eye.xml')

    # Parameters for blob detection
    detector_params = cv2.SimpleBlobDetector_Params()
    detector_params.filterByArea = True
    detector_params.maxArea = 1500
    app.detector = cv2.SimpleBlobDetector_create(detector_params)

    app.cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

def cut_eyebrows(img): # the contents of this function are from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    height, _ = img.shape[:2]
    eyebrow_h = int(height / 4)
    return img[eyebrow_h:, :]  # Cut eyebrows out

def blob_process(img, threshold, detector): # the contents of this function are from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)
    return keypoints

def detect_faces(img, classifier): # the contents of this function are from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_frame, 1.3, 5)
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # Get the largest face
        return img[y:y+h, x:x+w]
    return None

def detect_eyes(img, classifier): # the contents of this function are slightly adjusted from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = classifier.detectMultiScale(gray_frame, 1.3, 5)
    height, width = img.shape[:2]
    left_eye, leftEyeCoords, right_eye, rightEyeCoords= None, None, None, None
    
    for (x, y, w, h) in eyes:
        if y > height / 2:
            continue  # Skip detections below the midpoint of the face
        eye_center = x + w / 2
        if eye_center < width / 2:
            left_eye = img[y:y+h, x:x+w]
            leftEyeCoords = (x, y, w, h)
        else:
            right_eye = img[y:y+h, x:x+w]
            rightEyeCoords = (x, y, w, h)
    return left_eye, leftEyeCoords, right_eye, rightEyeCoords

def nothing(x): # the contents of this function are from https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
    pass

def gettingGazeCorner(app):
    ret, frame = app.cap.read()
    
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    
    face_frame = detect_faces(frame, app.face_cascade)
    if face_frame is not None:
        leftEyePic, leftEyeCoords, rightEyePic, rightEyeCoords = detect_eyes(face_frame, app.eye_cascade)
        for eye in (leftEyePic, rightEyePic):
            if eye is not None:
                threshold = cv2.getTrackbarPos('threshold', 'image')
                eye = cut_eyebrows(eye)
                keypoints = blob_process(eye, threshold, app.detector)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                for keypoint in keypoints:
                    
                    # below all my own code:
                    compareXL, compareXR, compareYL, compareYR = None, None, None, None
                    if leftEyeCoords != None:
                        pupilX = keypoint.pt[0]
                        pupilY = keypoint.pt[1]
                        leftEyeWidth = leftEyeCoords[2]
                        leftEyeHeight = leftEyeCoords[3]
                        compareYL = pupilY/leftEyeHeight
                        compareXL = pupilX/leftEyeWidth
                    if rightEyeCoords != None:
                        pupilX = keypoint.pt[0]
                        pupilY = keypoint.pt[1]
                        rightEyeWidth = rightEyeCoords[2]
                        rightEyeHeight = rightEyeCoords[3]
                        compareYR = pupilY/rightEyeHeight
                        compareXR = pupilX/rightEyeWidth
                    compareX = 0
                    numValsX = 0
                    compareY = 0
                    numValsY = 0
                    for val in (compareXR, compareXL):
                        if val != None:
                            compareX += val
                            numValsX += 1
                    compareX/=numValsX
                    for val in (compareYR, compareYL):
                        if val != None:
                            compareY += val
                            numValsY += 1
                    compareY/=numValsY

                    if compareX > 0.6:
                        if compareY > 0.22:
                            print('looking right-down',compareX,compareY)
                            return '6'
                        else:
                            print('looking right-up',compareX,compareY)
                            return '3'
                    elif compareX < 0.46:
                        if compareY > 0.22:
                            print('looking left-down',compareX,compareY)
                            return '4'
                        else:
                            print('looking left-up',compareX,compareY)
                            return '1'
                    else:
                        if compareY > 0.22:
                            print('looking center-down',compareX,compareY)
                            return '5'
                        else:
                            print('looking center-up',compareX,compareY)
                            return '2'
    
    print('None')
   
    



# ____________________MAIN ________________________
# this code comes from neurosity docs
load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

info = neurosity.get_info()
print(info)

runAppWithScreens(initialScreen='start')