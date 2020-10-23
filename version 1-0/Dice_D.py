import random

# Dice roller; need to expand to allow different engines
def die(min, max):
    result = random.randint(min, max)
    return result

# Parse individual characters from input
# seperating numbers from characters and symbols
def parseCharacter(line):
    if line[0].isnumeric():
        isNumber = True
        counter = 0
        stop = len(line)
        while counter <= stop and isNumber is True:
            counter += 1
            isNumber = line[:(counter)].isnumeric()
        counter -= 1
        result = line[:counter]
        lineShave = line[counter:]
        formatError = False
    elif line[0] in ["D"]:
        result = line[0]
        lineShave = line[1:]
        formatError = False
    elif line[0] in ["+", "-"]:
        result = line[0]
        lineShave = line[1:]
        formatError = False
    else:
        result = ""
        lineShave = ""
        formatError = True
    return result, lineShave, formatError

# Parse the entire input line, using parseCharacter to chew
# through the input
def parseLine(line):
    formatError = False
    disectLine = []
    while formatError is False and line != "":
        value, line, formatError = parseCharacter(line)
        disectLine.append(value)
    return disectLine, formatError

# Take the parsed line and determine where the dice sets are
# Sets are broken up at the symbols '+' and '-'
def parseSets(values):
    stop = len(values)
    counter = 0
    sets = []
    tempSet = []
    while counter < stop:
        if values[counter] in ["+", "-"]:
            if tempSet == []:
                tempSet.append(values[counter])
            else:
                if not(tempSet[0] in ["+", "-"]):
                    tempSet.insert(0, "+")
                if tempSet[1] == "D":
                    tempSet.insert(1, 1)
                sets.append(tempSet)
                tempSet = []
        else:
            tempSet.append(values[counter])
        counter += 1
    if not(tempSet[0] in ["+", "-"]):
        tempSet.insert(0, "+")
    if tempSet[1] == "D":
        tempSet.insert(1, 1)
    sets.append(tempSet)
    return sets

# Roll each set of dice
def rollSets(dieSet):
    dieNum = int(dieSet[1])
    dieSize = int(dieSet[3])
    counter = 1
    numSet = []
    total = 0
    while counter <= dieNum:
        roll = die(1, dieSize)
        numSet.append(roll)
        total += roll
        counter += 1
    total = int(str(dieSet[0]) + str(total))
    return numSet, total

# Return flat value for a set
def flatValue(numSet):
    valueRead = int(str(numSet[0]) + str(numSet[1]))
    return valueRead

# Self-explanatory; contains some formating to look good
def printOutput(total, rolls, dice):
    stop = len(rolls)
    counter = 0
    printOut = ""
    while counter < stop:
        diceStop = len(dice[counter])
        diceCounter = 0
        diceSet = ""
        while diceCounter < diceStop:
            diceSet += str(dice[counter][diceCounter])
            diceCounter += 1
        printOut += str(str(diceSet) + " : " + str(rolls[counter]) + "\n")
        counter += 1
    printOut += ("Total: " + str(total))
    return printOut

# ===== ===== =====
# Main Module
# ===== ===== =====
def mainRoller(userLine):
    print(userLine)
    userLine = userLine.upper()
    userLine = userLine.replace(" ", "")
    disctLine = []
    diceSets = []
    disectLine, formatError = parseLine(userLine)
    if formatError is False:
        diceSets = parseSets(disectLine)
        stop = len(diceSets) - 1
        counter = 0
        total = 0
        rollResults = []
        while counter <= stop:
            if not("D" in diceSets[counter]):
                tempSum = flatValue(diceSets[counter])
                rollResults.append(tempSum)
            else:
                rolls, tempSum = rollSets(diceSets[counter])
                rollResults.append(rolls)
            total += tempSum
            counter += 1
        resultsLine = printOutput(total, rollResults, diceSets)
    else:
        resultsLine = "Formatting Error."
    return resultsLine

# ===== ===== =====
# End of Modules
# ===== ===== =====
#mainRoller()
