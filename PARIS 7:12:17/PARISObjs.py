import pygame, os, string

def initColors():
        cols = {}
        cols["white"] = (255,255,255)
        cols["black"] = (0,0,0)
        cols["red"] = (220,0,0)
        cols["green"] = (0,128,0)
        cols["blue"] = (0,0,255)
        cols["purple"] = (139,0,139)
        cols["magenta"] = (255,0,255)
        cols["gray"] = (192,192,192)
        cols["grey"] = (192,192,192)
        cols["maroon"] = (128,0,0)
        cols["cyan"] = (0,255,255)
        cols["yellow"] = (255,255,0)
        cols["teal"] = (100,200,200)
        cols["orange"] = (255,150,0)
        cols["darkteal"] = (0,128,128)
        cols["pink"] = (255,182,193)
        cols["lightblue"] = (180,255,255)
        return cols 

class Stimulus(object):
    def __init__(self,name,path,screenWidth):
        self.name = name
        self.screenWidth = screenWidth
        self.position = "left"
        self.xPos = screenWidth//4
        self.ogX = self.xPos
        self.yPos = 200
        self.direction = "Right"
        self.path = path
        self.originalImg = pygame.image.load(path)
        self.img = self.originalImg
        self.times = []
        self.angle = 0
        self.imgSize = self.originalImg.get_rect()[2],self.originalImg.get_rect()[3]
        self.dx = 0
        self.dy = 0
        #TODO animate functions that take in:
        #                   Type: grow, move, rotate
        #                   Speed: slow, medium, fast                               
        self.animateType = "None"
        self.animateSpeed = "None"

    def posUpdate(self,side):
        if side == "left":
            self.position = "left"
            self.xPos = self.screenWidth//4
            self.ogX = self.xPos
        else:
            self.position = "right"
            self.xPos = 3*self.screenWidth//4
            self.ogX = self.xPos

    def addAnimations(self, infoTupe):
        self.animateType = infoTupe[0]
        self.animateSpeed = infoTupe[1]
        if self.animateSpeed == "Quickly": self.dx = 10; self.dy = 10
        elif self.animateSpeed == "Moderately": self.dx = 5; self.dy = 5
        elif self.animateSpeed == "Slowly": self.dx = 2; self.dy = 2

    def recordEntry(self,name,position,time):
        time = round(time,3)
        self.times.append((name,position,time))

    def draw(self,screen):
        screen.blit(self.img,(self.xPos-self.img.get_width()//2,self.yPos-self.img.get_height()//2))

    def animate(self):
        if self.animateType == "None" or self.animateType == "None": pass
        else:
            if self.animateType == "Rotate": self.rotate()
            elif self.animateType == "Grow": self.grow()
            elif self.animateType == "Move": self.move()

    def move(self):
        if self.xPos > self.screenWidth - self.imgSize[0]//2 or self.xPos > self.ogX + self.imgSize[0]:
            self.direction = "Left"
        elif self.xPos < self.imgSize[0]//2 or self.xPos < self.ogX - 20:
            self.direction = "Right"

        if self.direction == "Right": self.xPos += self.dx
        else: self.xPos -= self.dx

    def grow(self):
        rect = self.originalImg.get_rect()
        (width,height) = self.imgSize
        if (width < 1.5*rect[2]) or (height < 1.5*rect[3]):
            width += self.dx
            height += self.dx
            newImg = pygame.transform.scale(self.originalImg,(width,height))
            self.imgSize = (width,height)
            self.img = newImg
        else: 
            pass

    def rotate(self):
        rect = self.originalImg.get_rect()
        newImg = pygame.transform.rotate(self.originalImg, self.angle)
        #rect = newImg.get_rect(center=rect.center)
        self.img = newImg
        if self.angle + self.dx > 360: pass
        else: self.angle += self.dx

class Button(object):
    def __init__(self, centerX, centerY, width, height, text, color, textColor, fontsize = 0):
        colorList = initColors()
        self.centerX,self.centerY = centerX, centerY
        self.width, self.height = width, height
        self.coords = (centerX-width//2,centerY-height//2,width,height)
        self.msg = text
        self.col = self.muteCol(colorList[color])
        self.textCol = self.muteCol(colorList[color])
        self.fontsize = 15 * width//80
        if fontsize != 0: self.fontsize = fontsize
        self.font = pygame.font.Font(os.path.abspath('Fonts/Georgia.ttf'),self.fontsize)
        self.text = self.font.render(text, True, self.textCol)
        self.textX = centerX - self.text.get_width()//2
        self.textY = centerY - self.text.get_height()//2
        self.stroke = 1
        self.clicked = False

    def updateColor(self, color):
        self.col = color
        self.textCol = color
        self.text = self.font.render(self.msg, True, color)

    def textUpdate(self,text):
        font = pygame.font.Font(os.path.abspath('Fonts/Georgia.ttf'),self.fontsize)
        self.msg = text
        self.text = font.render(text, True, self.textCol)
        self.textX = self.centerX - self.text.get_width()//2
        self.textY = self.centerY - self.text.get_height()//2

    def draw(self,screen):
        pygame.draw.rect(screen,self.col,self.coords, self.stroke)
        screen.blit(self.text,(self.textX,self.textY))

    def isClicked(self, x, y):
        if ((self.centerX-self.width//2 <= x <= self.centerX+self.width//2) 
         and (self.centerY-self.height//2 <= y <= self.centerY+self.height//2)):
            self.stroke = 3
            self.clicked = True
            return True
        else:
            self.stroke = 1
            self.clicked = False
            return False

    def muteCol(self,color):
        return tuple(map(lambda x: x//2, color))

class TextBox(object):
    def __init__(self,centerX,centerY,text,size,color):
        colorList = initColors()
        self.color = self.muteCol(colorList[color])
        self.centerX,self.centerY = centerX, centerY
        self.font = pygame.font.Font(os.path.abspath('Fonts/Georgia.ttf'),size)
        self.msg = text
        self.text = self.font.render(self.msg, True, self.color)
        self.textX = centerX - self.text.get_width()//2
        self.textY = centerY - self.text.get_height()//2

    def draw(self,screen):
        screen.blit(self.text,(self.textX,self.textY))

    def textUpdate(self,newText):
        self.msg = newText
        self.text = self.font.render(newText, True, self.color)
        self.textX = self.centerX - self.text.get_width()//2

    def muteCol(self,color):
        return tuple(map(lambda x: x//2, color))
    
    def updateColor(self,color):
        self.color = color
        self.text = self.font.render(self.msg, True, color)

class GuideBox(TextBox):
    def __init__(self,centerX,centerY,text,size,color):
        colorList = initColors()
        self.color = self.muteCol(colorList[color])
        self.centerX,self.centerY = centerX, centerY
        self.font = pygame.font.Font(os.path.abspath('Fonts/Georgia.ttf'),size)
        self.msg = text
        self.text = self.font.render(self.msg, True, self.color)
        self.textX = centerX
        self.textY = centerY - self.text.get_height()//2

class InputBox(object):
    #Label is text descriptor
    #Tag is following notation e.g. "seconds"
    def __init__(self,centerX,centerY,label,tag,color):
        self.colorList = initColors()
        self.charMax = 30
        self.data = ""
        self.quantData = None
        self.tag = tag
        self.invalidData = False
        self.nums = {"1","2","3","4","5","6","7","8","9","0","."}
        self.punct = {".",","}
        self.fontsize = 15
        self.centerX,self.centerY = centerX, centerY
        self.label = label
        self.col = self.muteCol(self.colorList[color])
        self.textCol = self.colorList[color]
        self.font = pygame.font.Font(os.path.abspath('Fonts/Georgia.ttf'),self.fontsize)
        self.boxHeight = 20
        self.boxWidth = 15
        self.text = self.font.render(label,True, self.col)
        self.textX = self.centerX - self.text.get_width()
        self.textY = self.centerY - self.text.get_height()//2
        self.aftertext = self.font.render(tag,True, self.col)
        self.aftertextX = self.centerX+self.fontsize+self.boxWidth
        self.aftertextY = self.centerY - self.aftertext.get_height()//2
        self.boxCoords = (centerX+self.fontsize//2,centerY-self.boxHeight//2,self.boxWidth,self.boxHeight)
        self.stroke = 1
        self.boxText = self.font.render(self.data,True, self.textCol)
        self.boxTextX = centerX+3*self.fontsize//4
        self.boxTextY = centerY -self.text.get_height()//2
        self.errorText = self.font.render("Invalid Parameter!",True, self.colorList["red"])
        self.errorTextX = self.aftertextX + self.aftertext.get_width()+ self.fontsize
        self.errorTextY = self.centerY - self.aftertext.get_height()//2

    def updateColor(self,color):
        self.col = color
        self.textCol = color
        self.text = self.font.render(self.label, True, color)
        self.aftertext = self.font.render(self.tag,True, color)
        self.boxText = self.font.render(self.data,True, color)
        
    def recalculatePos(self):
        self.boxCoords = (self.centerX+self.fontsize//2,self.centerY-self.boxHeight//2,self.boxWidth,self.boxHeight)
        self.aftertextX = self.centerX+self.fontsize+self.boxWidth
        self.errorTextX = self.aftertextX+self.aftertext.get_width()+self.fontsize

    def draw(self,screen):
        screen.blit(self.aftertext,(self.aftertextX,self.aftertextY))
        screen.blit(self.text,(self.textX,self.textY))
        screen.blit(self.boxText,(self.boxTextX,self.boxTextY))
        pygame.draw.rect(screen,self.col,self.boxCoords, self.stroke)
        if self.invalidData: screen.blit(self.errorText,(self.errorTextX,self.errorTextY))
    
    def isClicked(self, x, y):
        return ((self.centerX+self.fontsize//2 <= x <= self.centerX+self.fontsize//2+self.boxWidth) 
         and (self.centerY-self.boxHeight//2 <= y <= self.centerY+self.boxHeight//2))

    def updateData(self,char):
        if char == "backspace" and self.data != "":
            self.data = self.data[:-1]
            self.boxWidth -= self.fontsize//2
        elif char != "backspace" and len(self.data) < self.charMax:
            self.data += char
            self.boxWidth += self.fontsize//2
        self.boxText = self.font.render(self.data,True,self.col)
        self.checkData()
        self.recalculatePos()

    def checkData(self):
        if (self.tag == "seconds"):
            count = 0
            for char in list(self.data):
                if char not in self.nums or (char =="0" and len(list(self.data)) == 1): self.invalidData = True
                else: count += 1
            if count == len(list(self.data)): self.invalidData = False
            self.quantizeTime()
        elif (self.tag == """ (e.g. "blue")"""):
            count = 0
            for char in list(self.data):
                if (char in (self.nums)) or (char in self.punct): self.invalidData = True
                else: count += 1
            if count == len(list(self.data)): self.invalidData = False
            self.quantizeCol()
        elif (self.tag == " (e.g. 1,2,3)"): 
            count = 0
            for char in list(self.data):
                if ((char not in (self.nums)) and (char not in self.punct)) or char == "." or (char =="0" and len(list(self.data)) == 1): self.invalidData = True
                else: count += 1
            if count == len(list(self.data)): self.invalidData = False
            self.quantizeList()
        elif self.tag.startswith(" (with"):
            count = 0
            for char in list(self.data):
                if char not in self.nums or char == "." or (char =="0" and len(list(self.data)) == 1): self.invalidData = True
                else: count += 1
            if count == len(list(self.data)): self.invalidData = False
            self.quantizeNum()
        elif self.tag.startswith("(e.g. LR"):
            count = 0
            for char in list(self.data):
                if char not in self.nums or char == "." or (char =="0" and len(list(self.data)) == 1): self.invalidData = True
                else: count += 1
            if count == len(list(self.data)): self.invalidData = False
            self.quantizeLR()

    def quantizeLR(self):
        if not self.invalidData and self.data != "": 
            num = int(self.data)
            self.quantData = num

    def quantizeList(self):
        if not self.invalidData and "." not in self.data:
            self.quantData = list(filter(lambda x:x!="",self.data.split(",")))
            #print("Images to Animate: ",self.quantData)
    
    def quantizeCol(self):
        if not self.invalidData and self.data in self.colorList: 
            self.quantData = self.colorList[self.data]
            self.textCol = self.muteCol(self.quantData)
            self.boxText = self.font.render(self.data,True, self.textCol)
            #print("Recognized Color: ",self.data)

    def muteCol(self,color):
        return tuple(map(lambda x: x//2, color))

    def quantizeTime(self):
        if not self.invalidData and ".." not in self.data and self.data != ".": 
            count = 0
            num = None
            for char in list(self.data):
                if char == ".": count += 1
            if self.data != "" and count <=1: 
                num = float(self.data)
                self.quantData = num

    def quantizeNum(self):
        if not self.invalidData:
            if self.data != "": 
                num = int(self.data)
                #if num > self.mainPoolSize(): self.invalidData = True
                self.quantData = num

    def mainPoolSize(self):
        x = list(filter(lambda x: x in self.nums, list(self.tag)))
        return int("".join(x))

    def select(self,selected):
        if selected: self.stroke = 3
        else: self.stroke = 1

class OptionBar(object):
    def __init__(self,centerX,centerY,optionList,widthPer,height,color):
        self.centerX = centerX
        self.centerY = centerY
        self.widthPer = widthPer
        self.height = height
        self.optionList = optionList #contains "name"
        self.color = color
        self.buttonList = self.optionsToButtons()

    def updateColor(self,color):
        self.color = color
        for button in self.buttonList: button.updateColor(color)

    def optionsToButtons(self):
        n = 0
        result = []
        for option in self.optionList:
            newButton = Button(self.centerX+self.widthPer*n,self.centerY,self.widthPer,self.height,option,self.color,self.color)
            result.append(newButton)
            n += 1
        return result

    def draw(self,screen):
        for button in self.buttonList:
            button.draw(screen)

    def isClicked(self, x, y):
        for button in self.buttonList:
            if ((button.centerX-button.width//2 <= x <= button.centerX+button.width//2) 
                and (button.centerY-button.height//2 <= y <= button.centerY+button.height//2)):
                button.stroke = 3
                button.clicked = True
                for otherbutton in self.buttonList:
                    if otherbutton != button: 
                        otherbutton.clicked = False
                        otherbutton.stroke = 1


