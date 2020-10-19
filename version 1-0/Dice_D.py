"""Dice Reader

This program is designed to take input from the user
and convert it into correct diceroll requests.  The
engine for dicerolls will draw from Python.

In the future, the dice engine should utilize external
sources for rolls with internal sources as a backup.

Version: Beta"""

import random
import ast

# This module acts as the defalut roller for any
# die rolls run in the system
def die(mi, ma):
    x = random.randint(mi, ma)
    return x

# This module is designed to chew up and whittle
# down the input string to find how many die of
# what size need to be rolled.
# Returns the remaining string and the roll list.
def parseDie(line):
    posD = line.find("D")                   #Determins where the D is for the die set
    try:
        dice = int(line[:posD])
    except:
        dice = 1
    line = line[posD + 1:]

    posP = line.find("+")   #Position of next Plus
    posN = line.find("-")   #Position of next Negative
                            #In the event of no sign found, a vlaue of -1 is returned
    move = 1
    size = 1

    """
    This next section takes the results of finding a '+' or '-' sign
    and sorts out what needs to be done.
        - First statement is the result of no '+' or '-' signs present
        - Second statement is to find if the '-' sign is first
            + Due to the -1 value given when no sign is found, special care
                is needed in the statements, hence the complexity
        - Third statement is to find if the '+' sign is first
            + As with the Second Statement, the complexity is due to the
                value given when no sign is found
    """
    if posP == -1 and posN == -1:
        size = int(line)
    elif (posP < posN and posP != -1) or (posP > posN and posN == -1):
        size = int(line[:posP])
        move = posP
    elif (posN < posP and posN != -1) or (posN > posP and posP == -1):
        size = int(line[:posN])
        move = posN 

    line = line[move:]
    roll = []
    while dice > 0:
        roll.append(random.randint(1, size))
        dice = dice - 1
    return line, roll

# This modulde takes the line and parses if
# the first character is a '+' symbol.  If a
# plus sign is found, it returns 'True'.  No
# plus sign returns a 'False'.
def parsePlus(line):
    if line[0] == "+":
        sign = "+"
        line = line[1:]
    elif line[0] == "-":
        sign = "-"
        line = line[1:]        
    return line, sign

# This module has the sole pupose to parsing
# if the remains of the string can be converted
# into an interger for addition/subtraction
def parseAdd(line):
    try:
        x = int(line)
    except:
        x = 0
    return x

# Here is the main module, pulling all the componants together
# It can be divided into three sections, each of which involve
# opening up the temp file and doing something with it.
def mainRoller(fileName = "tmp.txt", string = "12d - 3d6 - 10"):
    add = 0
    nums = []
    
    string = string.upper()                         #This is to make all characters uniform
    string = string.replace(" ", "")                #This will chop out all spaces

    """In this first section, the temp file is opened up in "write" mode.  This
    mode will allow the program to overwrite the current temp file.  (If
    there is no such file, a new one will be created, instead)
    This secion will also take the input line and begin to chew it up.  As
    Each piece is examined and deducted, the results are written into the
    temp file."""
    with open(fileName, "w") as F:
        while string != "":                         #If the string is empty, there is nothing left to process
            try:
                string, sign = parsePlus(string)    #ORDER! Checking for sign MUST be first.  If not, then...
                if sign == "-" or sign == "+":      #... it can result in the program trying to find a D...
                    string = string[0:]             #...and missing out on the positive or negative value of
            except:                                 #...the section.
                string, sign = string, "+"

            try:
                string, nums = parseDie(string)     #Read the die set; marked with 'try' in case there is...
            except:                                 #...improper formatting causing a crash.
                return

            # After the rolls are made, the positive or negative value is inserted at
            # the front of the list for easy access later on.
            nums.insert(0, sign)
            
            if string.find("D") == -1:      #Checks for no more dice sets existing
                loop = 1                    #Closes loop
                add = parseAdd(string)      #Grabs final number
                string = ""                 #Empty the string out

            # Take the roll result list and add it to the file.
            # The '\n' ensures a new line is ready for the next pass.
            F.write(str(nums) + "\n")

            # If there is a value for final flat number, then it
            # will be added here.
            if add != 0:
                F.write(str(add) + "\n")

    """This file opening sets the temp file in a "read" mode.  The lines are
    extracted from the file and turned into a list which can then be processed.
    The steps involved where a little complicated the first time around for me."""
    with open(fileName, "r") as A:
        finalNum = 0
        countA = 0

        lines = [line.rstrip("\n") for line in A]   #Clean up the 'whitespace' from the txt
        length = len(lines)

        """Due to how the file is structure akin to a two-dimensional array, it
        becomes a little more difficult to handle it properly."""

        # First loop here is to handle the file's contents line by line.
        # The current line is transcribed to a variable as a new list
        while countA < length:
            # This command reads the content LITERALLY.
            # This is why the whitespace needed to be cleaned up, earlier.
            nums = ast.literal_eval(lines[countA])
            count = 1

            # This section includes a 'try' here due to the possible error
            # with measuring the 'length' of an integer.  When the program
            # comes to the final, flat number, it will crash on 'len()'.
            # 'try' prevents the crash and redirects the system to simply
            # add the flat number to the final number.
            try:
                stop = len(nums)
                stop = int(stop) - 1
                while count <= stop:
                    if nums[0] == "+":
                        finalNum = finalNum + nums[count]
                    elif nums[0] == "-":
                        finalNum = finalNum - nums[count]
                    count = count + 1
            except:
                finalNum = finalNum + nums
            countA = countA + 1

    """This section opens up the temp file in "append" mode.  This will ensure
    no data is lost, as the information will be written to the end of the file.
    It takes the value of the sum as found in the previous section and tacks it
    to the end."""
    with open(fileName, "a") as F:
        F.write("Sum: " + str(finalNum))

    """This final section is simple enough.  It opens the file in "r" mode for
    reading.  Normally, the results would be in a 'print()' to display.
    In this case, we need to send it to a string variable to return to the bot."""
    with open(fileName, "r") as F:
        finalResult = F.read()

    return finalResult

# ===== ===== =====
# Main Program
# ===== ===== =====
def main():
    print("""Welcome to Dice Bones.
Please enter the dice you want to roll.
To exit, leave input blank and press ENTER.""")
    run = 0
    file = "tmp.txt"
    while run == 0:
        x = str(input())
        if x != "":
            mainRoller(file, x)
        else:
            run = 1
    print(x)

# ===== ===== =====
# End of modules
# ===== ===== =====

#Disable main() when program is used for Discord Bot
#main()
