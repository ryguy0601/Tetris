'''
tetris
ryan cuccurullo
'''

from random import choice, randint

import os
os.system('cls')  # clears terminal

WIDTH, HEIGHT = 550, 650
columns = 10
rows = 19
grid = [[0 for _ in range(columns)] for _ in range(rows)]
tile = 31
frame = 500
centerX = (WIDTH-tile*columns)/2
centerY = (HEIGHT-tile*(rows+2))+3
shapes = ["l",  "j",  "i", "o",  "z",  "s", "t"]
nextPeice = False
l = []
l1 = []
score = 0
check = []
go = False
gearLook = 0
showMenu = False
dead = False
amount = 0


# classes
class switch:
    def __init__(self, x, y, w, onCol=(0, 255, 0), offCol=200, state="off"):
        self.x = x
        self.y = y
        self.w = w
        self.h = self.w/2
        self.state = state

        if str(onCol)[0] in ['[', '(']:
            self.onCol = color(*onCol)
        else:
            self.onCol = color(onCol, onCol, onCol)

        self.offCol = color(offCol)
        if str(offCol)[0] in ['[', '(']:
            self.offCol = color(*offCol)

    def show(self):
        noStroke()
        fill(self.offCol)
        if len(self.state) == 2:
            fill(self.onCol)

        arc(self.x, self.y, self.w/3, self.h, HALF_PI, HALF_PI*3)
        rect(self.x, self.y-self.h/2, self.w/2, self.h)
        arc(self.x+self.w/2, self.y, self.w/3, self.h, -HALF_PI, HALF_PI)

        fill(0)
        if self.state == "on":
            ellipse(self.x+self.w-self.h-self.w/10, self.y, self.h-2, self.h-2)
        else:
            ellipse(self.x+self.w/10, self.y, self.h-2, self.h-2)

    def getState(self):
        return True if len(self.state) == 2 else False

    def mouseOn(self):
        x, y, w, h = [self.x, self.y-self.h/2, self.w/2, self.h]
        if (x <= mouseX <= x + w and
                y <= mouseY <= y + h):
            return True
        dist = ((mouseX - self.x)**2 + (mouseY - self.y)**2)**.5
        if dist <= self.w/3-self.w/(20/3):
            return True

        dist = ((mouseX - (self.x+self.w/2))**2 + (mouseY - self.y)**2)**.5
        if dist <= self.w/3-self.w/(20/3):
            return True
        return False

    def change(self):
        if len(self.state) == 2:
            self.state = 'off'
        else:
            self.state = 'on'


class slider:
    def __init__(self, x, y, w, txt='', col1=100, col2=0, value=None, Min=0, Max=255, horiz=True):
        self.x = x
        self.y = y
        self.w = w
        self.txt = txt
        self.value = value
        if self.value == None:
            self.value = Min
        self.col1 = color(col1)
        self.col2 = color(col2)
        self.Min = Min
        self.Max = Max
        self.horiz = horiz
        if self.horiz:
            percent = float((self.value-self.Min))/(self.Max-self.Min)
            self.circleX = percent * (self.Max-self.x)+self.x
        else:
            percent = float((self.value-self.Min))/(self.Max-self.Min)
            self.circleY = percent * (self.Max-self.y)+self.y

        self.isShow = False
        if self.horiz:
            self.showWhatsChanging = True
            self.showVal = True
        else:
            self.showWhatsChanging = False
            self.showVal = True

    def hide(self):
        self.isShow = False

    def show(self):
        self.isShow = True
        strokeWeight(10)
        stroke(self.col1)

        # the slide bar itself
        if self.horiz:
            line(self.x, self.y, self.x+self.w, self.y)
        else:
            line(self.x, self.y, self.x, self.w+self.y)

        strokeWeight(1)
        fill(self.col2)
        # draws circle small if mouse not on larger if mouse is on it

        if self.horiz:
            if self.mouseOn():
                ellipse(self.circleX, self.y, 20, 20)
            else:
                ellipse(self.circleX, self.y, 10, 10)
        else:
            if self.mouseOn():
                ellipse(self.x, self.circleY, 20, 20)
            else:
                ellipse(self.x, self.circleY, 10, 10)

        fill(255)
        # says whats being changed by the slider
        if self.showWhatsChanging:
            text(self.txt, self.x-.5*(textWidth(self.txt))-10, self.y+5)

        if self.showVal:
            # box around value on the right
            fill(self.col2)
            rect(self.x+self.w+17, self.y-10, 40, 20)

            # says what the value of the slider is
            fill(255)
            textAlign(CENTER)
            text(int(self.value), self.x+self.w+36, self.y+5)

        self.mouseOnAndPressed()

    def setVal(self, x):
        if self.horiz:
            self.circleX = x
            if self.circleX < self.x:
                self.circleX = self.x
            if self.circleX > self.x+self.w:
                self.circleX = self.x+self.w

            percent = round(x-self.x)/float((self.w))
            self.value = (percent * (self.Max - self.Min)) + self.Min
        else:
            self.circleY = x
            if self.circleY < self.y:
                self.circleY = self.y
            if self.circleY > self.y+self.w:
                self.circleY = self.y+self.w

            percent = round(x-self.y)/float((self.w))
            self.value = (percent * (self.Max - self.Min)) + self.Min

    def changeVal(self, x):
        self.value += x
        if self.value < self.Min:
            self.value = self.Min
        if self.value > self.Max:
            self.value = self.Max
        percent = (self.value-self.Min)/(self.Max-self.Min)
        if self.horiz:
            self.circleX = percent*self.w+self.x
        else:
            self.circleY = percent*self.w+self.y

    def mouseOn(self):
        if (self.y-5 <= mouseY <= self.y+5 and
                self.x <= mouseX <= self.x+self.w and self.isShow and self.horiz):
            return True
        if (self.y <= mouseY <= self.y+self.w and
                self.x-5 <= mouseX <= self.x+5 and self.isShow and not self.horiz):
            return True

    def mouseOnAndPressed(self):
        if self.mouseOn() and mousePressed:
            if self.horiz:
                self.setVal(mouseX)
            else:
                self.setVal(mouseY)

    def mouseOnAndKeyPressed(self):
        if self.mouseOn():
            if self.horiz:
                if keyCode == LEFT:
                    self.changeVal(-1)
                if keyCode == RIGHT:
                    self.changeVal(1)
            else:
                if keyCode == UP:
                    self.changeVal(-1)
                if keyCode == DOWN:
                    self.changeVal(1)

    def getVal(self):
        return self.value

    def showWhatsChanging(self, x):
        self.showWhatsChanging = x


class button:
    def __init__(self, x, y, w, h, txt="", txtPos=1, backCol=0, forCol=255):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.txt = txt
        self.txtSize = 12
        self.txtPos = txtPos
        self.backCol = color(backCol)
        self.forCol = color(forCol)
        self.isShow = False

    def show(self):
        self.isShow = True
        fill(self.backCol)
        rect(self.x, self.y, self.w, self.h)
        # print self.x,self.y
        self.showTxt()

        # darkens button
        if self.mouseOn():
            fill(34, 155)
            rect(self.x, self.y, self.w, self.h)

    def hide(self):
        self.isShow = False

    def showTxt(self):
        """
        1 is centered in the button
        2 is to the right the button
        3 is to the left the button
        4 is below the button
        5 is above the button
        """
        centerX = (self.w+self.x)-(textWidth(self.txt)/2)
        centerY = self.h/2+self.y
        if self.txtPos == 1:
            x = centerX
            y = centerY
            textAlign(CENTER, CENTER)
        elif self.txtPos == 2:
            x = self.x+self.w+textWidth(self.txt)+5
            y = centerY
            textAlign(RIGHT, CENTER)
        elif self.txtPos == 3:
            x = self.x-(textWidth(self.txt)+5)
            y = centerY
            textAlign(LEFT, CENTER)
        elif self.txtPos == 4:
            x = centerX
            y = self.y+self.h+(self.txtSize)+5
            textAlign(CENTER, BOTTOM)
        else:  # self.txtPos == 5:
            x = centerX
            y = self.y-((self.txtSize)+5)
            textAlign(CENTER, TOP)

        # print x,y
        fill(self.forCol)
        textSize(self.txtSize)
        text(self.txt, x, y)

    def setTxtSize(self, size):
        self.txtSize = size

    def mouseOn(self):
        if (self.y <= mouseY <= self.y+self.h and
                self.x <= mouseX <= self.x+self.w and self.isShow):
            return True


class popUp:
    def __init__(self, x=None, y=None, w=None, h=None, backCol=155, forCol=255):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        if self.w == None:
            self.w = WIDTH*.55

        if self.h == None:
            self.h = HEIGHT*.35
        if self.x == None:
            self.x = (WIDTH/2)-(self.w/2)  # centers x
        if self.y == None:
            self.y = (HEIGHT/2)-(self.h/2)  # center y

        self.txt = {}
        self.backCol = color(backCol)
        self.forCol = color(forCol)
        self.isShow = False
        self.editSet = [0, 0]
        self.reset = button(x=self.x+self.w/2-40, y=self.y+self.h-40,
                            w=80, h=25, txt="Reset Settings", txtPos=1, backCol=50)
        self.scroll = slider(x=self.x+self.w+15, y=self.y+10,
                             w=self.h-25, horiz=False, Max=150)
        self.pressKey = False

    def hide(self):
        self.isShow = False

    def show(self):
        self.isShow = True
        fill(self.backCol, 100)
        stroke(0)
        strokeWeight(1)
        rect(self.x, self.y, self.w, self.h)
        self.showTxt()
        # draws reset button
        self.reset.show()
        self.drawX()
        self.scroll.show()

    def drawX(self):
        textAlign(BASELINE)
        fill(255, 0, 0)
        textSize(20)
        text('x', self.x+self.w-15-textWidth("x"), self.y+20)
        # highlights 'x'
        if self.isOnX():
            fill(34, 50)
            rect(self.x+self.w-35, self.y+5, 30, 20)
        if self.pressKey:
            t = "Press a key to select"
            textSize(20)
            fill(255)
            text(t, self.x+self.w/2-textWidth(t)/2, self.y+20)

    def switchCheck(self):
        for i in self.txt.values():
            if isinstance(i[0], switch):
                if i[0].mouseOn():
                    i[0].change()

    def showTxt(self):
        # draws all text with a vertical space of 20
        for i, j in self.txt.items():
            textSize(12)
            textAlign(BASELINE)
            fill(self.forCol)

            xPos = self.x+5
            if not j[1]:
                xPos = self.x+self.w/2-textWidth(i)/2
            y = self.y+((j[2]+2)*20)+5-self.scroll.getVal()

            if self.y+38 < y < self.y+self.h-40:

                text(i, xPos, y)
                if isinstance(j[0], switch):
                    self.txt[i] = [
                        switch(x=self.x+self.w-40, y=y, w=35, state=j[0].state), j[1], j[2]]
                    self.txt[i][0].show()
                else:
                    text(j[0], self.x+self.w-15-textWidth(j[0]), y)

                # highlights rows
                if (y-15 <= mouseY <= y+5 and j[0] != 0 and not isinstance(j[0], switch) and
                        self.x <= mouseX <= self.x+self.w and self.isShow and j[1]):
                    fill(34, 50)
                    rect(self.x, y-12, self.w, 15)

        # highlights 'x'
        if self.isOnX():
            fill(34, 50)
            rect(self.x+self.w-35, self.y+5, 30, 20)

    def clearSettings(self):  # clears keybiend dictionary
        self.txt = {}

    def addTxt(self, setting, key="", keyCode=0, z=True):  # pretty self explanitoyry
        self.txt[setting] = [key, z, len(self.txt), keyCode]

    def editTxt(self, setting, key, keyCode):
        # makes it so thatif you press the key that is alredy there it makes it none
        if self.txt[setting] == [key, self.txt[setting][1], self.txt[setting][2], keyCode]:
            self.txt[setting] = ["None", self.txt[setting]
                                 [1], self.txt[setting][2], 0]
        else:
            self.txt[setting] = [key, self.txt[setting]
                                 [1], self.txt[setting][2], keyCode]

        # makes so nothing can have the same key bind
        for i in self.txt:
            if self.txt[setting][0] == self.txt[i][0] and i != setting:
                self.txt[i] = ["None", self.txt[i][1], self.txt[i][2], 0]

    def isOverTxt(self):
        for i, j in self.txt.items():

            xPos = self.x+5
            if not j[1]:
                xPos = self.x+self.w/2-textWidth(i)/2
            y = self.y+((j[2]+2)*20)+5-self.scroll.getVal()

            if (y-15 <= mouseY <= y+5 and j[0] != 0 and not isinstance(j[0], switch) and
                    self.x <= mouseX <= self.x+self.w and self.isShow and j[1]) and (
                    self.y+38 < y < self.y+self.h-40):
                self.pressKey = True
                self.editSet = [True, i]
                return
        self.editSet = [False, 0]
        return

    def isOnX(self):  # to exit pop up
        if (self.y+5 <= mouseY <= self.y+25 and
                self.x+self.w-35 <= mouseX <= self.x+self.w and self.isShow):
            return True

    def getKeyCodes(self):
        x = []
        for j,i in self.txt.items():
            if i[1]:
                if isinstance(i[0], switch):
                    x.append((j,i[0].getState()))
                else:
                    x.append((j,i[3]))
        return x

    def setKeys(self, x, y):
        if self.editSet[0]:
            self.pressKey = False

            # checks for the keys that dont render properly and puts text in there place
            if x == LEFT:
                pop.editTxt(self.editSet[1], "Left Arrow", LEFT)
            elif x == RIGHT:
                pop.editTxt(self.editSet[1], "Right Arrow", RIGHT)
            elif x == UP:
                pop.editTxt(self.editSet[1], "Up Arrow", UP)
            elif x == DOWN:
                pop.editTxt(self.editSet[1], "Down Arrow", DOWN)
            elif x == 32:
                pop.editTxt(self.editSet[1], "Space", 32)
            elif x == 10:
                pop.editTxt(self.editSet[1], "Enter", 10)
            elif x == 16:
                pop.editTxt(self.editSet[1], "Shift", 16)
            elif x == 17:
                pop.editTxt(self.editSet[1], "Ctrl", 17)
            elif x == 18:
                pop.editTxt(self.editSet[1], "Alt", 18)
            else:
                pop.editTxt(self.editSet[1], y.upper(), x)

            self.editSet[0] = False

    def isOnReset(self):
        return self.reset.mouseOn()

# return funcs


def colorCheck(x, opp=255):
    if x == 0:
        a = color(55, opp)
    if x == -1:
        a = color(127, opp)
    if x == 1:
        a = color(0, 255, 255, opp)  # light blue
    if x == 2:
        a = color(255, 255, 0, opp)  # yellow
    if x == 3:
        a = color(128, 0, 128, opp)  # purple
    if x == 4:
        a = color(0, 255, 0, opp)  # green
    if x == 5:
        a = color(255, 0, 0, opp)  # red
    if x == 6:
        a = color(0, 0, 255, opp)  # blue
    if x == 7:
        a = color(255, 127, 0, opp)  # orange
    return a


def getEndPeices(lst):
    check = []
    # fides the faces that are on the bottom of the piece
    for i in range(len(lst[0])):
        if lst[-1][i] == 0:
            # print 1    #for tests
            if lst[-2][i] == 0:
                check.append([len(lst)-2, i])
            else:
                check.append([len(lst)-1, i])
        else:
            # print 2    #for tests
            check.append([len(lst), i])
    # print check    #for tests
    # drawGrid()    #for tests
    # exitp()    #for tests

    return check


def lose():
    global dead
    dead = True
    setGradient(0, int((HEIGHT/2)-.5*(HEIGHT/8)),
                WIDTH, HEIGHT/16, 100, 0, True, 100)
    setGradient(0, int((HEIGHT/2)-.5*(HEIGHT/8)+HEIGHT/16),
                WIDTH, HEIGHT/16, 0, 100, True, 100)
    textAlign(CENTER)
    textSize(30)
    fill(255, 0, 0)
    text("You Died", WIDTH/2, HEIGHT/2+10)
    textSize(15)
    text("Press '{}' to play again.".format(reset[1]), WIDTH/2, HEIGHT/2+25)


def shift90(lst, x=True):
    global check
    posCheck = True

    temp = zip(*lst[::-1])  # somehow rotaes the list, isnt stack great

    # clears piece
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != 0:
                grid[pos[0]+i][pos[1]+j] = 0

    # checks if there is nothing in the way of the rotated form
    for i in range(len(temp)):
        for j in range(len(temp[i])):
            if ((pos[0]+i > rows-1 or pos[0]+i < 0) or
                (pos[1]+j > columns-1 or pos[1]+j < 0) or
                    (grid[pos[0]+i][pos[1]+j] > 0)):
                posCheck = False

    if posCheck:
        for i in range(len(temp)):
            temp[i] = list(temp[i])
        lst = temp
    if x:
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if lst[i][j] != 0:
                    grid[pos[0]+i][pos[1]+j] = lst[i][j]

    check = getEndPeices(lst)
    return lst


def findHightLight():
    z = pos[0]
    noStop = True

    # checks where it has to go
    while noStop:
        z += 1
        for i in range(len(check)):
            if check[i][0]+z >= rows:
                noStop = False
            if check[i][0]+z < rows and not nextPeice:
                # if there is anything below the piece
                if grid[check[i][0]+z][pos[1]+i] > 0:
                    noStop = False

    return z

# no return funcs


def lineCheck():
    # caused the most annoying bug just because i called it after i drew the new peices so the peices apeared down more on the screen because the rows were deleated and the just added back on top so it move everything down by however many liness you got
    global score
    for i in range(len(grid)):
        if all(grid[i]):
            grid.insert(0, [0 for _ in range(columns)])
            grid.pop(i+1)
            score += 1


def addToGrid():
    global nextPeice, pos
    # if piece is at the bottom
    if (pos[0]+len(l)-1 > rows-1):
        nextPeice = True
        return

    # removes piece
    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] != 0:
                grid[pos[0]+i-1][pos[1]+j] = 0

    # redraws piece
    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] != 0:
                grid[pos[0]+i][pos[1]+j] = l[i][j]

    # drawGrid()    #for tests
    # exitp()    #for tests


def resetSettings():
    global keys
    pop.clearSettings()
    pop.addTxt("Control", z=False)
    pop.addTxt(setting="Move Left", key="A", keyCode=65)
    pop.addTxt(setting="Move Right", key="D", keyCode=68)
    pop.addTxt(setting="Move Down 1", key="S", keyCode=83)
    pop.addTxt(setting="Move Down 2", key="Down Arrow", keyCode=DOWN)
    pop.addTxt(setting="Rotate Left", key="Left Arrow", keyCode=LEFT)
    pop.addTxt(setting="Rotate Right", key="Right Arrow", keyCode=RIGHT)
    pop.addTxt(setting="Rotate 180", key="Up Arrow", keyCode=UP)
    pop.addTxt(setting="Pause Game", key="Space", keyCode=32)
    pop.addTxt(setting="Reset Game", key="R", keyCode=82)

    pop.addTxt(setting="Preferances", z=False)
    pop.addTxt(setting="Highlight", key=switch(x=0, y=0, w=0, state='on'))
    pop.addTxt(setting="Instant Drop", key=switch(x=0, y=0, w=0))

    pop.addTxt(setting="Sounds", z=False)
    pop.addTxt(setting="Music", key=switch(x=0, y=0, w=0, state='off'))

    keys = {
        'Move Left': 65,
        'Move Right': 68,
        'Move Down 1': 83,
        'Move Down 2': 40,
        'Rotate Left': 37,
        'Rotate Right': 39,
        'Rotate 180': 38,
        'Pause Game': 32,
        'Reset Game': 82,

        'Highlight': True,
        'Instant Drop': False,
        
        'Music': False,
        }


def pickPeice(s, x):
    global l, pos, check, l1, nextPeice
    let = s[0]
    if let == "l":
        lst = [[7, 0],
               [7, 0],
               [7, 7]]
        pos = [0, 4]
    elif let == "j":
        lst = [[0, 6],
               [0, 6],
               [6, 6]]
        pos = [0, 5]
    elif let == "i":
        lst = [[1],
               [1],
               [1],
               [1]]
        pos = [0, 4]
    elif let == "o":
        lst = [[2, 2],
               [2, 2], ]
        pos = [0, 4]
    elif let == "z":
        lst = [[5, 5, 0],
               [0, 5, 5]]
        pos = [0, 3]
    elif let == "s":
        lst = [[0, 4, 4],
               [4, 4, 0]]
        pos = [0, 4]
    else:  # t
        lst = [[3, 3, 3],
               [0, 3, 0], ]
        pos = [0, 3]
    if x:
        l = lst
        check = getEndPeices(l)
        for _ in range(s[1]):
            l = shift90(l)
    else:
        l1 = lst
        for _ in range(s[1]):
            l1 = shift90(l1, False)

def changeKeybinds():
    for i in pop.getKeyCodes():
        keys[i[0]] = i[1]

# visual funcs


def screenInfo():
    global l1
    fill(255)
    stroke(0)
    textSize(20)
    textAlign(CENTER)
    text("Score: \n {}".format(score), 35, HEIGHT*.25)
    text("Next Piece:", 53, HEIGHT*.35)
    for i in range(len(l1)):
        for j in range(len(l1[i])):
            temp = 0
            # decieds were to draw next peice so its 'centered'
            if len(l1[0]) == 1:
                x = centerX-2.5*tile
            elif len(l1[0]) == 2:
                x = centerX-3*tile+(j*tile)
            elif len(l1[0]) == 3:
                x = centerX-3.5*tile+(j*tile)
            else:
                x = j*(tile-1)
                temp = 1

            y = (HEIGHT*.40)+i*tile
            fill(colorCheck(l1[i][j]))  # sets fill color based on number
            rect(x, y, tile-temp, tile)


def highlight():
    noFill()
    z = findHightLight()
    if z-pos[0] > 4:
        for i in range(len(l)):
            for j in range(len(l[i])):
                if l[i][j] != 0:
                    strokeWeight(5)
                    stroke(colorCheck(l[i][j]))
                    x = centerX+(pos[1]+j)*tile
                    y = centerY+(i+z)*tile
                    rect(x, y, tile, tile)


def drawGrid():
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            # print r,c
            x = centerX+c*tile
            y = centerY+r*tile
            fill(55)
            stroke(0)
            fill(colorCheck(grid[r][c]))

            rect(x, y, tile, tile)
            # fill(255)#draws x,y cords on each square
            # textAlign(CENTER)
            # text(str(r)+","+str(c),x+30,y+15)


def drawGear():
    global gearLook
    x, y, w, h = [WIDTH-(25+48), 25, 48, 48]
    if (x <= mouseX <= x + w and
            y <= mouseY <= y + h):
        gearLook += 1
        if gearLook >= 6:
            gearLook = 0
    image(gear[gearLook], x, y, w, h)


def setGradient(x, y, w, h, c1, c2, axis, opacity=255):
    noFill()

    if (axis):  # Top to bottom gradient
        for i in range(y, y+h, 1):
            inter = map(i, y, y+h, 0, 1)
            c = lerpColor(c1, c2, inter)
            stroke(c, opacity)
            line(x, i, x+w, i)

    else:  # (not axis) # Left to right gradient
        for i in range(x, x+w, 1):
            inter = map(i, x, x+w, 0, 1)
            c = lerpColor(c1, c2, inter)
            stroke(c, opacity)
            line(i, y, i, y+h)

#built in funcs


def keyPressed():
    global frame, l, go, score, grid, nextPeice, dead, amount, keys
    # print keyCode

    # sets what user typed as key for the action they selected
    pop.setKeys(keyCode, key)
    changeKeybinds()

    

    if keyCode == keys['Reset Game'] and not pop.isShow:
        score = 0
        grid = [[0 for _ in range(columns)] for _ in range(rows)]
        nextPeice = True
        dead = False
        amount = 0

    if keyCode == keys['Pause Game'] and not showMenu and not dead:  # defalut space
        go = not go
    if go and not dead:
        if keyCode == keys['Move Left']:  # defalut a
            # checeks if you can move left
            c = []
            for i in range(len(l)):
                for j in range(len(l[i])):
                    if l[i][j] != 0:
                        if (grid[pos[0]+i][pos[1]+j-1] == 0) or (j != 0 and l[i][j-1] != 0):
                            c.append(True)
                        else:
                            c.append(False)
            # print c
            if all(c):
                if pos[1] > 0:
                    for i in range(len(l)):
                        for j in range(len(l[i])):
                            if l[i][j] != 0:
                                grid[pos[0]+i][pos[1]+j] = 0
                    pos[1] -= 1
                    for i in range(len(l)):
                        for j in range(len(l[i])):
                            if l[i][j] != 0:
                                grid[pos[0]+i][pos[1]+j] = l[i][j]

        if keyCode == keys['Move Right']:  # defalut d
            # checks if you can move right
            c = []
            for i in range(len(l)):
                for j in range(len(l[i])):
                    if l[i][j] != 0:
                        if (pos[1]+j+1 < columns and grid[pos[0]+i][pos[1]+j+1] == 0) or (j != len(l[0])-1 and l[i][j+1] != 0):
                            c.append(True)
                        else:
                            c.append(False)
            # print c
            if all(c):
                if pos[1]+len(l[0])-1 < columns-1:
                    for i in range(len(l)):
                        for j in range(len(l[i])):
                            if l[i][j] != 0:
                                grid[pos[0]+i][pos[1]+j] = 0
                    pos[1] += 1
                    for i in range(len(l)):
                        for j in range(len(l[i])):
                            if l[i][j] != 0:
                                grid[pos[0]+i][pos[1]+j] = l[i][j]

        if keyCode in [keys['Move Down 1'], keys['Move Down 2']]:  # defalut s and down
            if not keys['Instant Drop']:  # speeds up the rate a peice goes down
                frame = 25
            else:  # telaports a peice down
                z = findHightLight()
                for i in range(len(l)):
                    for j in range(len(l[i])):
                        if l[i][j] != 0:
                            grid[pos[0]+i][pos[1]+j] = 0

                for i in range(len(l)):
                    for j in range(len(l[i])):
                        if l[i][j] != 0:
                            grid[i+z][pos[1]+j] = l[i][j]

                nextPeice = True


def keyReleased():
    global frame, l
    if keyCode in [keys['Move Down 1'], keys['Move Down 2']]:  # s
        frame = 500 - amount*10
    # rotates
    if go:
        if keyCode == keys['Rotate Right']:
            l = shift90(l)
        if keyCode == keys['Rotate Left']:
            for i in range(3):
                l = shift90(l)
        if keyCode == keys['Rotate 180']:
            for i in range(2):
                l = shift90(l)


def mouseClicked():
    global editSet, showMenu, go, keys

    pop.isOverTxt()

    # gear/settings stuff
    x, y, w, h = [WIDTH-(25+48), 25, 48, 48]
    if (x <= mouseX <= x + w and
            y <= mouseY <= y + h):
        showMenu = not showMenu
        go = True

    # to exit the settings menu
    if pop.isOnX():
        showMenu = False

    if pop.isOnReset():
        resetSettings()

    pop.switchCheck()

    changeKeybinds()
    #print(pop.getKeyCodes())

def setup():
    global lastSec, curPeice, newPeice, gear, pop, music, nextPeice,keys

    size(WIDTH, HEIGHT)
    lastSec = millis()

    background(34)

    pop = popUp()
    resetSettings()

    # sets controls
    changeKeybinds()

    gear = []
    for i in range(1, 7):
        x = loadImage("https://oyohub.s3.amazonaws.com/spriteeditor/projects/59b6ef68ca292c67acd55560/gear-2-{}.png".format(i))
        gear.append(x)

    music = "http://rcuccurulloswebsite.oyosite.com/tetris+music.wav"

    curPeice = (choice(shapes), randint(0, 3))
    newPeice = (choice(shapes), randint(0, 3))

    pickPeice(newPeice, 0)
    pickPeice(curPeice, 1)


def draw():
    global nextPeice, lastSec, curPeice, newPeice, go, playMusic, frame, amount,keys
    if keys['Music']:
        # music.start()
        pass
    else:
        # music.pause()
        pass

    strokeWeight(1)
    background(34)

    drawGrid()  # i think you know what this does

    screenInfo()  # shows next piece and score
    if keys['Highlight'] and not dead:
        highlight()  # whows where piece will land

    drawGear()
    # print showMenu,
    if showMenu:
        pop.show()
        go = False
    else:
        pop.hide()

    if go:

        if nextPeice:

            temp = []
            for i in range(len(check)):
                if check[i][0]+pos[0] < rows:
                    # print check[i][0]+pos[0], pos[1]+i# for testing
                    temp.append(grid[check[i][0]+pos[0]][pos[1]+i])

            # lose check
            if any(grid[1]) and any(temp):
                lose()

            else:
                lineCheck()  # checks if line is full

                # makes it so nextPiece works(peice is piece im just too lazy to change it)
                curPeice = newPeice
                newPeice = (choice(shapes), randint(0, 3))

                # sets color and orientaion for the peice
                pickPeice(newPeice, 0)
                pickPeice(curPeice, 1)

                # pickPeice(('i',1,3),0)#testing each peice
                # pickPeice(('i',1,3),1)#testing each peice

                nextPeice = False  # so only one peice spawns

        # moves pieces down one tile every frame
        curr = millis()
        if curr > lastSec + frame:
            lastSec = curr
            if score % 5 == 0 and score//5 == amount+1 and score != 0:
                frame = frame-amount*10
                amount += 1
                if amount > 14:
                    amount = 14

            for i in range(len(check)):
                if check[i][0]+pos[0] < rows and not nextPeice:
                    # if there is anything below the piece
                    if grid[check[i][0]+pos[0]][pos[1]+i] > 0:
                        nextPeice = True

            if not nextPeice and not dead:
                pos[0] += 1

                addToGrid()

    else:
        if not showMenu:
            setGradient(0, int((HEIGHT/2)-.5*(HEIGHT/8)),
                        WIDTH, HEIGHT/16, 100, 0, True, 100)
            setGradient(0, int((HEIGHT/2)-.5*(HEIGHT/8)+HEIGHT/16),
                        WIDTH, HEIGHT/16, 0, 100, True, 100)
            textAlign(CENTER)
            textSize(30)
            fill(255, 0, 0)
            text("Paused", WIDTH/2, HEIGHT/2+10)
