from turtle import *
from PIL import Image
from time import sleep
from random import randint
import os
import sys


#lists of possible combinations
colors = ["green", "yellow", "white", "grey"]
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ü"]
regions = ["top", "bottom"]

#create class for turtles
class newTurtle(Turtle):
    #init function
    def __init__(self, letter, color, region):
        Turtle.__init__(self)
        
        self.hideturtle()
        self.speed(0)
        self.penup()
        
        self.letter = letter
        self.color = color
        self.region = region
        self.filename = "newpics/" + self.letter + "_" + self.color + "_" + self.region + ".gif"
        self.image = Image.open(self.filename)
        if region == "bottom":  
            self.x = ((letters.index(self.letter) % 5) * 1.05 * self.image.size[0]) - ((1.05 * self.image.size[0]) * 2)
            self.y = (-1 * (letters.index(self.letter) // 5) * 1.05 * self.image.size[1]) - ((1.05 * self.image.size[1]) * 2)
        elif region == "top":
            self.x = ((blankIndex % 5) * 1.05 * self.image.size[0]) - ((1.05 * self.image.size[0]) * 2)
            self.y = -((blankIndex // 5) * 1.05 * self.image.size[1]) + ((1.05 * self.image.size[0]) * 5.5)
        self.shape(self.filename)

        self.onclick(self.gedrückt)
        
        self.goto(self.x, self.y)
        self.showturtle()

    #function for when turtles are clicked
    def gedrückt(self, x, y):
        if self.region == "bottom":         #check if clicked turtle is on keyboard
            global guess
            global charNum
            if self.letter == "Ü":
                os.startfile(sys.argv[0])   #restart/reload code
                sys.exit()
            if solved != True and  trys <= 5:       #if game is still on
                #print(self.letter)
                changeGameTurtle(charNum, self.letter, "white")
                charNum = charNum + 1
                guess = guess + self.letter
                getGuess()

def create_newTurtle(letter, color, region):    #function to create new turtle
    return newTurtle(
        letter = letter,
        color = color,
        region = region
        )

def changeKeyboardTurtle(letter, newColor):     #change turtles on keyboard
    filepath = "newpics/" + letter + "_" + newColor + "_bottom.gif"
    keyboardTurtles[letters.index(letter)].shape(filepath)

def changeGameTurtle(index, newLetter, newColor):   #change turtles on gaamefield
    filepath = "newpics/" + newLetter + "_" + newColor + "_top.gif"
    gameTurtles[index].shape(filepath)

def registerShapes():                           #register all turtle shapes from file folder
    # registering the image
    # as a new shape
    for letter in letters:
        for color in colors:
            for region in regions:
                filepath = "newpics/" + letter + "_" + color + "_" + region + ".gif"
                screen.register_shape(filepath)
    screen.register_shape("newpics/NULL_NULL_top.gif")

def setTurtles():                               #create and set all turtles to their position
    global keyboardTurtles
    keyboardTurtles = []
    for letter in letters :
        color = "white"
        region = "bottom"
        keyboardTurtles.append(create_newTurtle(letter, color, region))

    global gameTurtles
    global blankIndex
    gameTurtles = []
    for blankIndex in range(30):
        letter = "NULL"
        color = "NULL"
        region = "top"
        gameTurtles.append(create_newTurtle(letter, color, region))

    keyboardTurtles[letters.index("Ü")].goto((105.00,-367.50))      #set "reload" turtle to correct position

def writeTitle():                                               #write the title of the game on gamefield
    writer.hideturtle()
    writer.penup()
    writer.goto(-95, 340)
    writer.write("WordlePy", font=("Courier", 30, "bold"))

def listupper(list_):                                       #make all entrys of list uppercase
    upperList = []
    for word in list_:
        word = word.upper()
        upperList.append(word)
    list_ = upperList
    return list_

def possibleWords(list_):                                   #filter out all bad words
    posWords = [item for item in list_ if len(item) == 5]
    return posWords
    
def randSelect(list_):                                      #select random from list
    selection = list_[randint(0, len(list_) - 1)]
    return selection

def getGuess():                                             #get guess from player
    global guess
    global trys
    if len(guess) == 5:
        #print(guess)
        guess = guess.upper()
        checkGuess(guess)
        guess = ""

def checkGuess(guess):                                      #check the guess the player entered
    global answer
    global charNum
    global solved
    global trys
    if len(guess) == 5:
        if (guess in listupper(possibleWords(dictonary))) == True:      #check if guess is possible word
            trys = trys + 1
            if guess == selectedWord:
                #print("Korrekt, das Wort war " + selectedWord)
                solved = True
            letterNum = 0
            for n in guess:                                 #go through every letter of guess and correct
                if n == selectedWord[letterNum]:
                    answer = answer + "X"
                    changeGameTurtle(charNum - 5 + letterNum, n, "green")
                    changeKeyboardTurtle(n, "green")
                    
                elif (n in selectedWord) == True:
                    answer = answer + "Y"
                    changeGameTurtle(charNum - 5 + letterNum, n, "yellow")
                    if keyboardTurtles[letters.index(n)].color != "green": 
                        changeKeyboardTurtle(n, "yellow")
                    
                else:
                    answer = answer + "O"
                    changeGameTurtle(charNum - 5 + letterNum, n, "grey")
                    changeKeyboardTurtle(n, "grey")
                    
                letterNum = letterNum + 1
            #print("                  " + answer)
            answer = ""
        else:
            #print("Das Wort existiert nicht!")
            for _ in range(6):
                changeGameTurtle(charNum - _, "NULL", "NULL")
            charNum = charNum - 5
        if trys > 5:                            #end game if trys is too high
            #print("Das war dein letzter Versuch!")
            writer.goto(-140, -50)
            writer.write("Das Wort war " + selectedWord, font=("Courier", 20, "bold"))
    
#--------code---------
screen = Screen()                       #setup screen
screen.setup(400, 900)
screen.title("WordlePy")
screen.bgcolor("light grey")
screen.tracer(False)

f = open("deutsch.txt", "r")            #open file and split to list
content = f.read()
dictonary = content.split("\n")
f.close()

writer = Turtle() 

blankIndex = 0

answer = ""
guess = ""
trys = 0
charNum = 0
solved = False
selectedWord = randSelect(listupper(possibleWords(dictonary)))
#enable for dev mode
#print(selectedWord)

posWords = []

writeTitle()                            #setup gamefield
registerShapes()
setTurtles()

#print(keyboardTurtles[letters.index("Ü")].pos())

#--------main---------
while True:
    screen.update()
