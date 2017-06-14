################################################################################
#                                  PARIS
#                       -VExP Infant Cognition Test-
#                    PyGame Application by Griffin Tang
#
#   Citations:
#   -Pygame template adapted from Lukas Peraz's model
################################################################################

import pygame, os, time, datetime, copy, string,random
from random import shuffle
from PARISObjs import *
from pygame.locals import *

class InfantAttentionApp(object):
    #Dictionaries containing 
    mainPool = []
    testPool = []
    tested = set()
    trialRecord = []
    novelPool = set()
    famPool = set()

    def resetObjs(self):
        self.mainPool = []
        self.testPool = []
        self.tested = set()
        self.trialRecord = []
        self.novelPool = set()
        self.famPool = set()
        self.homeButtons = []
        self.homeIntInputs = []
        self.homeTextBoxes = []
        self.animationBars = []
        self.animationButtons = []
        self.animationTexts = []
        self.trialButtons = []
        self.init()

    def init(self, screen = "home"):
        #Research Customizable Variables:
        self.userBGColor = (255,255,255)
        self.LPattern = 2
        self.imgBufferTime = 0
        self.imgDisplayTime = .5
        self.imgsPerTrial = 0
        self.imgsToAnimate = []
        self.animationList = []

        #Computational Variables:
        self.initMainPool()
        self.mainPoolSize = len(self.mainPool)
        self.screen = screen
        self.triggerTrial = False
        self.trialInProgress = False
        self.startTime = 0 
        self.endTime = 0
        self.currStim = None
        self.currCount = 0
        self.currTime = 0
        self.currAnim = None
        self.timeWatched = 0
        self.currBox = None
        self.keyListen = False
        self.requestAnimations = None
        self.animationInput = False
        self.animationsComplete = True
        self.invalidInput = True
        self.trialName = ""
        self.estimatedTime = None
        #Saftey Check for User Input
        self.checkUserVars()
        self.initTrialRecord()

    def checkUserVars(self):
        assert(0 <= self.imgsPerTrial <= self.mainPoolSize)
        assert(self.imgBufferTime >= 0 and self.imgDisplayTime > 0)
        assert(self.LPattern > 0)
        for infoTupe in self.animationList:
            assert(infoTupe[1] != None and infoTupe[2] != None)
            assert(infoTupe[0] < self.imgsPerTrial)


    def initMainPool(self):
        for path, dirs, files in os.walk("MainPool"):
            for file in files:

                if file == '_DS_Store': pass
                else:
                    self.mainPool.append(Stimulus(file,os.path.join(path,file),self.width))
        self.mainPool = random.sample(self.mainPool,len(self.mainPool))
    
    def initTrialRecord(self):
        count = 1
        for path, dirs, files in os.walk("Trial Record"):
            for file in files:
                if file == '_DS_Store': pass
                else:
                    count += 1
        self.trialName += "Trial Record/"
        self.trialName += "Trial[%d]-%s" %(count, ".".join(str(datetime.date.today()).split("-")))
        self.trialName += ".txt"

    def getSamplePool(self):
        spill = self.imgsPerTrial - self.mainPoolSize
        while (spill > 0):
            for i in range(min(spill,self.mainPoolSize)):
                stimulus = self.mainPool[i]
                self.testPool.append(copy.copy(stimulus))
            self.mainPool = random.sample(self.mainPool,len(self.mainPool))
            spill -= (min(spill,self.mainPoolSize))

        for i in range(self.mainPoolSize):
            stimulus = self.mainPool[i]
            self.testPool.append(copy.copy(stimulus))

    def recordTrial(self):
        path = os.path.abspath("Trial Record")
        doc = open(self.trialName,'a')
        #self.currStim.name,self.timeWatched/self.imgDisplayTime,self.imgDisplayTime,self.imgBufferTime,self.currStim.position,self.currStim.animationType,self.userBGColor)
        for trial in self.trialRecord:
            name,onTime,totalTime,bufferTime,orientation,animate,speed,bgCol = trial
            doc.write("Name: %s | Observed Time: %d | Time Given: %d | Time Between: %d | Orientation: %s | Animation: %s | Speed: %s | Background Color: %s\n"%(name,onTime,totalTime,bufferTime,orientation,animate,speed,bgCol))
        doc.close()

    def invertBgCol(self):
        return (255-self.userBGColor[0],255-self.userBGColor[1],255-self.userBGColor[2],)

    def mousePressed(self, x, y):
        if self.screen == 'home': self.homeMouseOnePressed(x,y)
        elif self.screen == "trial": self.trialMouseOnePressed(x,y)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if self.screen == "home": self.homeKeyPressed(keyCode,modifier)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if self.screen == "home": self.homeTimerFired(dt)
        elif self.screen == "trial": self.trialTimerFired(dt)
        
    def redrawAll(self, screen):
        if self.screen == "home": self.homeDrawAll(screen)
        elif self.screen == "trial": self.trialDrawAll(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

############################### HOME SCREEN ####################################
    homeButtons = []
    homeIntInputs = []
    homeTextBoxes = []
    animationBars = []
    animationButtons = []
    animationTexts = []
    
    def updateColor(self):
        for button in self.homeButtons: button.updateColor(self.invertBgCol())
        for box in self.homeIntInputs: box.updateColor(self.invertBgCol())
        for bar in self.animationBars: bar.updateColor(self.invertBgCol())
        for animeButton in self.animationButtons: animeButton.updateColor(self.invertBgCol())
        for text in self.animationTexts: text.updateColor(self.invertBgCol())
        for text in self.homeTextBoxes: text.updateColor(self.darkenColor(self.userBGColor))

    def darkenColor(self,color):
        if color == (0,0,0): return (50,50,50)
        else:
            return tuple(map(lambda x: (x)//3, list(color)))

    def homeMouseOnePressed(self, x, y):
        for button in self.homeButtons:
            if button.isClicked(x,y):
                if button.msg in ["Animations","Reset"] and self.animationInput:
                    if self.requestAnimations == False:
                        self.imgsToAnimate = []
                        self.animationList = []
                        self.animationBars = []
                        self.animationButtons = []
                        self.animationTexts = []
                        self.requestAnimations = True
                    elif self.requestAnimations == None: button.textUpdate("Reset")
                    self.requestAnimations = True
                    self.animationsComplete = False
                elif button.msg == "Begin Trial!":
                    self.screen = "trial"
                    self.getSamplePool()
                    self.applyAnimations()
                    self.nextTrial()

        for button in self.animationButtons:
            if button.msg in ["Next","Complete"]:
                if button.isClicked(x,y) and self.currAnim < len(self.imgsToAnimate):
                    if button.msg == "Complete":
                        self.addAnimations()
                        self.animationsComplete = True

                    if button.msg == "Next": 
                        if self.currAnim == len(self.imgsToAnimate) - 2: 
                            button.textUpdate("Complete") 
                            button.msg = "Complete"
                        self.addAnimations()
                        self.currAnim += 1
                        self.animationTexts[0].textUpdate("Configure Animations for Image %s"%(self.imgsToAnimate[self.currAnim]))
        count = 0
        for intBox in self.homeIntInputs:
            if intBox.isClicked(x,y):
                self.currBox = intBox
                intBox.select(True)
                self.keyListen = True 
            else:
                intBox.select(False)
                count += 1
            if count == len(self.homeIntInputs): 
                self.keyListen = False
                self.currBox = None

        for bar in self.animationBars:
            bar.isClicked(x,y)

    def addAnimations(self):
        if self.imgsToAnimate == []: pass
        else:
            infoList = [int(self.imgsToAnimate[self.currAnim])-1]
            for bar in self.animationBars:
                for button in bar.buttonList:
                    if button.clicked: infoList.append(button.msg)
            self.animationList.append(tuple(infoList))
    
    def applyAnimations(self):
        for infoTupe in self.animationList:
            self.testPool[infoTupe[0]].addAnimations(infoTupe[1:])
    
    def homeKeyPressed(self, keyCode, modifier):
        if self.keyListen:
            if (pygame.key.name(keyCode) in string.ascii_letters) or (pygame.key.name(keyCode) == "backspace") or pygame.key.name(keyCode) in ["1","2","3","4","5","6","7","8","9","0",".",","]:
                self.currBox.updateData(pygame.key.name(keyCode))

    def homeTimerFired(self, dt):
        if self.homeButtons == []:
            #                                centerX       centerY    width,height  text       color  textColor
            self.homeButtons.append(Button(self.width//2,6*self.height//7,310,75,"Need Input!","blue","blue"))
            self.homeButtons.append(Button(4*self.width//10,7*self.height//10,150,30,"Animations","blue","blue"))
        if self.homeTextBoxes == []:
            self.homeTextBoxes.append(TextBox(self.width//2,6*self.height//7-50,"",14,"blue"))
            self.homeTextBoxes.append(GuideBox(20,3*self.height//4,"Guide:",20,"blue"))
            self.homeTextBoxes.append(GuideBox(20,3*self.height//4+25,"-The window is resizable; resizing initiates a restart",14,"blue"))
            self.homeTextBoxes.append(GuideBox(20,3*self.height//4+25*2,"-If animations are desired, configure them last",14,"blue"))
            self.homeTextBoxes.append(GuideBox(20,3*self.height//4+25*3,"-For a list of recognized colors, check the top of PARISObjs.py",14,"blue"))
        if self.homeIntInputs == []:
            self.homeIntInputs.append(InputBox(3.5*self.width//10,  self.height//10,"Background Color:",""" (e.g. "blue")""","blue"))
            self.homeIntInputs.append(InputBox(3.5*self.width//10,2*self.height//10,"Images Per Trial:"," (with %d individual images in Library)"%(self.mainPoolSize),"blue"))
            self.homeIntInputs.append(InputBox(3.5*self.width//10,3*self.height//10,"Image Display Duration:","seconds","blue"))
            self.homeIntInputs.append(InputBox(3.5*self.width//10,4*self.height//10,"Time Between Image Display:","seconds","blue"))
            self.homeIntInputs.append(InputBox(3.5*self.width//10,5*self.height//10,"Left-Right Pattern:","(e.g. LR is 2, LRR is 3...)","blue"))
            self.homeIntInputs.append(InputBox(3.5*self.width//10,6*self.height//10,"Images to Animate:"," (e.g. 1,2,3)","blue"))

        if self.requestAnimations and self.imgsToAnimate != []:
            self.currAnim = 0
            self.animationMessage = "Complete"
            if self.currAnim < len(self.imgsToAnimate) - 1: self.animationMessage = "Next"
            self.animationTexts.append(TextBox(2.17*self.width//3,1.5*self.height//10,"Configure Animations for Image %s"%(self.imgsToAnimate[self.currAnim]),15,"blue"))
            self.animationBars.append(OptionBar(2*self.width//3,2*self.height//10,["Rotate","Move","Grow"],70,30,"blue"))
            self.animationBars.append(OptionBar(2*self.width//3,3*self.height//10,["Slowly","Moderately","Quickly"],70,30,"blue"))
            self.animationButtons.append(Button(8*self.width//10,5.8*self.height//10,150,30,self.animationMessage,"blue","blue"))   
            self.requestAnimations = False

        errorCount = 0
        for intBox in self.homeIntInputs:
            if (intBox.invalidData or intBox.quantData == None) and not (intBox.label.startswith("Images to A")): errorCount += 1
        if errorCount>0: self.invalidInput = True
        else: self.invalidInput = False

        if not self.invalidInput and self.animationsComplete: 
            self.homeButtons[0].textUpdate("Begin Trial!")
            self.homeButtons[0].msg = "Begin Trial!"
            self.getPredictedDuration()
            self.homeTextBoxes[0].textUpdate("Estimated Duration: %s"%self.estimatedTime)
        else:
            self.homeButtons[0].msg = "Need Input!"
            self.homeButtons[0].textUpdate("Need Input!")
            self.homeTextBoxes[0].textUpdate("")

        self.interpretButtons()

    def getPredictedDuration(self):
        totalSeconds = self.imgsPerTrial * (self.imgDisplayTime + self.imgBufferTime)
        totalMinutes = totalSeconds // 60
        remainingSeconds = totalSeconds %60
        minString = "minutes"
        secString = "seconds"
        if totalMinutes == 1: minString = "minute"
        if remainingSeconds == 1: secString = "second"
        self.estimatedTime = "%d %s and %d %s" %(totalMinutes,minString,remainingSeconds,secString)

    def interpretButtons(self):
        for box in self.homeIntInputs:
            if box.label.startswith("Images to") and box.quantData != None: self.animationInput = True
            if box.quantData != None:
                if box.label.startswith("Background"):
                    self.userBGColor = box.quantData
                    self.updateColor()
                elif box.label.startswith("Images Per"):
                    self.imgsPerTrial = box.quantData
                elif box.label.startswith("Image Display"):
                    self.imgDisplayTime = box.quantData
                elif box.label.startswith("Time"):
                    self.imgBufferTime = box.quantData
                elif box.label.startswith("Images to"):
                    self.imgsToAnimate = box.quantData
                elif box.label.startswith("Left-Right"):
                    self.LPattern = box.quantData

    def homeDrawAll(self,screen):
        for button in self.homeButtons:
            if button.msg == "Animations" and not self.animationInput: pass
            else: button.draw(screen)
        for intBox in self.homeIntInputs:
            intBox.draw(screen)
        if self.animationBars != [] and not self.animationsComplete:
            for bar in self.animationBars:
                bar.draw(screen)
        if self.animationButtons != [] and not self.animationsComplete:
            for button in self.animationButtons:
                button.draw(screen)
        if self.animationTexts != [] and not self.animationsComplete:
            for text in self.animationTexts:
                text.draw(screen)
        if self.homeTextBoxes != []:
            for text in self.homeTextBoxes:
                text.draw(screen)

############################### TRIAL SCREEN ###################################
    trialButtons = [] 
    def commenceTrial(self):
        self.trialInProgress = True
        self.triggerTrial = False
        self.loadStimulus()

    def loadStimulus(self):
        self.currStim = self.testPool.pop(0)
        if self.currCount % self.LPattern == 0: 
            self.currStim.posUpdate("left")
        else: 
            self.currStim.posUpdate("right")
        self.startTime = time.time()

    def concludeTesting(self):
        self.tested.clear()
        self.testPool = []
        self.currCount = 0
        self.triggerTrial = False
        self.trialInProgress = False
        self.currStim = None
        self.screen = "home"
        self.recordTrial()

    def trialMouseOnePressed(self, x, y):
        pass

    def trialTimerFired(self, dt):
        self.currTime = time.time()
        if self.triggerTrial:
            if (abs(self.currTime - self.startTime) < self.imgBufferTime): 
                self.currStim = None
                pass
            else: self.commenceTrial()

        elif self.trialInProgress:
            self.currTime = time.time()
            if (abs(self.currTime - self.startTime) < self.imgDisplayTime): 
                #record time 
                pass
            else:
                self.currStim.recordEntry(self.currStim.name,self.currStim.position,self.timeWatched/self.imgDisplayTime)
                self.trialRecord.append((self.currStim.name,self.timeWatched/self.imgDisplayTime,self.imgDisplayTime,self.imgBufferTime,self.currStim.position,self.currStim.animateType,self.currStim.animateSpeed,str(self.userBGColor)))
                self.tested.add(self.currStim)
                self.currCount += 1
                self.trialInProgress = False
                if len(self.testPool) > 0: self.nextTrial()
                else: self.concludeTesting() 

        if self.trialButtons == []: self.trialButtons.append(Button(self.width//2,self.height//2,50,50,str(self.currTime-self.startTime),"black","black"))
        if self.currStim != None: 
            self.currStim.animate()
        for button in self.trialButtons:
            button.textUpdate(str(abs(round(self.currTime-self.startTime,2))))
    
    def nextTrial(self):
        self.triggerTrial = True
        self.startTime = time.time()
    
    def trialDrawAll(self,screen):
        if self.currStim != None: self.currStim.draw(screen)
        for button in self.trialButtons:
            button.draw(screen)

################################################################################
    def __init__(self, width=1200, height=800, fps=100, title="Infant Attention App"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height),pygame.RESIZABLE)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    if event.key == ord("q") and event.mod == 1: #Shift + Q
                        playing = False
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
                elif event.type==VIDEORESIZE:
                    screen=pygame.display.set_mode(event.dict['size'],pygame.RESIZABLE)
                    self.width,self.height = event.dict['size'][0],event.dict['size'][1]
                    pygame.display.flip()
                    self.resetObjs()
            screen.fill(self.userBGColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = InfantAttentionApp()
    game.run()

if __name__ == '__main__':
    main()
