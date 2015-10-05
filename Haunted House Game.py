




# Date: 17 Mar 2015
# Modified by Tony Kuo, David McCurdy

# NOTE: 
# This game was created based on the book: Write Your Own Adventure Programs
# Written by Jenny Tyler, Les Howarth
# Published by Usborne computer books, 1983
# https://books.google.co.nz/books?id=f6BoAAAACAAJ

# Description: Code used for ISCG 5420 Assignment 2015 S1.




# currentLocation equals 0-63
import pickle
import random
import sys




#############################################################################################################
# GAME DATA                                                                                                 #
#############################################################################################################

# SOME CONSTANTS
HERO_INVENTORY_POS = 999
##variable declaired 

# this list draws the map
# if options are SE that means there are walls at NW etc
DirectionsList = ['SE', 'WE',  'WE',  'W', 'WE',   'WE',  'SWE',  'WS', #0-7
                   'NS', 'SE',  'WE',  'NW',  'SE',   'W',   'NE',   'NSW', #8-15
                   'NS', 'NS',  'SE',  'WE',  'NW', 'SE',  'WS', 'NX', #16-23
                   'N',  'NS',  'NSE',  'WE',  'WE',   'NSW', 'NS',   'NS', # 24 - 31
                   'S',  'NSE', 'NSW', 'S',   'NS', 'N',   'N',    'NS', #32 - 39
                   'NE', 'NSW',  'NE',  'W',   'NSE',  'WE',  'W',    'NS', #40 - 47
                   'SE', 'NSW', 'E',   'WE',  'NW',   'SE',   'SWE',   'NW', #48 - 55
                   'NE', 'NWE', 'WE',  'WE',  'WE',   'NWE', 'NWE',  'W'] #56 - 63

#variable list directionslist 63 parts tells user where they are

# '\' below is a continuation character, it tells Python that the current statement continues to the next line.

LocationsList = \
[ 'DARK CORNER',                  'OVERGROWN GARDEN',       'BY LARGE WOODPILE',         'BY PILE OF CRUD',
  'WEEDPATCH',                    'FOREST',                 'THICK FOREST',              'BLASTED TREE',
  'CORNER OF HOUSE',              'ENTRANCE TO KITCHEN',    'KITCHEN & GRIMY COOKER',    'SCULLERY DOOR',
  'ROOM WITH INCHES OF DUST',     'REAR TURRET ROOM',       'CLEARING BY HOUSE',         'PATH',
  'SIDE OF HOUSE',                'BACK OF HALLWAY',        'DARK ALCOVE',               'SHALL DARK ROOM',
  'BOTTOM OF SPIRAL STAIRCASE',   'WIDE PASSAGE',           'SLIPPERY STEPS',            'CLIFFTOP',
  'NEAR CRUMBLING WALL',          'GLOOMY PASSAGE',         'POOL OF LIGHT',             'IMPRESSIVE VAULTED HALLWAY',
  'HALL BY THICK WOODEN DOOR',    'TROPHY ROOM',            'CELLAR WITH BARRED WINDOW', 'CLIFF PATH',
  'CUPBOARD WITH HANGING COAT',   'FRONT HALL',             'SITTING ROOM',              'SECRET ROOM',
  'STEEP MARBLE STAIRS',          'DINING ROOM',            'DEEP CELLAR WITH COFFIN',   'CLIFF PATH',
  'CLOSET',                       'FRONT LOBBY',            'LIBRARY OF EVIL BOOKS',   'STUDY WITH DESK & HOLE IN WALL',
  'WEIRD COBWEBBY ROOM',          'VERY COLD CHAMBER',      'SPOOKY ROOM',               'CLIFF PATH BY MARSH',
  'RUBBLE-STREWN VERANDAH',       'FRONT PORCH',            'FRONT TOWER',               'SLOPING CORRIDOR',
  'UPPER GALLERY',                'MARSH BY WALL',          'MARSH',                     'SOGGY PATH',
  'BY TWISTED RAILING',           'PATH THROUGH IRON GATE', 'BY RAILINGS',               'BENEATH FRONT TOWER',
  'DEBRIS FROM CRUMBLING FACADE', 'LARGE FALLEN BRICKWORK', 'ROTTING STONE ARCH',        'CRUMBLING CLIFFTOP']
PLANK OF WOOD

#list of all options player can do in game
VerbList = ['DIRECTIONS: W= UP S= DOWN A= LEFT D= RIGHT',\
            'CARRYING?: DISPLAYS INVENTORY', \
            'GET: GET FOLLOWED BY THE ITEM NAME ADDS THE ITEM TO PLAY INVENTORY E.G GET AXE', \
            'TAKE TAKE FOLLOWED BY THE ITEM NAME ADDS THE ITEM TO PLAY INVENTORY E.G TAKE AXE',   \
            'OPEN MIGHT BE A USEFUL WORD WHEN CONFRONTED WITH A LOCKED DOOR', \
            'EXAMINE: EXAMINE FOLLOWED BY THE OBJECT YOU WANT TO EXAMINE MORE CLOSELY LETS YOU FIND OUT MORE ABOUT IT ', \
            'READ: IS A KEY WORD THAT SHOULD BE USED BEFORE AN OBJECT IE READ BOOK',  \
            'DIG: ALLOWS PLAYER TO DIG AS LONG AS PLAYER HAS SHOVEL IN INVENTORY',\
            'USE THE WORD USE FOLLOWE BY AN ITEM YOU ARE HOLDING WILL USE THAT ITEM IN THE SITUATION IF APPROPRIATE',\
            'UNLOCK MIGHT BE USEFUL WHEN CONFRONTED WITH A LOCKED DOOR',\
            'DROP: DROP FOLLOWED BY ITEM NAME ALLOWS YOU TO DROP THAT ITEM E.G DROP AXE',\
            'COUNTITEMS: TYPING THE WORD SCORE COUNTS THE NUMBER OF ITEMS YOU ARE HOLDING   - ', \
            'QUIT   - EXITS GAME',\
            'LOAD   - LOADS GAME',\
            'SAVE   - SAVES GAME',\
            'X2ANFAR   -TRANSPORTS PLAYER TO NEW LOCATION']

 
# These list may be useful in the future
#NounList = ['NORTH',   'SOUTH',  'WEST',   'EAST',    'UP',   'DOWN',
#            'DOOR',    'BATS',   'GHOSTS', 'X2ANFAR', 'SPELLS', 'WALL']

#PropList = ['DRAWER',  'DESK', 'COAT', 'RUBBISH', 'COFFIN', 'BOOKS']

#PositionOfProps = [43, 43, 32, 3, 38, 35]

#items available
ItemList = ['PLANK OF WOOD', 'RING',      'MAGIC SPELLS', 'GOBLET', 'SCROLL', 'COINS', 'STATUE',  'CANDLESTICK', 'MATCHES',
            'VACUUM',   'BATTERIES', 'SHOVEL',       'AXE',    'ROPE',   'BOAT',  'AEROSOL', 'CANDLE',      'KEY']
#GLOBAL VARIABLES TO SAVE

#location of items available
PositionOfItems = [24, 38, 35, 50, 14, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 100, 100]

#Vistited locations which gets added to each time player moves some how linked to building up the map 
VisitedLocations =[0]
location = 0
theLocation =[0]

#############################################################################################################
# HELPER FUNCTIONS                                                                                          #
#############################################################################################################


# New Name Function is there a space in this sentence?
# Input = string
# Processing = does the string contain space?
# Output = T or F

def isMultiwordStatement(value):
    return value.find(" ") != -1

# Input = ItemID = int = which is the unique int in the list ItemList that identifies each item eg panting = [46]
# Input2 = currentLocation = int = which is the current location 
# Processing = is current location == location of item within ItemList
# Output returns T or F
# i.e PositionOfItems[46] == [46] would return true

def isItemAvailableAtLocation(ItemID, currentLocation):
    return PositionOfItems[ItemID] == currentLocation

# Input        = itemName = string
# Processing   = String gets inputed into def GetItemID assigns that int to ItemID
# Output       = Returns T or F depending on if ItemID == 999

def isItemInInventory(itemName):
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == HERO_INVENTORY_POS

# Input        = itemName = string
# Processing   = String gets inputed into def GetItemID assigns that int to the variable ItemID
# Output       = Returns T or F depending on if ItemID == 100
 
def isItemHidden(itemName):
    # 100 is the location for hidden items. 
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == 100


# Input = String
# Processing = for loop which finds the location of item i.e "KEY" = 17 location in the list Item list but not its lcation on the map i.e 100
# Output = int location of string within ItemList
def GetItemID(item):
    for ItemID in range(0, len(ItemList), 1):
        if item == ItemList[ItemID]:
            return ItemID
    return -1


def contains(validValues, values):
    """
    Function: contains
    validValues: a string containing all the valid characters allowed
    values: a string that need to be checked (to see whether it contains only valid characters)
    """
    validCount = 0
    lengthValues = len(values)
    for letter in validValues:
        for character in values:
           if letter == character:
                validCount=validCount+1
    return validCount == lengthValues


def isAlphabetic(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return contains(alphabeticCharacters, value)

def isValidName(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ &-"
    return contains(alphabeticCharacters, value)



#############################################################################################
# GAME LOGIC                                                                                #
#############################################################################################

#How the game works#
# Inputs
# 1 -- direction which can be NSEW or GO
# 2 -- verb which can be anything from the verbList
# 3 -- noun which can be anything from the nounList
# 4 -- examine 

# Processing What has the user entered?
# 1 --  is it a direction? if so I need to do functions relating to moving
# 2 --  is it a verb if so I need to do functions relating to the verb
# 3 --  is it a noun if so I need to do fuctions relating to the noun 

# Outputs
# 1 -- if a direction was entered it will out put 
#YOU ARE LOCATED IN A  DARK CORNER (0)   DARK CORNER     (0) = current location
#VISIBLE EXITS:  SE = directionsList[0]
#WHAT DO YOU WANT TO DO NEXT?s =statement
#YOU MOVED FROM DARK CORNER= LocationsList[0]  TO CORNER OF HOUSE  = LocationsList[8 ]



# This Function is to do with userInput and finding the space within it
# Input = String = statement 
# Processing = if string does not contain space return the sentence
# Processing2 = calls NOT isMultiwordStatement(sentence) which means if there is
# a " " in the sentence it will return false and if there is not " " return true
# Processing3 if there is space fuction will find it and splice the location where the
# space occurs capturing just the first word

def GetVerbFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return sentence
    locationOfSpace=sentence.find(" ")
    return sentence[:locationOfSpace]
# This fuction does the same as above but captures the second word after the space

def GetNounFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return ""
    locationOfSpace=sentence.find(" ") + 1
    return sentence[locationOfSpace:]



# is movement available 
# Input= string = N,S,E,W input2= int 63
# Processing = Which ever number current location is at find that same location on in the DirectionsList and make what
# ever is inside that list = to dirString e.g if current location was 15 dirString would == NSW
# Processing2 = Checks to see if dirString contains directioncharacter and assigns to variable result
# Processing3 = if dirString does contain directioncharacter then it will return at which intext it is located if it does not 
# contain it will print -1
# Output = the result is then evaluated and if it is >= 0 it will return True else False


def isMovementAvailable(directioncharacter, currentLocation):
    """
    isMovementAvailable checks whether it is possible to move in a direction in the current location


    directioncharacter - intended direction to move toward at the currentLocation
    returns True or False - based on whether the directioncharacter can be found in the String from DirectionsList[currentLocation]

    Example: 
    if directioncharacter is 'N' and DirectionsList[currentLocation] is 'NSW', this function returns True
    """
    
    dirString = DirectionsList[currentLocation]
    result = dirString.find(directioncharacter)
    if result >= 0:
        return True
    else:
        return False
    
# Input = String =
# Processing
def isMovementVerb(verb, noun):
    
    return verb == 'N' or verb == 'S' or verb == 'E' or verb == 'W' or verb == 'U' or verb == 'D' or verb == 'GO'

#I don't think the function is currently being used
# Takes a statement
# Splits it into noun and verb 1st word second word
# if len verb = 1 i.e W return string "w"
# if verb  == 'GO' return the first letter of the second word inputed(noun)
# This means if you type GO then west it will see it as go w

def GetMovementDirection(statement):
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)
    if len(verb)==1:
        return verb
    if verb == 'GO':
        return noun[:1]
    return ''

# score must be == 5 
def isEndOfGame(score, currentLocation):
    return score == 5 and currentLocation == 0
# calculates score
def GetScore():
    score = 0
    for name in ItemList:
        if isItemInInventory(name):
            score +=1
    return score
    
#############################################################################################
# END GAME LOGIC                                                                            #
#############################################################################################

#############################################################################################
# BEGIN PRESENTATION LOGIC                                                                  #
#############################################################################################

def DisplayCongratulation():
    print(""" CONGRATULATIONS YOU FOUND THE GOLDEN POLAR BEAR
 __     __                    _       
 \ \   / /                   (_)      
  \ \_/ /__  _   _  __      ___ _ __  
   \   / _ \| | | | \ \ /\ / / | '_ \ 
    | | (_) | |_| |  \ V  V /| | | | |
    |_|\___/ \__,_|   \_/\_/ |_|_| |_|
                                      
 """)
#Prints VerbList to player
def DisplayHelpMessage():
    
    print("I UNDERSTAND THE FOLLOWING WORDS:")
    
    for words in VerbList:
        print(words)
        
# When a player picks up a item it changes it's value to 999
# This fuction checks if the list PostionOfItems == 999
# If it does contain 999 it adds it to strItems variable and prints on screen
# Else it prints string "nothing"
def DisplayInventory():
    strItems=[]
    for i in range(len(PositionOfItems)):
        if PositionOfItems[i] == HERO_INVENTORY_POS:
            strItems.append(ItemList[i])
    
    if len(strItems) == 0:
        strItems = "NOTHING"
    
    print("YOU ARE CARRYING:")
    for i in strItems:
        print(i)
    

# trasports user from current location to new location
def DisplayMagicMessage(currentLocation, newLocationID) :
    print ("YOU UTTER WORDS OF DARK MAGIC... X2ANFAR!")
    print ("YOU DISAPPEAR AND REAPPEAR IN ANOTHER LOCATION...")
    print ("YOU WERE IN " + LocationsList[currentLocation])
    print ("YOU ARE NOW IN " + LocationsList[newLocationID])



def DisplayMap():

    """
     Each row of the map is consisted of 3 lines
     The first line - contains exit to North
     The second line - contains exits to West and East plus room no.
     The third line - contains exit to South
     
    """
    Line1 = ""
    Line2 = ""
    Line3 = ""
    # Use a FOR loop to draw every room this loop compaires the number of items of two lists visitedLocations and directionsList
    # for example if there is 3 items in the vistitedLocations list and three items in the directionsList then it would read the NSEW inside the
    # items and would draw lines according to what NSEW was in the list
   
    #
    currentlocaion = 2
    for Index in range (0, 64, 1):
        if Index in VisitedLocations:
            # assign the exits at location 'Index' to currentValues
            # e.g. "NSW" if there are exits to North, South, and West
            currentValues=DirectionsList[Index]
            # Assigns what ever is in directionList to currentValues
            # Then depending on what letters are in that location in direction list will draw walls
            
            if "N" in currentValues:
                Line1 += "█  █"
            # otherwise, draw a wall
            else:
                Line1 += "████"
            #this deals with what is printed where the number is so this is where work needs to be done with **    
            if "W" in currentValues:
                Line2 += (" ") + PrintableInts(Index)
            else:
                Line2 += ("█") + PrintableInts(Index)
            
                
            if "E" in currentValues:
                Line2 += " "
            else:
                Line2 += "█"

            if "S" in currentValues:
                Line3 += "█  █"
            else:
                Line3 += "████"
        else:
            Line1 += "    "
            Line2 += "    "
            Line3 += "    "
        # Draw the first row of rooms if 8 rooms have been processed.     
        if (Index + 1) % 8 == 0:
            print (Line1)
            print (Line2)
            print (Line3)
            # Emptying the lines for the next row of 8 rooms.
            Line1 = ""
            Line2 = ""
            Line3 = "" 
                                
 # all these functions deal with the verb "EXAMINE" the basic format is
 # Input = current location
 # Processing = is current location == postion on the map
 # Output = if it is == to some locaiton on the map do something else do something else
def ExamineCoat(currentLocation):
    if currentLocation == 32 and isItemHidden("Key"):
        PositionOfItems[GetItemID("KEY")] = 32
        print ("YOU EXAMINE THE COAT AND FIND A KEY IN THE POCKET")
    elif currentLocation == 32 and not isItemHidden("Key"):
        print ("IT\'S A DIRTY OLD COAT")
    else:
        print ("WHAT COAT?")


def ExamineDrawer(currentLocation):
    if currentLocation == 43 and isItemInInventory("KEY") :
        print ("YOU UNLOCK THE DRAWER AND FIND IT IS EMPTY")
    elif currentLocation == 43 and not isItemInInventory("KEY") :
        print ("UNFORTUNATELY THE DRAWER IS LOCKED")
    else:
        print ("WHAT DRAWER?")

    

def ExamineRubbish(currentLocation):
    if currentLocation == 3:
        print ("THE RUBBISH IS FILTHY")
    else:
        print ("WHAT RUBBISH?")

def ExamineWall(currentLocation):
    if currentLocation == 43:
        LocationsList[currentLocation] = "STUDY WITH DESK"
        DirectionsList[currentLocation]="NW"
        print ("YOU LOOK AT THE WALL AND DISCOVER IT IS FALSE!\nYOU DISCOVER A NEW EXIT")
    else:
        print ("NO INTERESTING WALLS HERE")

def ExamineDoor(currentLocation):
    if currentLocation == 28 and  isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print ("YOU UNLOCK THE DOOR AND DISCOVER A NEW LOCATION!")
    elif currentLocation == 28 and  not isItemInInventory("KEY"):
        print ("UNFORTUNATELY THE DOOR IS LOCKED")
    else:
        print ("NO INTERESTING DOOR HERE")

def CutDownDoor(currentLocation):
    if currentLocation == 3 and isItemInInventory("AXE"):
        DirectionsList[currentLocation]="SWE"
        print ("YOU CUT DOWN THE DOOR AND DISCOVER A NEW LOCATION!")
    elif currentLocation == 28 and  not isItemInInventory("KEY"):
        print ("HMM THE WALL LOOKS THIN MAYBE AN AXE COULD CUT IT DOWN")
    else:
        print ("NO INTERESTING DOOR HERE")

def UseScroll(currentLocation):
    if currentLocation == 23 and isItemInInventory("SCROLL"):
        DirectionsList[currentLocation]="NS"
        print ("YOU UTTER THE MAGIC WORDS FROM THE SCROLL AND THE DOOR OPENS")
    
    

def ExamineBooks(currentLocation):
    if currentLocation == 42 and isItemHidden("CANDLE"):
        print ("YOU LOOK AT THE BOOKS AND FOUND A CANDLE IN BETWEEN BOOKS!")
        PositionOfItems[GetItemID("CANDLE")] = 42
    elif currentLocattion == 42 and not isItemHidden("CANDLE"):
        print ("THE BOOKS LOOK EVIL")
    else:
        print ("NO BOOKS HERE")
        
def DoExamine(currentLocation, noun) :
    if noun == "COAT":
        ExamineCoat(currentLocation)
    elif noun == "DRAWER":
        ExamineDrawer(currentLocation )
    elif noun == "RUBBISH":
        ExamineRubbish(currentLocation)
    elif noun == "WALL":
        ExamineWall(currentLocation)
    elif noun == "DOOR":
        ExamineDoor(currentLocation)
    elif noun == "BOOKS":
        ExamineBooks(currentLocation)
    
    else:
        print ("WHAT "+noun+"?")

def beenThere():
    global VisitedLocations 
    VisitedLocations = [] 
    for i in range(0,64): 
        VisitedLocations.append(i) 
          
# This Function is concerned with output format
# if the location is less than 10 it adds a space prints the position of the player
# current values =  directionList[index] = directionList[index] are equal to

def PrintableInts(value):
    
    if (value == theLocation[-1]):
        return ""+str("**")
    elif(value<10):
        return " "+str(value)
    return str(value)


def Dig(currentLocation):
    if currentLocation == 30 and isItemInInventory("SHOVEL"):
        DirectionsList[currentLocation]="NSE"
        LocationsList[30] = 'HOLE IN WALL'
        print ("YOU DIG AROUND THE ROOM. THE BARS IN THE WINDOW BECOME LOOSE! REVEALLING A NEW EXIT!")
    elif isItemInInventory("SHOVEL"):
        print ("YOU DIG A LITTLE HOLE.")
    else:
        print ("YOU HAVE NOTHING TO DIG WITH")

#############################################################################################
# END PRESENTATION LOGIC                                                                    #
#############################################################################################

# Input = current location
# Processing = if position of items  == current location
# Output = return the name of the item
def ListItemsAtPosition(currentLocation):
    strItems=""
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            strItems = strItems + " "+ ItemList[i]
    return strItems
# Input = current location
# Processing = if position of items == current location returns true that the function above will execute soon after
def ItemsAvailableAtPosition(currentLocation):
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            return True
    return False

# this is what happens when the spell is uttered 
def GoMagic(currentLocation):
    newLocationID=currentLocation
    while(newLocationID == currentLocation):
           newLocationID = random.randint(0,63)

    return newLocationID;

def BackToBeginning(location):
    print ("AS YOU TRAVELED BETWEEN LOCATIONS YOU SLIPED THOUGH A CRACK IN THE FLOOR BACK TO THE BEGINNING FOR YOU")
    location = 0
    return location
    

# Input = String, int
# Processing = separates the noun and the verb
# Processing2 = Creates variable direction character
# Processing3 = If verb = go assign the first letter of the noun (second word inputed) to variable direction character
# Processing4 = if direction charater = NSEW currentlocation = currentlocation + -8,8,-1,1 an amount
# Output = returns int currentlocation
# i.e if currentLocation = 0 and player put in "go east"
# Output would be 0 + 1 = 1

def Go(statement, currentLocation):

    
    directioncharacter = ''
     
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)

    directioncharacter = verb
    
    if verb == 'GO':
        directioncharacter = noun[:1]
        
    if isMovementAvailable(directioncharacter, currentLocation):
        
        if directioncharacter == 'N':
            currentLocation -= 8
        elif directioncharacter == 'S':
            currentLocation += 8
        elif directioncharacter == 'W':
            currentLocation -= 1
        elif directioncharacter == 'E':
            currentLocation += 1
    return currentLocation

# GET ITEM CODE
# Input = String, int
# Processing = Passes string to GetItemID which will return the location of the item in the item list assings that int to variable ItemID
# Processing2 = Passes variable ItemID to isItemAvailableAtLocation
# Processing3 if it returns true will changes the value of the item from whatever its value in the PostionofItems list to a new value 999
# Output = "you are now carring a " item else sorry you cannot take a XX
# I.E = noun AXE currentLocation = 2 isItemAvailableAtLocation returns true PositionOfItems[ItemID] where AXE was is now 999
# PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 100, 100]
# Changes to PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, """999""", 7, 47, 60, 100, 100]
def GetItem(noun, currentLocation):
    ItemID = GetItemID(noun)
    if isItemAvailableAtLocation(ItemID, currentLocation):
        PositionOfItems[ItemID]=HERO_INVENTORY_POS
        print("YOU ARE NOW CARRYING A",noun, file=sys.stderr)
    else:
        print("SORRY YOU CANNOT TAKE A ", noun)

# similar to above function except I.E  Input = AXE, 44
# # PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 100, 100]
# changes to PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, """44""", 7, 47, 60, 100, 100]

def DropItem(noun, currentLocation):
    ItemID = GetItemID(noun)
    if isItemAvailableAtLocation(ItemID, HERO_INVENTORY_POS):
        PositionOfItems[ItemID] = currentLocation
        print("YOU HAVE DROPPED THE ", noun)
    else:
        print("YOU CANNOT DROP THAT WHICH YOU DO NOT POSSESS")
#Similar to examine functions
def OpenDoor(currentLocation):
    if currentLocation == 28 and isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print("THE DOOR IS NOW OPEN! REVEALLING A NEW EXIT!")
    else:
        print("THE DOOR IS LOCKED")

def allItemsCheat():
    for index, item in enumerate(PositionOfItems):
        PositionOfItems[index] = 999

def clearLocationHistory():
    global VisitedLocations
    VisitedLocations = []
    VisitedLocations.append(0)

def beenThere():
    global VisitedLocations
    VisitedLocations = []
    for i in range(0,64):
        VisitedLocations.append(i)
    
    
def DoCheat(noun):
    
    ItemID = GetItemID(noun)
    PositionOfItems[ItemID]=HERO_INVENTORY_POS
    print("YOU ARE NOW CARRYING A",noun, file=sys.stderr)

def save():
    print("YOU HAVE SAVED THE GAME")
    print(PositionOfItems,VisitedLocations,location)

    lister=[PositionOfItems,VisitedLocations,location,DirectionsList]
    output = open('hant2.txt','wb')
    pickle.dump(lister, output)
    output.close()

def load():
    global PositionOfItems
    global VisitedLocations
    global location
    global DirectionsList
    global currentLocation
    
    print("LOADING")
    inputFile = open("hant2.txt", 'rb')
    example = pickle.load(inputFile)
    PositionOfItems = example[0]
    VisitedLocations = example[1]
    location = example[2]
    currentLocation = location
    DirectionsList =example[3]
    inputFile.close()

def ProcessStatement(statement, currentLocation):
    '''
      A statement can be either a verb or a verb + a noun
      If a statement is consisted of 1 verb and 1 noun, (separated by a space), it can looks like 'examine desk', 'get axe' ..etc
      There is also a quit statement which when typed in quits the game
    '''

    
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)    

    if verb.upper()== "HELP":
        
        DisplayHelpMessage()

    elif verb =="CLEAR":
        clearLocationHistory()
        
    elif verb =="BEENTHERE":
        beenThere()
    
    elif verb == "SCORE":
        print("YOUR CURRENT SCORE IS:", GetScore())

    elif verb == "CARRYING" or verb == "CARRYING?" or verb == "INVENTORY" or verb == "INV":
        DisplayInventory()

    elif verb == "GET" or verb == "TAKE":
        GetItem(noun,currentLocation)

    elif ((verb == "OPEN" or verb == "UNLOCK") and noun == "DOOR") or (verb =="USE" and noun == "KEY"):
        OpenDoor(currentLocation)
        
    elif (verb == "USE") and (noun == "AXE"):
        CutDownDoor(currentLocation)

    elif (verb == "USE") and (noun == "SCROLL"):
        UseScroll(currentLocation) 
        
    elif verb == "DIG" or (verb =="USE" and noun=="SHOVEL"):
        Dig(currentLocation)

    elif verb == "DROP":
        DropItem(noun, currentLocation)

    elif verb == "EXAMINE":
        DoExamine(currentLocation, noun)

    elif verb == "SAY" and noun == "X2ANFAR":
        newLocationID = GoMagic(currentLocation)
        DisplayMagicMessage(currentLocation, newLocationID)
        currentLocation = newLocationID

    elif verb == "SHOW" and noun == "MAP" or verb == "SS":
        DisplayMap()

    elif verb == "QUIT":
        quit()

    elif verb == "SAVE":
        save()
    elif verb=="LOAD":
        x=input("If you do not have  a previous save - program will crash are you sure you want to load? Y/N").upper()
        if x == "Y":
            load()
        
 
        
    elif verb == "GIVEITTOME":
        
        print("POSSIBLE ITEMS TO GET:", )
        for words in ItemList:
            print(words,end=", ")
        noun = input("NAME THE ITEM YOU NEED").upper()
        DoCheat(noun)
    
 
    elif verb == "GOODSTUFF":
        print("you are correct, here are all items as a reward")
        allItemsCheat()
    

    elif isMovementVerb(verb, noun):  
        newLocationID = Go(statement, currentLocation)
        if currentLocation != newLocationID:
            print("YOU MOVED FROM " + LocationsList[currentLocation] + " TO " + LocationsList[newLocationID], file=sys.stderr)
        else:
            print("YOU ARE UNABLE TO MOVE IN THAT DIRECTION")
        currentLocation = newLocationID


    return currentLocation

def checkUserInput():
    actions =["Welcome to the game press enter to get started "]
    

    
    for i in actions:
        print(i)
    
    x = input("").upper()
    
    while 1<2:
        x=input("Please chose the following options: 'N' for New Game 'C' to continue from previous save 'Q' for Quit").upper()
        if x=='N':
            break
        elif x == 'C':
            x=input("If you do not have  a previous save - program will crash are you sure you want to load? Y/N").upper()
            if x == "Y":
                load()
                break
            
        elif x == 'Q':
            quit()
        else:
            x=input("Not a valid option please hit enter").upper()
    else:
        print("Input Accepted\n\n")
    print("HOW TO PLAY HANTED HOUSE:")
    print("THE AIM OF THE GAME IS TO FIND THE SECRET ROOM IN THE HANTED HOUSE")
    print("TO PICK UP AN ITEM USE THE WORD GET FOLLOWED BY THE ITEM NAME")
    print("TO USE AN ITEM USE THE KEYWORD USE FOLLOWED BY THE ITEM NAME I.E GET AXE... USE AXE")
    
#location is a local variable 
def Game():
    global location
    location = 0
    checkUserInput()
    while not isEndOfGame(GetScore(),location):
        
        
        
        print("========Haunted House=========")
        print("YOU ARE LOCATED IN A ", LocationsList[location],"("+str(location)+")")
        if ItemsAvailableAtPosition(location):
            print("YOU CAN SEE THE FOLLOWING ITEMS AT THIS LOCATION: ", ListItemsAtPosition(location))
        DirectionsList[location]
        if "N" in DirectionsList[location]:
            print("VISIBLE EXSITS UP")
        if "S" in DirectionsList[location]:
            print("VISIBLE EXSITS DOWN")
        if "E" in DirectionsList[location]:
            print("VISIBLE EXSITS RIGHT")
        if "W" in DirectionsList[location]:
            print("VISIBLE EXSITS LEFT")
            
        
        statement = input("WHAT DO YOU WANT TO DO NEXT? W= UP S= DOWN A= LEFT D= RIGHT\n\n").upper()
        if statement == "W":
            statement = "N"
        elif statement == "S":
            statement = "S"
        elif statement == "D":
            statement = "E"
        elif statement == "A":
            statement = "W"
            
         
                
        
        location = ProcessStatement(statement, location)
        theLocation.append(location)
        if location == 23 and "N" in DirectionsList[23] and "X" in DirectionsList[23]:
            print("LOOKS LIKE SOMETHING ON THE OTHERSIDE OF THE CLIF MAYBE A MAGIC SCROLL WOULD HELP TO GET TO THE OTHER SIDE")

        if location ==11 and 999 != PositionOfItems[0]:
            location = 0
            print ("OH KNOW YOU FELL DOWN A HOLE BACK TO THE BEGINNING FOR YOU IF ONLY YOU HAD A PLANK OF WOOD TO COVER THE HOLE WITH")
        elif location == 11 and 999==PositionOfItems[0]:
            print("LUCKY YOU PICKED UP THAT PLANK OF WOOD NOW YOU CAN CROSS SAFELY")
       
        
        if location ==53:
            location = BackToBeginning(location) 
        elif location ==60:
            location = BackToBeginning(location)
        
            
        elif location ==46:
            break
            
        if not (location in VisitedLocations):
            VisitedLocations.append(location)
        
        DisplayMap()
        

        
    DisplayCongratulation()
Game()

