'''
physics_project.py
@author: n. lovett
started 7/30/24
'''

#imports
import pygame
pygame.init()
import math

#variables: screen setup
screen = pygame.display.set_mode((950, 750))
pygame.display.set_caption("FBD Creator")
pygame.display.set_icon(pygame.image.load(r"assets\icon.png"))
floor = pygame.Rect(0, 550, 750, 2)
sidePanel = pygame.Rect(750, 0, 2, 750)
font = pygame.font.SysFont("AnonymousPro", 24)
italicFont = pygame.font.SysFont("AnonymousPro", 24, False, True)
popup = False
infoGoesUp = False
escapeRect = pygame.Rect(20, 5, 15, 15)
gridUp = False
displayComingSoon = False
#time
clock = pygame.time.Clock()
fps = 30 #i made this up
pxPerM = 100 #pixels per meter
#variables: colors:
cursorColor = pygame.Color(64, 194, 103)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
grey = pygame.Color(75, 75, 75)
lightGrey = pygame.Color(125, 125, 125)
red = pygame.Color(232, 49, 49)
orange = pygame.Color(255, 156, 56)
yellow = pygame.Color(228, 245, 32)
lightGreen = pygame.Color(73, 214, 73)
green = pygame.Color(0, 110, 0)
teal = pygame.Color(52, 209, 204)
blue = pygame.Color(50, 151, 252)
purple = pygame.Color(175, 91, 240)
magenta = pygame.Color(238, 47, 245)
pink = pygame.Color(255, 107, 201)
aColors = [lightGreen, blue, purple, red, magenta, orange, teal, pink, green]#available colors
rainbow = (red, orange, yellow, lightGreen, green, teal, blue, purple, magenta, pink)
#tabs 
formulas = pygame.image.load(r"assets\formulaSheet1.png")
formulas = pygame.transform.scale(formulas, (198, 198*formulas.get_height()/formulas.get_width()))
formulaTab = pygame.Rect(sidePanel.right, 2, (screen.get_width()-sidePanel.right-4)//2, 36)
dataTab = pygame.Rect(formulaTab.right+2, 2, (screen.get_width()-sidePanel.right-4)//2, 36)
tabs = [formulaTab, dataTab]
tabTexts = ["Formulas", "Data"]
currentTab = formulaTab
currentBlockTab = 'red'
cE = pygame.draw.circle(screen, white, (0, 0), 0, -1)
pInE = pygame.draw.circle(screen, white, (0, 0), 0, -1)
inE = pygame.draw.circle(screen, white, (0, 0), 0, -1)

hammerImg = pygame.transform.scale(pygame.image.load(r"assets\hammer.png"), (26, 25))

#squares
redSquareLoc = [10, 50]
redSquare = {"name":"red", 'tab':pygame.Rect(0,0,0,0), 'color':red, "base":pygame.Rect(redSquareLoc[0]+2, redSquareLoc[1]+2, 46, 46)}
redSquare["border"] = pygame.Rect(redSquareLoc, (50, 50))
yellowSquareLoc = [210, 50]
yellowSquare = {"name":"yellow", 'color':yellow, "base":pygame.Rect(yellowSquareLoc[0]+2, yellowSquareLoc[1]+2, 46, 46)}
yellowSquare["border"] = pygame.Rect(yellowSquareLoc, (50, 50))
tealSquareLoc = [410, 50]
tealSquare = {"name":"teal", 'color':teal, "base":pygame.Rect(tealSquareLoc[0]+2, tealSquareLoc[1]+2, 46, 46)}
tealSquare["border"] = pygame.Rect(tealSquareLoc, (50, 50))
squareCounter = 0
squares = [redSquare, yellowSquare, tealSquare]
blitSquares = []
#add a/v/m/etc
muImg = pygame.transform.scale(pygame.image.load(r'assets\mu.png'), (93*30//93, 102*30//93))
muTextRect = pygame.Rect(0,0,0,0)

variableNames = ["x", "y", "z", "a", "b", "c", "d"]

for i in range(len(squares)):
    squares[i]["Vx"] = 0
    squares[i]["Vy"] = 0
    squares[i]["a"] = 0
    squares[i]["m"] = squares[i]["border"].width//5
    squares[i]["Fnet"] = 0
    squares[i]["Fn"] = 0
    squares[i]["Fnetx"] = 0
    squares[i]["Fnety"] = 0
    squares[i]["Ff"] = 0
    squares[i]["m<Fnet"] = 90
    squares[i]["FnetDir"] = ""
    squares[i]["tab"] = pygame.Rect(0,0,0,0)

#variables: physics
startedYet = False
forcesUp = False
updateFapp = False
saveFapp = False
ySaveFapp = False
yUpdateFapp = False  
FnetArrow = False
scaled = True
showVCbool = False
Kpercent = 1.0
gravity = 9.8
mu = 0.2
gravityFPS = round(gravity/30, 4)
applyForce = True
FappA = {}
FappB = {}
FappC = {}
redFapps = [FappA, FappB, FappC]
FappD = {}
FappE = {}
FappF = {}
tealFapps = [FappD, FappE, FappF]
FappG = {}
FappH = {}
FappI = {}
yellowFapps = [FappG, FappH, FappI]
currentlyEditing = "" #this is which one is clicked
newData = ""#this is what the user has typed
rects = {} #for storing data text rects
dataNames = []

startButton = pygame.Rect(0,0,0,0)
#functions: screen setup
def createCover():
    global startButton, rainbow
    coverColors = rainbow+rainbow+rainbow
    screen.fill(white)
    hugeFont = pygame.font.SysFont("AnonymousPro", 60)
    hugishFont = pygame.font.SysFont("AnonymousPro", 50)    
    startFont = pygame.font.SysFont("AnonymousPro", 45)
    #title
    text = hugeFont.render("FBD Creator", True, black)
    titleBorder = pygame.Rect(0, 0, 300, 300)
    titleBorder.center = (screen.get_width()//2, screen.get_height()//2-100)
    pygame.draw.rect(screen, black, titleBorder)
    pygame.draw.rect(screen, teal, (titleBorder.left+5, titleBorder.top+5, 290, 290))
    textRect = text.get_rect()
    textRect.center = (titleBorder.centerx, titleBorder.centery-20)
    screen.blit(text, textRect)
    lighterTeal = pygame.Color(91, 240, 235)
    text = hugishFont.render("by N. Lovett", True, lighterTeal)
    textRect = text.get_rect()
    textRect.center = (titleBorder.centerx, titleBorder.centery+25)
    screen.blit(text, textRect)
    #cascading squares
    for j in range(2):
        for i in range(len(coverColors[:(750//50)])): 
            if i % 2 == 0:
                border = pygame.draw.rect(screen, black, (100+725*j, 50*i, 50, 50))
                fill = pygame.draw.rect(screen, coverColors[i], (102+725*j, 50*i+2, 46, 46))
            else:
                border = pygame.draw.rect(screen, black, (75+725*j, 50*i, 50, 50))
                fill = pygame.draw.rect(screen, coverColors[i], (77+725*j, 50*i+2, 46, 46))
            text = font.render('10 kg.', True, black)
            textRect = text.get_rect()
            textRect.center = fill.center
            screen.blit(text, textRect)
    #credits & start button
    pygame.draw.rect(screen, black, (950//2-250//2, 550, 250, 60))#border
    startButton = pygame.Rect(954//2-250//2, 552, 246, 56)
    text = startFont.render("Start", True, black)
    textRect = text.get_rect()
    textRect.center = startButton.center
    if startButton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, white, startButton)           
    else:
        pygame.draw.rect(screen, (240, 240, 240), startButton)     
    screen.blit(text, textRect)

def infoPanel():
    font = pygame.font.SysFont("AnonymousPro", 30)
    info = ["Left-click to drag blocks,", "& right-click to add forces.", "NOTE: kinematics are not", "synced to real-world time atm"]    
    border = pygame.draw.rect(screen, black, (250, 185, 310, 200))
    page = pygame.draw.rect(screen, white, (252, 187, 306, 196))
    for i in range(len(info)):
        text = font.render(info[i], True, black)
        textRect = text.get_rect()
        textRect.center = (page.centerx, page.top+40+30*i)
        screen.blit(text, textRect)
    addX(page)
    
def makeTabs():
    global sidePanel, currentTab, tabs
    font = pygame.font.SysFont("AnonymousPro", 28)
    lightBlue = (105, 162, 219)
    lighterBlue = (115, 172, 229)
    pygame.draw.rect(screen, black, sidePanel)
    tabsBorder = pygame.draw.rect(screen, black, (sidePanel.right, 0, screen.get_width()-sidePanel.right, 40))
    for tab in tabs:
        if tab == currentTab:
            if tab.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, lighterBlue, tab)
            else:
                pygame.draw.rect(screen, lightBlue, tab)
        elif tab.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, white, tab)
        else:
            pygame.draw.rect(screen, (240, 240, 240), tab)
    for i in range(len(tabTexts)):
        text = font.render(tabTexts[i], True, black)
        textRect = text.get_rect()
        textRect.center = tabs[i].center
        screen.blit(text, textRect)
    if currentTab == formulaTab:
        screen.blit(formulas, (sidePanel.right, tabsBorder.bottom))
    else:
        blitData()

def collisionOps():
    #collision option setup
    global Kpercent, pInE, inE, cE
    #collision colors
    reg = (53, 119, 219)
    lightReg = (98, 149, 227)
    greenish = (81, 196, 219)
    lightGreenish = (118, 202, 219)
    purplish = (83, 72, 240)
    lightPurplish = (132, 125, 240)
    largerFont = pygame.font.SysFont("AnonymousPro", 30)
    tinyFont = pygame.font.SysFont("AnonymousPro", 15)
    sectionW = screen.get_width()-sidePanel.right
    text = font.render("Collision Options", True, black)
    textRect = text.get_rect()
    textRect.midbottom = (sidePanel.right -5 + sectionW//2, 85)
    screen.blit(text, textRect)
    text = tinyFont.render("Perfectly", True, black)
    textRect = text.get_rect()
    textRect.midtop = (sidePanel.right+(sectionW//8), 90)
    screen.blit(text, textRect)
    text = tinyFont.render("Inelastic", True, black)
    textRect = text.get_rect()
    textRect.midtop = (sidePanel.right+(sectionW//8), 105)
    screen.blit(text, textRect)
    text = tinyFont.render("Completely", True, black)
    textRect = text.get_rect()
    textRect.midtop = (sidePanel.right+7*(sectionW//8), 90)
    screen.blit(text, textRect)
    text = tinyFont.render("Elastic", True, black)
    textRect = text.get_rect()
    textRect.midtop = (sidePanel.right+7*(sectionW//8), 105)
    screen.blit(text, textRect)
    pInEBorder = pygame.draw.circle(screen, black, (sidePanel.right+(sectionW//3)-5, 100), 10)
    pInE = pygame.draw.circle(screen, white, (sidePanel.right+(sectionW//3)-5, 100), 8)
    inEBorder = pygame.draw.circle(screen, black, (sidePanel.right+(sectionW//2)-5, 100), 10)
    inE = pygame.draw.circle(screen, white, (sidePanel.right+(sectionW//2)-5, 100), 8)
    cEBorder = pygame.draw.circle(screen, black, (sidePanel.right+2*(sectionW//3)-5, 100), 10)
    cE = pygame.draw.circle(screen, white, (sidePanel.right+2*(sectionW//3)-5, 100), 8)
    pygame.draw.line(screen, black, (pInEBorder.right, 100), (inEBorder.left, 100), 2)
    pygame.draw.line(screen, black, (inEBorder.right, 100), (cEBorder.left, 100), 2)
    if Kpercent == 1.0:
        pygame.draw.circle(screen, purplish, cE.center, 5)
    if cE.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, lightPurplish, cE.center, 5)
    if Kpercent == 0.5:
        pygame.draw.circle(screen, reg, inE.center, 5)
    if inE.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, lightReg, inE.center, 5)
    if Kpercent == 0.0:
        pygame.draw.circle(screen, greenish, pInE.center, 5)
    if pInE.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, lightGreenish, pInE.center, 5)

def saveMu():
    global mu, newData, currentlyEditing
    goodChars = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    newerData = ""
    for char in newData:
        if char in goodChars:
            newerData += char
            if char == '.':
                goodChars.remove('.')
    if newerData != '':
        newerData = abs(float(newerData))
        if newerData > 2:
            place = len(str(int(newerData)))
            newerData = newerData / (10**place)
        if len(str(newerData)) > 7:
            newerData = float(str(newerData)[:7])
        #newer data mods are done
        mu = newerData
    currentlyEditing = ""
    newData = ""

def saveNotMuData():
    global dataNames, newData, currentlyEditing, currentBlockTab
    goodChars = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    newerData = ""
    for char in newData:
        if char in goodChars:
            newerData += char
            if char == '.':
                goodChars.remove('.')
    if newerData != '':
        if '.' in newerData:
            newerData = float(newerData)
        else:
            newerData = int(newerData)
        #you should add limits for the different datas
        #also fix acceleration
        for datum in dataNames:
            for square in squares:
                if square['name'] == currentBlockTab and currentlyEditing == datum:
                    square[datum] = newerData
    currentlyEditing = ""
    newData = ""
    
def vectorComponents():        
    for vector in redFapps+yellowFapps+tealFapps:
        if vector != {}:
            d = vector['dir'][0]/2, vector['dir'][1]/2            
            x = vector['x']
            y = vector['y']
            startx = vector['basePt']
            starty = (startx[0]+d[0]*x, startx[1]+d[1]*5)
            xpoints = ((startx[0], startx[1]-1), (startx[0]+d[0]*x, startx[1]-1), (startx[0]+d[0]*x, startx[1]+1), (startx[0], startx[1]+1))
            xtip = ((startx[0]+d[0]*x, startx[1]-3), (startx[0]+d[0]*x, startx[1]+3), (startx[0]+d[0]*x+d[0]*5, startx[1]+1), (startx[0]+d[0]*x+d[0]*5, startx[1]-1))
            ypoints =((starty[0]-1, starty[1]), (starty[0]-1, starty[1]+d[1]*y-d[1]*5),  (starty[0]+1, starty[1]+d[1]*y-d[1]*5), (starty[0]+1, starty[1]))
            ytip = ((starty[0]-3, starty[1]+d[1]*y-d[1]*5), (starty[0]+3, starty[1]+d[1]*y-d[1]*5), (starty[0]+1, starty[1]+d[1]*y), (starty[0]-1, starty[1]+d[1]*y))
            if x != 0:
                pygame.draw.polygon(screen, vector['color'], xpoints)
                pygame.draw.polygon(screen, vector['color'], xtip)
            if y != 0:
                pygame.draw.polygon(screen, vector['color'], ypoints)
                pygame.draw.polygon(screen, vector['color'], ytip)
        
def blitData():
    global redSquare, redFapps, redSquareLoc, blitSquares, squares, currentBlockTab, mu, currentlyEditing, dataNames, newData, muTextRect, rects
    largerFont = pygame.font.SysFont("AnonymousPro", 30)
    tinyFont = pygame.font.SysFont("AnonymousPro", 15)
    sectionW = screen.get_width()-sidePanel.right
    #mu 
    screen.blit(muImg, (sidePanel.right, 40))
    if currentlyEditing == 'mu':
        text = italicFont.render("=  " + newData + '_', True, black)
    else:
        text = font.render("=  " + str(mu), True, black)
    muTextRect = text.get_rect()
    muTextRect.midleft = (sidePanel.right+muImg.get_width(), 38+muImg.get_height()//2)
    screen.blit(text, muTextRect)
    #collision
    collisionOps()
    #block tabs
    textRect = largerFont.render("Block Stats", True, black).get_rect()
    squaresBorder = pygame.draw.rect(screen, black, (sidePanel.right, 150, sectionW, 40))
    textRect.midbottom = ((sidePanel.right + (sectionW)//2), 150)
    screen.blit(largerFont.render("Block Stats", True, black), textRect)
    for i in range(len(squares)):
        squares[i]['tab'] = pygame.Rect(squaresBorder.x+2*(i+1)+i*(squaresBorder.width-8)/3, squaresBorder.y+2, (squaresBorder.width-8)/3, squaresBorder.height-4)
        if squares[i]['tab'].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (squares[i]['color'][0]+10,squares[i]['color'][1]+10,squares[i]['color'][2]+10), squares[i]['tab'])            
        else:
            pygame.draw.rect(screen, squares[i]['color'], squares[i]['tab'])
        if currentBlockTab == squares[i]['name']:
            text = font.render(squares[i]['name'][0].upper() + squares[i]['name'][1:], True, white)
        else:
            text = font.render(squares[i]['name'][0].upper() + squares[i]['name'][1:], True, black)
        textRect = text.get_rect()
        textRect.center = squares[i]['tab'].center
        screen.blit(text, textRect)  
    #what goes under tabs
    dataNames = ["m", "Vx", "Vy", "a", "Fn", "Fg", "Fnet", "m<Fnet"]
    for i in range(len(dataNames)):
        text = dataNames[i]+" = "
        for square in squares:
            if square['name'] == currentBlockTab:
                if dataNames[i] in square:
                    if dataNames[i] == 'm':
                        units = "kg"
                    elif dataNames[i][0] == 'a':
                        units = "m/s^2"
                    elif "V" in dataNames[i]:
                        units = "m/s"
                    elif "m<Fnet" == dataNames[i]:
                        units = square["FnetDir"]
                    elif "F" in dataNames[i]:
                        units = "N"
                    
                    if currentlyEditing == dataNames[i]:
                        text += newData + " " + units
                    else:   
                        text += str(square[dataNames[i]])+" "+units
                else:
                    text += "N/A"
                if currentlyEditing == dataNames[i]:
                    text = italicFont.render(text, True, black)
                else:
                    text = font.render(text, True, black)
                textRect = text.get_rect()
                textRect.topleft = (sidePanel.right+5, squaresBorder.bottom+5+25*i)
                rects[dataNames[i]] = textRect
                screen.blit(text, textRect)
    FappBorder = pygame.draw.rect(screen, black, (sidePanel.right, squaresBorder.bottom+5+25*len(dataNames), sectionW, 2))
    if currentBlockTab == 'red':
        for i in range(len(redFapps)):
            if redFapps[i] != {}:
                text = font.render("Fapp = "+str(round(redFapps[i]['total'], 2))+"N", True, redFapps[i]['color'])
                textRect = text.get_rect()
                textRect.topleft = (sidePanel.right+5, FappBorder.bottom+5+50*i)
                screen.blit(text, textRect)
                text = font.render("m<Fapp = "+str(round(math.degrees(redFapps[i]['angle']), 2))+" degrees", True, redFapps[i]['color'])
                textRect = text.get_rect()
                textRect.topleft = (sidePanel.right+5, FappBorder.bottom+30+50*i)
                screen.blit(text, textRect)
    if currentBlockTab == 'yellow':
        for i in range(len(yellowFapps)):
            if yellowFapps[i] != {}:
                text = font.render("Fapp = "+str(round(yellowFapps[i]['total'], 2))+"N", True, yellowFapps[i]['color'])
                textRect = text.get_rect()
                textRect.topleft = (sidePanel.right+5, FappBorder.bottom+5+50*i)
                screen.blit(text, textRect)
                text = font.render("m<Fapp = "+str(round(math.degrees(yellowFapps[i]['angle']), 2))+" degrees", True, yellowFapps[i]['color'])
                textRect = text.get_rect()
                textRect.topleft = (sidePanel.right+5, FappBorder.bottom+30+50*i)
                screen.blit(text, textRect)
    #ADD CHECKBOX FOR REPLACING W/ VARIABLE


def addX(surface):
    global escapeRect 
    font = pygame.font.SysFont("AnonymousPro", 24)
    escapeRect = pygame.Rect(surface.right - 20, surface.top + 5, 15, 15)
    if escapeRect.collidepoint(pygame.mouse.get_pos()):
        text = font.render("X", True, white)
        pygame.draw.rect(screen, red, escapeRect)
    else:
        text = font.render("X", True, black)
        pygame.draw.rect(screen, lightGrey, escapeRect)     
    screen.blit(text, (escapeRect.x + 2, escapeRect.y))

def tooManySquares():
    font = pygame.font.SysFont("AnonymousPro", 34)
    border = pygame.draw.rect(screen, black, (275, 285, 300, 100))
    page = pygame.draw.rect(screen, white, (277, 287, 296, 96))
    text = font.render("That's enough squares.", True, black)
    textRect = text.get_rect()
    textRect.center = pygame.Rect(277, 277, 296, 96).center
    screen.blit(text, textRect)
    text = font.render("You cannot add more.", True, black)
    screen.blit(text, (textRect.x, textRect.y + 25))
    addX(page)

addSquare = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Add Block"}
showForces = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Show Forces"}
FBDMode = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Use FBD Mode"}
showFnet = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Show Fnet"}
scaleBlocks = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Scaled Up Blocks"}
showVC = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Show Vector Comp."}
#showGrid = {"rect":pygame.Rect(0, 0, 0, 0), "text":"Show Grid"}
infoBorder = pygame.draw.circle(screen, black, (sidePanel.right-50, floor.top+15), 10)
hamBorder = pygame.draw.rect(screen , black, (0,0,0,0))
buttons = [addSquare, showForces, FBDMode, showFnet, scaleBlocks, showVC]
def buttonCreate():
    font = pygame.font.SysFont("AnonymousPro", 24)
    smallerFont = pygame.font.SysFont("AnonymousPro", 18)
    global buttons, hamBorder
    for i in range(len(buttons)):
        if (135+150*i) >= sidePanel.left:
            pygame.draw.rect(screen, black, (10+150*(i-5), 650, 125, 30))#border
            buttons[i]["rect"] = pygame.Rect(12+150*(i-5), 652, 121, 26)
        else:
            pygame.draw.rect(screen, black, (10+150*i, 700, 125, 30))#border
            buttons[i]["rect"] = pygame.Rect(12+150*i, 702, 121, 26)
        if 'Scaled' in buttons[i]['text'] or "Sized" in buttons[i]['text'] or 'Comp.' in buttons[i]['text']:
            text = smallerFont.render(buttons[i]["text"], True, black)
        else:
            text = font.render(buttons[i]["text"], True, black)
        textRect = text.get_rect()
        textRect.center = buttons[i]["rect"].center
        if buttons[i]["rect"].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, white, buttons[i]["rect"])           
        else:
            pygame.draw.rect(screen, (240, 240, 240), buttons[i]["rect"])     
        screen.blit(text, textRect)
    #info button
    infoBorder = pygame.draw.circle(screen, black, (sidePanel.right-50, floor.top+15), 10)
    if infoBorder.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, white, (sidePanel.right-50, floor.top+15), 8)
    else:
        pygame.draw.circle(screen, (240, 240, 240), (sidePanel.right-50, floor.top+15), 8)
    font = pygame.font.SysFont("AnonymousPro", 22)
    text = font.render("i", True, black)
    textRect = text.get_rect()
    textRect.center = infoBorder.center
    screen.blit(text, textRect)
    #coming soon button
    hamBorder = pygame.draw.rect(screen, black, (sidePanel.right-35, floor.top+5, 30, 29))
    screen.blit(hammerImg, (hamBorder.left+2, hamBorder.top+2))


def andUpNext():
    stuff = ["update this yo- ", "that'd be mad cool"]
    font = pygame.font.SysFont("AnonymousPro", 34)
    border = pygame.draw.rect(screen, black, (275, 285, 300, 125))
    page = pygame.draw.rect(screen, white, (277, 287, 296, 121))
    text = font.render("COMING SOON:", True, black)
    textRect = text.get_rect()
    textRect.midtop = (page.centerx, page.top+5)
    screen.blit(text, textRect)
    for i in range(len(stuff)):
        text = font.render(" - "+stuff[i], True, black)
        screen.blit(text, (textRect.x - 50, textRect.y + 25*(i+1)))
    addX(page)


def makeGrid():
    global pixPerM
    gridWidth = floor.width
    gridHeight = floor.top
    tinyFont = pygame.font.SysFont("AnonymousPro", 18)
    for i in range(round(gridWidth/pxPerM)):
        gridRect = pygame.Rect(i*pxPerM, 0, 2, gridHeight)
        pygame.draw.rect(screen, lightGrey, gridRect)
        text = tinyFont.render(str(i)+'m', True, lightGrey)
        textRect = text.get_rect()
        textRect.midtop = (gridRect.centerx, floor.bottom+2)
        screen.blit(text, textRect)
    for i in range(round(gridHeight/pxPerM)):
        gridRect = pygame.Rect(0, floor.top - i*pxPerM, gridWidth, 2)
        pygame.draw.rect(screen, lightGrey, gridRect)

#physics functions
def getRelation(square, point):#returns the values of how far a point is from the top left corner of a rect. 
    return [point[0]-square.left, point[1] - square.top]

drag = False
yDrag = False
def checkDrag():
    global drag, redSquare, redSquareLoc, yDrag, yellowSquare, yellowSquareLoc
    inRange = pygame.Rect(0, 0, floor.width, floor.top)
    dist = [0, 0]
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            if redSquare['base'].collidepoint(pygame.mouse.get_pos()):
                drag = True
                dist = getRelation(redSquare['base'], pygame.mouse.get_pos())
            elif yellowSquare['base'].collidepoint(pygame.mouse.get_pos()):
                yDrag = True
                dist = getRelation(yellowSquare['base'], pygame.mouse.get_pos())   
        else:
            drag = False
            yDrag = False
    if drag:
        if inRange.collidepoint(pygame.mouse.get_pos()):
            redSquareLoc = [pygame.mouse.get_pos()[0] - dist[0], pygame.mouse.get_pos()[1] - dist[1]]
        else:
            drag = False
    if yDrag:
        if inRange.collidepoint(pygame.mouse.get_pos()):
            yellowSquareLoc = [pygame.mouse.get_pos()[0] - dist[0], pygame.mouse.get_pos()[1] - dist[1]]
        else:
            yDrag = False
            
            
def addASquare():
    global squareCounter, popup, blitSquares
    if squareCounter == len(squares):
        squareCounter -= 1
        popup = True
    else:
        blitSquares.append(squares[squareCounter]["name"])
        squareCounter += 1
        
def writeMass(square):
    global screen
    font = pygame.font.SysFont("AnonymousPro", 24)
    newMass = str(round(square["m"], 2))+ " kg"
    text = font.render(newMass, True, black)
    textRect = text.get_rect()
    textRect.center = square["border"].center
    screen.blit(text, textRect)


tempDir = [0, 0]
def redPhysics():
    global gravityFPS, blitSquares, redSquare, redSquareLoc, tempDir, redFapps, floor, updateFapp, saveFapp, aColors
    redSquareLoc = [redSquareLoc[0], redSquareLoc[1]]
    mass = redSquare['m']
    #this bit is getting a, ax, and ay
    redSquare['a'] = round(redSquare['Fnet']/mass, 2)
    theta = math.radians(redSquare["m<Fnet"])
    acc = redSquare['a']
    redSquare['ax'] = tempDir[0]*round(acc*math.cos(theta), 2)
    redSquare['ay'] = tempDir[1]*round(acc*math.sin(theta), 2)
    #this updates Vx and Vy
    if applyForce and not drag:
        redSquare["Vx"] = round(redSquare["Vx"] + round(redSquare['ax'], 2), 2)
        redSquare["Vy"] = round(redSquare["Vy"] + round(redSquare['ay'], 2), 2)
        realVx = (redSquare["Vx"])*pxPerM/fps
        realVy = (redSquare["Vy"])*pxPerM/fps
        if -0.1 < redSquare["Vx"] < 0.1:
            redSquare["Vx"] = 0        
        if -0.1 < redSquare["Vy"] < 0.1:
            redSquare["Vy"] = 0
        redSquareLoc[0] += realVx
        redSquareLoc[1] += realVy
        if redSquareLoc[0] <= 0:
            redSquareLoc[0] = 1
            redSquare['Vx'] *= -1
        if redSquare["border"].width+redSquareLoc[0] >= sidePanel.left:
            redSquareLoc[0] = sidePanel.left-redSquare["border"].width-1
            redSquare['Vx'] *= -1
    #this checks for bottom border collision 
    if redSquare["border"].bottom > floor.top:
        redSquareLoc = [redSquareLoc[0], floor.top - redSquare["border"].height]
        redSquare["base"].bottom = redSquare["border"].bottom - 2
        redSquare["Vy"] = 0 #adapt later for bouncing? look into energy conservation, etc
    #updates square location & draws it
    if scaled:
        redSquare['border'] = pygame.Rect(redSquareLoc, (mass*5, mass*5))
        redSquare['base'] = pygame.Rect(redSquareLoc[0]+2, redSquareLoc[1]+2, redSquare['border'].width-4, redSquare['border'].width-4)       
    else:
        redSquare['border'] = pygame.Rect(redSquareLoc, (50, 50))
        redSquare['base'] = pygame.Rect(redSquareLoc[0]+2, redSquareLoc[1]+2, 46, 46)       
    pygame.draw.rect(screen, black, redSquare["border"])
    pygame.draw.rect(screen, red, redSquare["base"])
    writeMass(redSquare)
    font = pygame.font.SysFont("AnonymousPro", 24)
    base = redSquare["border"]
    #update fapps for loc:
    for dicti in redFapps:
        if dicti != {}:
            if dicti['dir'] == [2, 2]:
                dicti['basePt'] = redSquare["border"].bottomright                        
            if dicti['dir'] == [-2, 2]:
                dicti['basePt'] = redSquare["border"].bottomleft
            if dicti['dir'] == [2, -2]:
                dicti['basePt'] = redSquare["border"].topright  
            if dicti['dir'] == [-2, -2]:
                dicti['basePt'] = redSquare["border"].topleft
            dicti['endPt'] = [dicti['basePt'][0]+(dicti["x"]*dicti['dir'][0]/2), dicti['basePt'][1]+(dicti["y"]*dicti['dir'][1]/2)]
            dicti["polygon"] = ((dicti['basePt'][0], dicti['basePt'][1]-dicti['dir'][1]), (dicti['basePt'][0]-dicti['dir'][0], dicti['basePt'][1]), (dicti['endPt'][0], dicti['endPt'][1]+dicti['dir'][1]), (dicti['endPt'][0]+dicti['dir'][0], dicti['endPt'][1]))
            if dicti['basePt'][0] == redSquare['border'].left:
                dicti["textLoc"].right = dicti['basePt'][0] + (dicti['endPt'][0]-dicti['basePt'][0])//2
            else:
                dicti["textLoc"].left = dicti['endPt'][0] + (dicti['basePt'][0]-dicti['endPt'][0])//2
                
            if dicti['basePt'][1] == redSquare['border'].top:
                dicti["textLoc"].top = dicti['endPt'][1]  + (dicti['basePt'][1]-dicti['endPt'][1])//2
            else:
                dicti["textLoc"].bottom = dicti['basePt'][1] + (dicti['endPt'][1]-dicti['basePt'][1])//2
    #draws Fg
    redSquare["Fg"] = round(mass*gravity, 2)
    if forcesUp:
        redSquare["FgPolygon"] = pygame.draw.polygon(screen, black, ([base.centerx - 1, base.bottom], [base.centerx + 1, base.bottom], [base.centerx + 1, base.bottom + redSquare["Fg"]-5], [base.centerx + 3, base.bottom+redSquare["Fg"]-5],  [base.centerx + 1, base.bottom +redSquare["Fg"]], [base.centerx - 1, base.bottom + redSquare["Fg"]], [base.centerx - 3, base.bottom+redSquare["Fg"]-5], [base.centerx - 1, base.bottom + redSquare["Fg"]-5]))    
        FgText = font.render("Fg = "+str(round(redSquare["Fg"], 2))+"N", True, black)
        textRect = FgText.get_rect()
        textRect.topleft = [redSquare["FgPolygon"].x + 5, redSquare["FgPolygon"].centery]
        screen.blit(FgText, textRect)
    #starts calculating Fnet
    redSquare["Fup"] = 0
    redSquare["Fdown"] = redSquare["Fg"]
    redSquare["Fwest"] = 0
    redSquare["Feast"] = 0
    #adds Fapps to Fnet
    if not applyForce:
        for force in redFapps:
            if force != {}:
                if force["dir"][1] < 0:
                    redSquare["Fup"] += force["y"]
                if force["dir"][1] > 0:
                    redSquare["Fdown"] += force["y"]
                if force['dir'][0] < 0:
                    redSquare["Fwest"] += force["x"]
                if force['dir'][0] > 0:
                    redSquare["Feast"] += force["x"]
    #this bit does Fn and Ff
    if base.colliderect(floor) or floor.top-base.bottom <= 1:
        if redSquare["Fdown"] > redSquare["Fup"]:
            redSquare["Fn"] = (redSquare["Fdown"]-redSquare['Fup'])
            redSquare["Ff"] = round(mu*redSquare['Fn'], 2)
            #this bit does friction
            if redSquare['Vx'] > 0:
                if redSquare['Vx'] - redSquare['Ff']/mass < 0:
                    redSquare['Vx'] = 0
                    #redSquare["Fwest"] += redSquare['Vx']*mass
                else:
                    redSquare['Fwest'] += redSquare["Ff"]
            elif redSquare['Vx'] < 0:
                if redSquare['Vx'] + redSquare['Ff']/mass > 0:
                    redSquare['Vx'] = 0
                    #redSquare["Feast"] += redSquare['Vx']*mass
                else:
                    redSquare["Feast"] += redSquare["Ff"]
            if forcesUp:
                if redSquare['Vx'] > 0:
                    pygame.draw.polygon(screen, black, ((base.left, base.centery+1), (base.left, base.centery-1), (base.left-redSquare['Ff']+5, base.centery-1), (base.left-redSquare['Ff']+5, base.centery-3), (base.left-redSquare['Ff'], base.centery-1), (base.left-redSquare['Ff'], base.centery+1), (base.left-redSquare['Ff']+5, base.centery+3), (base.left-redSquare['Ff']+5, base.centery+1)))
                elif redSquare['Vx'] < 0:
                    pygame.draw.polygon(screen, black, ((base.right, base.centery+1), (base.right, base.centery-1), (base.right+redSquare['Ff']-5, base.centery-1), (base.right+redSquare['Ff']-5, base.centery-3), (base.right+redSquare['Ff'], base.centery-1), (base.right+redSquare['Ff'], base.centery+1), (base.right+redSquare['Ff']-5, base.centery+3), (base.right+redSquare['Ff']-5, base.centery+1)))
            #friction over            
            if forcesUp:
                redSquare["FnPolygon"] = pygame.draw.polygon(screen, black, ([base.centerx - 1, base.top], [base.centerx + 1, base.top], [base.centerx + 1, base.top-redSquare["Fn"]+5], [base.centerx + 3, base.top-redSquare["Fn"]+5], [base.centerx + 1, base.top-redSquare["Fn"]], [base.centerx - 1, base.top-redSquare["Fn"]], [base.centerx - 3, base.top-redSquare["Fn"]+5], [base.centerx - 1, base.top-redSquare["Fn"]+5]))
                FnText = font.render("Fn = "+str(redSquare["Fn"])+"N", True, black)
                textRect = FnText.get_rect()
                textRect.topleft = [redSquare["FnPolygon"].x + 5, redSquare["FnPolygon"].centery]
                screen.blit(FnText, textRect)
        else:
            redSquare["Fn"] = 0            
        redSquare["Fup"] += redSquare["Fn"]
    else:
        redSquare["Fn"] = 0
    #fnet direction finding:    
    if redSquare["Fdown"] ==  redSquare["Fup"] and redSquare["Fwest"] ==  redSquare["Feast"]:
        redSquare["Fnet"] = 0
        redSquare["FnetDir"] = ""
        redSquare["FnetArrowBase"] = redSquare['base'].bottomright   
    elif redSquare["Fdown"] > redSquare["Fup"]: #south > north
        if redSquare["Fwest"] > redSquare["Feast"]:
            redSquare["FnetDir"] = "SoW"
            redSquare['FnetArrowBase'] = redSquare['base'].bottomleft
        elif redSquare["Fwest"] < redSquare["Feast"]:
            redSquare["FnetDir"] = "SoE"
            redSquare['FnetArrowBase'] = redSquare['base'].bottomright        
        else:
            redSquare["FnetDir"] = "S"
            redSquare['FnetArrowBase'] = redSquare['base'].bottomleft
    elif redSquare["Fdown"] < redSquare["Fup"]: #south < north
        if redSquare["Fwest"] > redSquare["Feast"]:
            redSquare["FnetDir"] = "NoW"
            redSquare['FnetArrowBase'] = redSquare['base'].topleft
        elif redSquare["Fwest"] < redSquare["Feast"]:
            redSquare["FnetDir"] = "NoE"
            redSquare['FnetArrowBase'] = redSquare['base'].topright            
        else:
            redSquare["FnetDir"] = "N"
            redSquare['FnetArrowBase'] = redSquare['base'].topleft
    else: #south = north
        if redSquare["Fwest"] > redSquare["Feast"]:
            redSquare["FnetDir"] = "W"
            redSquare['FnetArrowBase'] = redSquare['base'].topleft
        elif redSquare["Fwest"] < redSquare["Feast"]:
            redSquare["FnetDir"] = "E"
            redSquare['FnetArrowBase'] = redSquare['base'].topright
        else:
            redSquare['FnetArrowBase'] = redSquare['base'].center
    #end of that
    #finds components of Fnet
    redSquare['Fnetx'] = abs(redSquare["Fwest"] - redSquare["Feast"])
    redSquare['Fnety'] = abs(redSquare["Fdown"] - redSquare["Fup"])
    redSquare["Fnet"] = round(math.sqrt(redSquare['Fnetx']**2 + redSquare['Fnety']**2), 2)
    #gets the angle
    if abs(redSquare["Fwest"] - redSquare["Feast"]) != 0 and abs(redSquare["Fdown"] - redSquare["Fup"]) != 0:
        redSquare["m<Fnet"] = round(math.degrees(math.atan(abs(redSquare["Fdown"] - redSquare["Fup"])/abs(redSquare["Fwest"] - redSquare["Feast"]))), 1)
    elif abs(redSquare["Fdown"] - redSquare["Fup"]) == 0:
        redSquare["m<Fnet"] = 0
    elif abs(redSquare["Fwest"] - redSquare["Feast"]) == 0:
        redSquare["m<Fnet"] = 90        
    #draws Fnet
    basePt = redSquare['FnetArrowBase']
    endPt = [0, 0]
    tempDir = [0, 0]
    if 'E' in redSquare['FnetDir']:
        endPt[0] = basePt[0] + abs(redSquare["Fwest"] - redSquare["Feast"])
        tempDir[0] = 2
    elif 'W' in redSquare['FnetDir']:
        endPt[0] = basePt[0] - abs(redSquare["Fwest"] - redSquare["Feast"])
        tempDir[0] = -2
    else:
        endPt[0] = basePt[0]
    if 'S' in redSquare['FnetDir']:
        endPt[1] = basePt[1] + abs(redSquare["Fdown"] - redSquare["Fup"])
        tempDir[1] = 2
    elif 'N' in redSquare['FnetDir']:
        endPt[1] = basePt[1] - abs(redSquare["Fdown"] - redSquare["Fup"])
        tempDir[1] = -2
    else:
        endPt[1] = basePt[1]
    if FnetArrow:            
        redSquare['FnetArrow'] = pygame.draw.polygon(screen, (255, 131, 122), ((basePt[0]+tempDir[0], basePt[1]), (basePt[0], basePt[1]+tempDir[1]), (endPt[0], endPt[1]+tempDir[1]), (endPt[0]+tempDir[0], endPt[1])))
        textRect = font.render("Fnet = " + str(redSquare['Fnet']), True, (255, 131, 122)).get_rect()
        if basePt[0] == redSquare['border'].left:
            textRect.right = basePt[0]-5 + (endPt[0]-basePt[0])//2
        else:
            textRect.left = endPt[0]+5 + (basePt[0]-endPt[0])//2
        if basePt[1] == redSquare['border'].top:
            textRect.top = endPt[1]  + (basePt[1]-endPt[1])//2
        else:
            textRect.bottom = basePt[1] + (endPt[1]-basePt[1])//2
        if basePt != redSquare['base'].center:
            screen.blit(font.render("Fnet", True, (255, 131, 122)), textRect)
    #Fapps: draws them:
    if not applyForce and forcesUp:
        for dicti in redFapps:
            if dicti != {}:
                '''
                Fapp = dicti["total"]
                dicti["x"] = Fapp*math.cos(dicti['angle'])
                dicti["y"] = Fapp*math.sin(dicti['angle'])
                dicti['endPt'] = [dicti['basePt'][0]+(dicti["x"]*dicti['dir'][0]/2), dicti['basePt'][1]+(dicti["y"]*dicti['dir'][0]/2)]
                dicti["polygon"] = ((dicti['basePt'][0], dicti['basePt'][1]-dicti['dir'][1]), (dicti['basePt'][0]-dicti['dir'][0], dicti['basePt'][1]), (dicti['endPt'][0], dicti['endPt'][1]+dicti['dir'][1]), (dicti['endPt'][0]+dicti['dir'][0], dicti['endPt'][1]))
                '''
                screen.blit(font.render("Fapp = "+str(round(dicti["total"], 2))+"N", True, dicti['color']), dicti["textLoc"])
                pygame.draw.polygon(screen, black, dicti["polygon"])
    #add new applied force
    angleFixer = 0
    direction = [0,0]
    if updateFapp:
        mousePt = pygame.mouse.get_pos()
        if mousePt[0] <= redSquare["border"].centerx:#left
            if mousePt[1] <= redSquare["border"].centery:#up
                basePt = redSquare["border"].topleft
                direction = [-2,-2]
            else:#down
                basePt = redSquare["border"].bottomleft
                direction = [-2,2]
        else:#right
            if mousePt[1] <= redSquare["border"].centery:#up
                basePt = redSquare["border"].topright
                direction = [2,-2]
            else:#down
                basePt = redSquare["border"].bottomright
                direction = [2,2]
        FappX = abs(mousePt[0]-basePt[0])//2
        FappY = abs(mousePt[1]-basePt[1])//2
        if FappX < 5:
            FappX = 0
        if FappY < 5:
            FappY = 0 
        Fapp = math.sqrt(FappX**2 + FappY**2)
        pygame.draw.polygon(screen, black, ((basePt[0], basePt[1]-direction[1]), (basePt[0]-direction[0], basePt[1]), (mousePt[0], mousePt[1]+direction[1]), (mousePt[0]+direction[0], mousePt[1])))
        textRect = font.render("Fapp = "+str(round(Fapp, 2))+"N", True, black).get_rect()
        if basePt[0] == redSquare['border'].left:
            textRect.right = basePt[0] + (mousePt[0]-basePt[0])//2
        else:
            textRect.left = mousePt[0] + (basePt[0]-mousePt[0])//2
        if basePt[1] == redSquare['border'].top:
            textRect.top = mousePt[1]  + (basePt[1]-mousePt[1])//2
        else:
            textRect.bottom = basePt[1] + (mousePt[1]-basePt[1])//2
        screen.blit(font.render("Fapp = "+str(round(Fapp, 2))+"N", True, black), textRect)    
        if saveFapp:
            for dicti in redFapps:
                if dicti == {} and Fapp >= 1:
                    dicti["dir"] = direction
                    if dicti['dir'] == [2, 2]:
                        dicti['basePt'] = redSquare["border"].bottomright                        
                    if dicti['dir'] == [-2, 2]:
                        dicti['basePt'] = redSquare["border"].bottomleft
                    if dicti['dir'] == [2, -2]:
                        dicti['basePt'] = redSquare["border"].topright  
                    if dicti['dir'] == [-2, -2]:
                        dicti['basePt'] = redSquare["border"].topleft
                    dicti["total"] = Fapp
                    dicti["x"] = FappX
                    dicti["y"] = FappY
                    dicti['endPt'] = [dicti['basePt'][0]+(dicti["x"]*dicti['dir'][0]/2), dicti['basePt'][1]+(dicti["y"]*dicti['dir'][0]/2)]
                    dicti["angle"] = math.asin(FappY/Fapp)
                    dicti["polygon"] = ((dicti['basePt'][0], dicti['basePt'][1]-dicti['dir'][1]), (dicti['basePt'][0]-dicti['dir'][0], dicti['basePt'][1]), (dicti['endPt'][0], dicti['endPt'][1]+dicti['dir'][1]), (dicti['endPt'][0]+dicti['dir'][0], dicti['endPt'][1]))
                    dicti["textLoc"] = textRect
                    dicti['color'] = aColors.pop(0)
                    if len(aColors) == 0:
                        aColors = [lightGreen, blue, purple, red, magenta, orange, teal, pink, green]
                    break
            saveFapp = False
            updateFapp = False


yTempDir = [0, 0]
def yellowPhysics():
    global gravityFPS, blitSquares, yellowSquare, yellowSquareLoc, yTempDir, yellowFapps, floor, yUpdateFapp, ySaveFapp, aColors
    yellowSquareLoc = [yellowSquareLoc[0], yellowSquareLoc[1]]
    mass = yellowSquare['m']
    #this bit is getting a, ax, and ay
    yellowSquare['a'] = round(yellowSquare['Fnet']/mass, 2)
    theta = math.radians(yellowSquare["m<Fnet"])
    acc = yellowSquare['a']
    yellowSquare['ax'] = yTempDir[0]*round(acc*math.cos(theta), 2)
    yellowSquare['ay'] = yTempDir[1]*round(acc*math.sin(theta), 2)
    #this updates Vx and Vy
    if applyForce and not yDrag:
        yellowSquare["Vx"] = round(yellowSquare["Vx"] + round(yellowSquare['ax'], 2), 2)
        yellowSquare["Vy"] = round(yellowSquare["Vy"] + round(yellowSquare['ay'], 2), 2)
        realVx = (yellowSquare["Vx"])*pxPerM/fps
        realVy = (yellowSquare["Vy"])*pxPerM/fps
        if -0.1 < yellowSquare["Vx"] < 0.1:
            yellowSquare["Vx"] = 0        
        if -0.1 < yellowSquare["Vy"] < 0.1:
            yellowSquare["Vy"] = 0
        yellowSquareLoc[0] += realVx
        yellowSquareLoc[1] += realVy
        if yellowSquareLoc[0] <= 0:
            yellowSquareLoc[0] = 1
            yellowSquare['Vx'] *= -1
        if yellowSquare["border"].width+yellowSquareLoc[0] >= sidePanel.left:
            yellowSquareLoc[0] = sidePanel.left-yellowSquare["border"].width-1
            yellowSquare['Vx'] *= -1
    #this checks for bottom border collision
    if yellowSquare["border"].bottom > floor.top:
        yellowSquareLoc = [yellowSquareLoc[0], floor.top - yellowSquare["border"].height]
        yellowSquare["base"].bottom = yellowSquare["border"].bottom - 2
        yellowSquare["Vy"] = 0 #adapt later for bouncing? look into energy conservation, etc
    #updates square location & draws it
    if scaled:
        yellowSquare['border'] = pygame.Rect(yellowSquareLoc, (mass*5, mass*5))
        yellowSquare['base'] = pygame.Rect(yellowSquareLoc[0]+2, yellowSquareLoc[1]+2, yellowSquare['border'].width-4, yellowSquare['border'].width-4)       
    else:
        yellowSquare["base"] = pygame.Rect(yellowSquareLoc[0]+2, yellowSquareLoc[1]+2, 46, 46)
        yellowSquare["border"] = pygame.Rect(yellowSquareLoc, (50, 50))               
    pygame.draw.rect(screen, black, yellowSquare["border"])
    pygame.draw.rect(screen, yellow, yellowSquare["base"])
    writeMass(yellowSquare)
    font = pygame.font.SysFont("AnonymousPro", 24)
    base = yellowSquare["border"]
    #update fapps for loc:
    for dicti in yellowFapps:
        if dicti != {}:
            if dicti['dir'] == [2, 2]:
                dicti['basePt'] = yellowSquare["border"].bottomright                        
            if dicti['dir'] == [-2, 2]:
                dicti['basePt'] = yellowSquare["border"].bottomleft
            if dicti['dir'] == [2, -2]:
                dicti['basePt'] = yellowSquare["border"].topright  
            if dicti['dir'] == [-2, -2]:
                dicti['basePt'] = yellowSquare["border"].topleft
            dicti['endPt'] = [dicti['basePt'][0]+(dicti["x"]*dicti['dir'][0]/2), dicti['basePt'][1]+(dicti["y"]*dicti['dir'][1]/2)]
            dicti["polygon"] = ((dicti['basePt'][0], dicti['basePt'][1]-dicti['dir'][1]), (dicti['basePt'][0]-dicti['dir'][0], dicti['basePt'][1]), (dicti['endPt'][0], dicti['endPt'][1]+dicti['dir'][1]), (dicti['endPt'][0]+dicti['dir'][0], dicti['endPt'][1]))
            if dicti['basePt'][0] == yellowSquare['border'].left:
                dicti["textLoc"].right = dicti['basePt'][0] + (dicti['endPt'][0]-dicti['basePt'][0])//2
            else:
                dicti["textLoc"].left = dicti['endPt'][0] + (dicti['basePt'][0]-dicti['endPt'][0])//2
                
            if dicti['basePt'][1] == yellowSquare['border'].top:
                dicti["textLoc"].top = dicti['endPt'][1]  + (dicti['basePt'][1]-dicti['endPt'][1])//2
            else:
                dicti["textLoc"].bottom = dicti['basePt'][1] + (dicti['endPt'][1]-dicti['basePt'][1])//2
    #draws Fg
    yellowSquare["Fg"] = round(mass*gravity, 2)
    if forcesUp:
        yellowSquare["FgPolygon"] = pygame.draw.polygon(screen, black, ([base.centerx - 1, base.bottom], [base.centerx + 1, base.bottom], [base.centerx + 1, base.bottom + yellowSquare["Fg"]-5], [base.centerx + 3, base.bottom+yellowSquare["Fg"]-5],  [base.centerx + 1, base.bottom +yellowSquare["Fg"]], [base.centerx - 1, base.bottom + yellowSquare["Fg"]], [base.centerx - 3, base.bottom+yellowSquare["Fg"]-5], [base.centerx - 1, base.bottom + yellowSquare["Fg"]-5]))    
        FgText = font.render("Fg = "+str(round(yellowSquare["Fg"], 2))+"N", True, black)
        textRect = FgText.get_rect()
        textRect.topleft = [yellowSquare["FgPolygon"].x + 5, yellowSquare["FgPolygon"].centery]
        screen.blit(FgText, textRect)
    #starts calculating Fnet
    yellowSquare["Fup"] = 0
    yellowSquare["Fdown"] = yellowSquare["Fg"]
    yellowSquare["Fwest"] = 0
    yellowSquare["Feast"] = 0
    #adds Fapps to Fnet
    if not applyForce:
        for force in yellowFapps:
            if force != {}:
                if force["dir"][1] < 0:
                    yellowSquare["Fup"] += force["y"]
                if force["dir"][1] > 0:
                    yellowSquare["Fdown"] += force["y"]
                if force['dir'][0] < 0:
                    yellowSquare["Fwest"] += force["x"]
                if force['dir'][0] > 0:
                    yellowSquare["Feast"] += force["x"]
    #this bit does Fn and Ff
    if base.colliderect(floor) or floor.top-base.bottom <= 1:
        if yellowSquare["Fdown"] > yellowSquare["Fup"]:
            yellowSquare["Fn"] = (yellowSquare["Fdown"]-yellowSquare['Fup'])
            yellowSquare["Ff"] = round(mu*yellowSquare['Fn'], 2)
            #this bit does friction
            if yellowSquare['Vx'] > 0:
                if yellowSquare['Vx'] - yellowSquare['Ff']/mass < 0:
                    yellowSquare['Vx'] = 0
                else:
                    yellowSquare['Fwest'] += yellowSquare["Ff"]
            elif yellowSquare['Vx'] < 0:
                if yellowSquare['Vx'] + yellowSquare['Ff']/mass > 0:
                    yellowSquare['Vx'] = 0
                else:
                    yellowSquare["Feast"] += yellowSquare["Ff"]
            if forcesUp:
                if yellowSquare['Vx'] > 0:
                    pygame.draw.polygon(screen, black, ((base.left, base.centery+1), (base.left, base.centery-1), (base.left-yellowSquare['Ff']+5, base.centery-1), (base.left-yellowSquare['Ff']+5, base.centery-3), (base.left-yellowSquare['Ff'], base.centery-1), (base.left-yellowSquare['Ff'], base.centery+1), (base.left-yellowSquare['Ff']+5, base.centery+3), (base.left-yellowSquare['Ff']+5, base.centery+1)))
                elif yellowSquare['Vx'] < 0:
                    pygame.draw.polygon(screen, black, ((base.right, base.centery+1), (base.right, base.centery-1), (base.right+yellowSquare['Ff']-5, base.centery-1), (base.right+yellowSquare['Ff']-5, base.centery-3), (base.right+yellowSquare['Ff'], base.centery-1), (base.right+yellowSquare['Ff'], base.centery+1), (base.right+yellowSquare['Ff']-5, base.centery+3), (base.right+yellowSquare['Ff']-5, base.centery+1)))
            #friction over            
            if forcesUp:
                yellowSquare["FnPolygon"] = pygame.draw.polygon(screen, black, ([base.centerx - 1, base.top], [base.centerx + 1, base.top], [base.centerx + 1, base.top-yellowSquare["Fn"]+5], [base.centerx + 3, base.top-yellowSquare["Fn"]+5], [base.centerx + 1, base.top-yellowSquare["Fn"]], [base.centerx - 1, base.top-yellowSquare["Fn"]], [base.centerx - 3, base.top-yellowSquare["Fn"]+5], [base.centerx - 1, base.top-yellowSquare["Fn"]+5]))
                FnText = font.render("Fn = "+str(yellowSquare["Fn"])+"N", True, black)
                textRect = FnText.get_rect()
                textRect.topleft = [yellowSquare["FnPolygon"].x + 5, yellowSquare["FnPolygon"].centery]
                screen.blit(FnText, textRect)
        else:
            yellowSquare["Fn"] = 0            
        yellowSquare["Fup"] += yellowSquare["Fn"]
    else:
        yellowSquare["Fn"] = 0
    #fnet direction finding:    
    if yellowSquare["Fdown"] ==  yellowSquare["Fup"] and yellowSquare["Fwest"] ==  yellowSquare["Feast"]:
        yellowSquare["Fnet"] = 0
        yellowSquare["FnetDir"] = ""
        yellowSquare["FnetArrowBase"] = yellowSquare['base'].bottomright   
    elif yellowSquare["Fdown"] > yellowSquare["Fup"]: #south > north
        if yellowSquare["Fwest"] > yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "SoW"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].bottomleft
        elif yellowSquare["Fwest"] < yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "SoE"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].bottomright        
        else:
            yellowSquare["FnetDir"] = "S"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].bottomleft
    elif yellowSquare["Fdown"] < yellowSquare["Fup"]: #south < north
        if yellowSquare["Fwest"] > yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "NoW"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].topleft
        elif yellowSquare["Fwest"] < yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "NoE"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].topright            
        else:
            yellowSquare["FnetDir"] = "N"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].topleft
    else: #south = north
        if yellowSquare["Fwest"] > yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "W"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].topleft
        elif yellowSquare["Fwest"] < yellowSquare["Feast"]:
            yellowSquare["FnetDir"] = "E"
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].topright
        else:
            yellowSquare['FnetArrowBase'] = yellowSquare['base'].center
    #end of that
    #finds components of Fnet
    yellowSquare['Fnetx'] = abs(yellowSquare["Fwest"] - yellowSquare["Feast"])
    yellowSquare['Fnety'] = abs(yellowSquare["Fdown"] - yellowSquare["Fup"])
    yellowSquare["Fnet"] = round(math.sqrt(yellowSquare['Fnetx']**2 + yellowSquare['Fnety']**2), 2)
    #gets the angle
    if abs(yellowSquare["Fwest"] - yellowSquare["Feast"]) != 0 and abs(yellowSquare["Fdown"] - yellowSquare["Fup"]) != 0:
        yellowSquare["m<Fnet"] = round(math.degrees(math.atan(abs(yellowSquare["Fdown"] - yellowSquare["Fup"])/abs(yellowSquare["Fwest"] - yellowSquare["Feast"]))), 1)
    elif abs(yellowSquare["Fdown"] - yellowSquare["Fup"]) == 0:
        yellowSquare["m<Fnet"] = 0
    elif abs(yellowSquare["Fwest"] - yellowSquare["Feast"]) == 0:
        yellowSquare["m<Fnet"] = 90        
    #draws Fnet
    basePt = yellowSquare['FnetArrowBase']
    endPt = [0, 0]
    yTempDir = [0, 0]
    if 'E' in yellowSquare['FnetDir']:
        endPt[0] = basePt[0] + abs(yellowSquare["Fwest"] - yellowSquare["Feast"])
        yTempDir[0] = 2
    elif 'W' in yellowSquare['FnetDir']:
        endPt[0] = basePt[0] - abs(yellowSquare["Fwest"] - yellowSquare["Feast"])
        yTempDir[0] = -2
    else:
        endPt[0] = basePt[0]
    if 'S' in yellowSquare['FnetDir']:
        endPt[1] = basePt[1] + abs(yellowSquare["Fdown"] - yellowSquare["Fup"])
        yTempDir[1] = 2
    elif 'N' in yellowSquare['FnetDir']:
        endPt[1] = basePt[1] - abs(yellowSquare["Fdown"] - yellowSquare["Fup"])
        yTempDir[1] = -2
    else:
        endPt[1] = basePt[1]
    if FnetArrow:            
        yellowSquare['FnetArrow'] = pygame.draw.polygon(screen, (255, 131, 122), ((basePt[0]+yTempDir[0], basePt[1]), (basePt[0], basePt[1]+yTempDir[1]), (endPt[0], endPt[1]+yTempDir[1]), (endPt[0]+yTempDir[0], endPt[1])))
        textRect = font.render("Fnet = " + str(yellowSquare['Fnet']), True, (255, 131, 122)).get_rect()
        if basePt[0] == yellowSquare['border'].left:
            textRect.right = basePt[0]-5 + (endPt[0]-basePt[0])//2
        else:
            textRect.left = endPt[0]+5 + (basePt[0]-endPt[0])//2
        if basePt[1] == yellowSquare['border'].top:
            textRect.top = endPt[1]  + (basePt[1]-endPt[1])//2
        else:
            textRect.bottom = basePt[1] + (endPt[1]-basePt[1])//2
        if basePt != yellowSquare['base'].center:
            screen.blit(font.render("Fnet", True, (255, 131, 122)), textRect)
    #resets Fapps or draws them:
    if not applyForce and forcesUp:
        for dicti in yellowFapps:
            if dicti != {}:
                screen.blit(font.render("Fapp = "+str(round(dicti["total"], 2))+"N", True, dicti['color']), dicti["textLoc"])
                pygame.draw.polygon(screen, black, dicti["polygon"])
    #add new applied force
    angleFixer = 0
    direction = [0,0]
    if yUpdateFapp:
        mousePt = pygame.mouse.get_pos()
        if mousePt[0] <= yellowSquare["border"].centerx:#left
            if mousePt[1] <= yellowSquare["border"].centery:#up
                basePt = yellowSquare["border"].topleft
                direction = [-2,-2]
            else:#down
                basePt = yellowSquare["border"].bottomleft
                direction = [-2,2]
        else:#right
            if mousePt[1] <= yellowSquare["border"].centery:#up
                basePt = yellowSquare["border"].topright
                direction = [2,-2]
            else:#down
                basePt = yellowSquare["border"].bottomright
                direction = [2,2]
        FappX = abs(mousePt[0]-basePt[0])//2
        FappY = abs(mousePt[1]-basePt[1])//2
        if FappX < 5:
            FappX = 0
        if FappY < 5:
            FappY = 0 
        Fapp = math.sqrt(FappX**2 + FappY**2)
        pygame.draw.polygon(screen, black, ((basePt[0], basePt[1]-direction[1]), (basePt[0]-direction[0], basePt[1]), (mousePt[0], mousePt[1]+direction[1]), (mousePt[0]+direction[0], mousePt[1])))
        textRect = font.render("Fapp = "+str(round(Fapp, 2))+"N", True, black).get_rect()
        if basePt[0] == yellowSquare['border'].left:
            textRect.right = basePt[0] + (mousePt[0]-basePt[0])//2
        else:
            textRect.left = mousePt[0] + (basePt[0]-mousePt[0])//2
        if basePt[1] == yellowSquare['border'].top:
            textRect.top = mousePt[1]  + (basePt[1]-mousePt[1])//2
        else:
            textRect.bottom = basePt[1] + (mousePt[1]-basePt[1])//2
        screen.blit(font.render("Fapp = "+str(round(Fapp, 2))+"N", True, black), textRect)    
        if ySaveFapp:
            for dicti in yellowFapps:
                if dicti == {} and Fapp >= 1:
                    dicti["dir"] = direction
                    if dicti['dir'] == [2, 2]:
                        dicti['basePt'] = yellowSquare["border"].bottomright                        
                    if dicti['dir'] == [-2, 2]:
                        dicti['basePt'] = yellowSquare["border"].bottomleft
                    if dicti['dir'] == [2, -2]:
                        dicti['basePt'] = yellowSquare["border"].topright  
                    if dicti['dir'] == [-2, -2]:
                        dicti['basePt'] = yellowSquare["border"].topleft
                    dicti["total"] = Fapp
                    dicti["x"] = FappX
                    dicti["y"] = FappY
                    dicti['endPt'] = [dicti['basePt'][0]+(dicti["x"]*dicti['dir'][0]/2), dicti['basePt'][1]+(dicti["y"]*dicti['dir'][0]/2)]
                    dicti["angle"] = math.asin(FappY/Fapp)
                    dicti["polygon"] = ((dicti['basePt'][0], dicti['basePt'][1]-dicti['dir'][1]), (dicti['basePt'][0]-dicti['dir'][0], dicti['basePt'][1]), (dicti['endPt'][0], dicti['endPt'][1]+dicti['dir'][1]), (dicti['endPt'][0]+dicti['dir'][0], dicti['endPt'][1]))
                    dicti["textLoc"] = textRect
                    dicti['color'] = aColors.pop(0)
                    if len(aColors) == 0:
                        aColors = [lightGreen, blue, purple, red, magenta, orange, teal, pink, green]
                    break
            ySaveFapp = False
            yUpdateFapp = False


def imperfectCollisions(A, B):
    global redSquare, yellowSquare, tealSquare, Kpercent
    mA = A['m']
    mB = B['m']
    aVxi = A['Vx']
    bVxi = B['Vx']
    KE = Kpercent*((0.5*mA*(aVxi**2))+(0.5*mB*(bVxi**2)))
    Pi = (mA*aVxi) + (mB*bVxi)
    l = mB+1
    m = -2*Pi
    n = (-2*(mB*KE) + -1*((Pi)**2))/mA 
    neg4ac = -1*4*l*n
    discriminant = math.sqrt((m)**2 + neg4ac )
    aVxf = (-1*m + discriminant)/(2*l)
    bVxf = (Pi - (mA*aVxf))/mB
    A['Vx'] = aVxf
    B['Vx'] = bVxf

def perfectCollisions(A, B): #perfectly inelastic --- WORK IN PROGRESS
    # finding Vx 
    Vxia = A["Vx"]
    Vxib = B["Vx"]
    xai = A['border'].left
    xbi = B['border'].left
    mA = A['m']
    mB = B['m']
    Pi = (mA*Vxia) + (mB*Vxib)
    Vxf = Pi/(mA + mB)
    A["Vx"] = Vxf
    B['Vx'] = Vxf
    
            
#main
while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.toggle_fullscreen()
     
            if currentlyEditing == "mu":
                if event.key == pygame.K_BACKSPACE:
                    newData = newData[:-1]
                elif event.key == pygame.K_RETURN:
                    saveMu()
                else:
                    newData += event.unicode
            elif currentlyEditing != "":
                if event.key == pygame.K_BACKSPACE:
                    newData = newData[:-1]
                elif event.key == pygame.K_RETURN:
                    saveNotMuData()
                else:
                    newData += event.unicode                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if muTextRect.collidepoint(pygame.mouse.get_pos()):
                currentlyEditing = 'mu'
            for i in range(len(rects)):
                if rects[dataNames[i]].collidepoint(pygame.mouse.get_pos()) and dataNames[i] not in ('Fg', 'Fn' ):
                    currentlyEditing = dataNames[i]          
            if escapeRect.collidepoint(pygame.mouse.get_pos()):
                popup = False
                infoGoesUp = False
                displayComingSoon = False
            if addSquare["rect"].collidepoint(pygame.mouse.get_pos()):
                addASquare()
            if FBDMode["rect"].collidepoint(pygame.mouse.get_pos()):
                if applyForce:
                    applyForce = False
                    FBDMode["text"] = "Apply Forces"
                else:
                    FBDMode["text"] = "Use FBD Mode"
                    applyForce = True
                    redFapps = [{}, {}, {}]
                    yellowFapps = [{}, {}, {}]
            if showForces["rect"].collidepoint(pygame.mouse.get_pos()):
                if forcesUp:
                    forcesUp = False
                    showForces["text"] = "Show Forces"
                else:
                    showForces["text"] = "Hide Forces"
                    forcesUp = True
            if showVC["rect"].collidepoint(pygame.mouse.get_pos()):
                if showVCbool:
                    showVCbool = False
                    showVC["text"] = "Show Vector Comp."
                else:
                    showVC["text"] = "Hide Vector Comp."
                    showVCbool = True
            if scaleBlocks["rect"].collidepoint(pygame.mouse.get_pos()):
                if scaled:
                    scaled = False
                    scaleBlocks["text"] = "Scaled Up Blocks"
                else:
                    scaleBlocks["text"] = "Same Sized Blocks"
                    scaled = True
            if infoBorder.collidepoint(pygame.mouse.get_pos()):
                if infoGoesUp:
                    infoGoesUp = False
                else:
                    infoGoesUp = True
            if hamBorder.collidepoint(pygame.mouse.get_pos()):
                if displayComingSoon:
                    displayComingSoon = False
                else:
                    displayComingSoon = True                                    
            if showFnet["rect"].collidepoint(pygame.mouse.get_pos()):
                if FnetArrow:
                    showFnet["text"] = "Show Fnet"
                    FnetArrow = False
                else:
                    FnetArrow = True
                    showFnet["text"] = "Hide Fnet"
            if cE.collidepoint(pygame.mouse.get_pos()):
                Kpercent = float(1.0)
            if inE.collidepoint(pygame.mouse.get_pos()):
                Kpercent = 0.5
            if pInE.collidepoint(pygame.mouse.get_pos()):
                Kpercent = float(0.0)
            if event.button == 3 and redSquare["border"].collidepoint(pygame.mouse.get_pos()) and forcesUp and not applyForce:
                saveFapp = False
                updateFapp = True
            if event.button == 3 and yellowSquare["border"].collidepoint(pygame.mouse.get_pos()) and forcesUp and not applyForce:
                ySaveFapp = False
                yUpdateFapp = True
            for tab in tabs:
                if tab.collidepoint(pygame.mouse.get_pos()):
                    currentTab = tab
            for square in squares:
                if square['tab'].collidepoint(pygame.mouse.get_pos()) and currentTab == dataTab:
                    currentBlockTab = square['name']
            if not startedYet and startButton.collidepoint(pygame.mouse.get_pos()):
                startedYet = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                saveFapp = True
                ySaveFapp = True
    if gridUp:
        makeGrid()   
    pygame.draw.rect(screen, black, floor)#make floor
    makeTabs()
    checkDrag()
    buttonCreate()#make buttons
    


    if 'red' in blitSquares:
        redPhysics()    
    if 'yellow' in blitSquares:
        yellowPhysics()    
    if Kpercent != 0 and redSquare['border'].colliderect(yellowSquare['border']):
        imperfectCollisions(redSquare, yellowSquare)
    if Kpercent == 0 and redSquare['border'].colliderect(yellowSquare['border']):
        perfectCollisions(redSquare, yellowSquare)
    if showVCbool:
        vectorComponents()
    if displayComingSoon:
        andUpNext()    
    if popup:
        tooManySquares()
    if infoGoesUp:
        infoPanel()
    if not startedYet:
        createCover()

    #fin
    pygame.display.update()
    pygame.time.delay(50)
    clock.tick()
