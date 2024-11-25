from cmu_graphics import *
# from solidtaire import app.headerHeight # how do I do this???

def onAppStart(app):
    app.width = 1500
    app.height = 750
    app.headerHeight = app.height/5
    app.buttonHeight = app.headerHeight - 50
    app.buttonWidth = app.width / 15
    app.numButtonCols = 3 # not changeable easily
    app.numButtonRows = 2 # not changeable easily
    app.buttonSpacingOffEdgeX = app.buttonWidth/2 + 50 # need to do this cuz the align of the buttons are center
    app.buttonSpacingOffEdgeY = (app.headerHeight - app.buttonHeight) / 2 + app.buttonWidth/2 # need to add the app.buttonWidth/2 cuz align of the buttons are center
    app.buttonLabels = [['pile 1', 'pile2', 'flip deck'], ['pile 3', 'pile4', 'side card']]
    app.selectedButtonAnimation = None
    app.selectedButtonAniPadding = 10

def redrawAll(app):
    for row in range(app.numButtonRows):
        for col in range(app.numButtonCols):
            buttonX, buttonY = getButtonXY(app, row, col)
            drawRect(buttonX, buttonY, app.buttonWidth, app.buttonHeight,
                          align = 'center', fill = None, border = 'black')
            drawLabel(app.buttonLabels[row][col], buttonX, buttonY, align = 'center')

    if app.selectedButtonAnimation !=None:
        row = app.selectedButtonAnimation[0]
        col = app.selectedButtonAnimation[1]
        buttonCenterX, buttonCenterY = getButtonXY(app, row, col)
        leftX = buttonCenterX - app.buttonWidth/2 - app.selectedButtonAniPadding
        topY = buttonCenterY - app.buttonHeight/2 - app.selectedButtonAniPadding
        rightX = buttonCenterX + app.buttonWidth/2 + app.selectedButtonAniPadding
        bottomY = buttonCenterY + app.buttonHeight/2 + app.selectedButtonAniPadding
        drawLine(leftX, topY, rightX, topY)
            
def onStep(app):
    if app.selectedButtonAnimation != None:
        app.percentageTongue +=1 # this is a placeholder for now

def onKeyPress(app, key):
    if key == 'p':
        app.selectedButtonAnimation = (0,0) # this is button 1

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
    

runApp()