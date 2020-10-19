"""Mission Bones Randomizer
This program untilizies a random d6 to generate potential
missions or objectives for an RP.  The results are bare
bones that can then have the meat of details put on as
per the RP in question.

Original guide for system: OBJECTIVERANDOMIZER.odt by 13Swords
Progamming done by Hailed Manic

Version D
Date: 10/7/020

1.1     Objectives are created and stored in a temp txt file, then printed results
1.2     Objectives can now be saved in a file named by the user; temp file is cleared up on closure
1.3     Enhancements to saving functionality:
            -Shows default save folder (where program is located)
            -Shows instructions to save to another directory
            -Checks if directory is valid for saving
1.4     Resolved crash issue
            -Program would crash when attempting to save to a nonexistent directory
            -Added parsing section to Save Module that determines if the directory is valid

===== ===== =====

NOTICE: This program was made before I learned of certain techniques that can be used with opening
files.  As such, there is plenty of space where optimization can be made."""

from random import randrange
from os import system
import os

#from rdoclient import RandomOrgClient


# Objective List; "Chain Mission" covered in Chain Mission buffer
lstObj = ["Locate",
          "Secure",
          "Escort to",
          "Destroy",
          "Sabotage"]

# Lists for Universal Complicatiosn; Ally, Enemy, and Conflict
lstUni = [["No Allies", "Inept Allies", "Allies are Known Enemies", "Allies will betray players", "Allies will disobey", "Allies have other prioities"],    #Ally
          ["Many Enemies", "Enemies have Hostages", "Enemy is known NPC", "3-way battle", "Unwilling Enemies", "Led by powerful leader"],                   #Enemy
          ["Innocents in corssfire", "Target belongs to neutral", "Others failed, dead or captured", "Bad Intel", "No Warning", "No Violence Allowed"]]     #Conflict

# Lists for Specific Complications; Person, Place, and Thing
lstSpe = [["Running", "Hiding", "Protected", "Kidnapped", "Disguised", "Impersonator"],                                                     #Person
          ["Hidden base inside", "Filled with Enemies", "Filled with Neutrals", "Den of Predators", "Heavily Fortified", "Well Concealed"], #Place
          ["Hidden", "Protected", "Naturally Dangerous", "Sapient", "Extremely Valuable", "Cheap Copy"]]                                    #Thing

# List of for 'What you learn'
# Five options, buffer for Roll 6
lstLearn = ["New plan of foe",
            "Exploit vs foe",
            "Location of foe's resource",
            "Foe's secret enemy or ally",
            "Foe's secret history"]

# Roll Module; six-side die
# Range from 0 to 5, still six possible outcomes
# but the range accomodates for the arrays
def d6():
    global counter
    global r
    counter = counter + 1
    num = randrange(0, 5)
    #roll = r.generate_integers(1, -1, 5)
    #roll = list(roll)
    #num = roll[0]
    return num

# Clean temporary file cache
def tempReload(c):
    if os.path.exists(c):
        os.remove(c)
    return

# Listing Module for Universal Complications
def uCompList(num, tempFile):
    for i in range(num):
        x = d6()
        y = d6()
        if x > 2:
            x = x - 3
        tempFile.write(" - " + lstUni[x][y] + "\n")
    return

#Listing Module for Specific Complications
def sCompList(num, t, tempFile):
    for i in range(num):
        x = d6()
        tempFile.write(" - " + lstSpe[t][x] + "\n")
    return
        
# Mission Target Module
# Identifies type of target
def target():
    lstTar = ["person", "place", "thing"]
    t = d6()
    if t > 2:
        t = t - 3
    return lstTar[t], t

# Universal Complications Module
# Counts the number of U-Comps there will be for the mission
# Defers to U-Comp maker for details and creating list
def comps():
    x = d6()
    val = 0
    while x > 2:
        val = val + 1
        if x < 5:
            x = 0
        else:
            x = d6()
    return val

# Mission generator
# Does not interfere with Chain Mission results
# num1 is a non 6 value
def genMission(num1, tempFile):

    # Objective and Target
    part1 = lstObj[(num1 - 1)]
    part2, tType = target()
    tempFile.write(part1 + " " + part2 + "\n")

    # Universal Complications
    num3 = comps()
    tempFile.write("Universal Complications: " + str(num3) + "\n")
    uCompList(num3, tempFile)

    # Specific Complications
    num4 = comps()
    tempFile.write("Specific Complications: " + str(num4) + "\n")
    sCompList(num4, tType, tempFile)
    return

# Generate What You Learn after completing misssion(s)
def reward(tempFile):
    x = 5
    c = 0   # Counter for 'Choose 1 and Roll Again'
    tempFile.write("\nWhat is learned: \n")
    while x == 5:
        x = d6()
        if x == 5:
            c = c + 1
        elif x < 5:
            line = lstLearn[x]
    if c != 0:
        tempFile.write("Choose " + str(c) + "\n")
    tempFile.write(line + "\n")
    return

# Chain Mission Buffer
# In the event of a 6 being rolled to begin with
def bufCM(tempFile):
    x = 5
    count = 0
    while x == 5:
        x = d6()
        if count == 0 and x == 5:       # For titling purposes
            tempFile.write("CHAIN MISSION")
        
        if count == 0 and x != 5:       # In the event of no chain
            tempFile.write("OBJECTIVE: \n")
        elif x == 5:                    # Chain Mission
            count = count + 1
            tempFile.write("\nMission " + str(count) + "\n")
        elif count != 0 and x != 5:     # Last Chain Mission
            count = count + 1
            tempFile.write("\nMission " + str(count) + "\n")
        genMission(x, tempFile)

    reward(tempFile)
    return

# ===== ===== =====
# Main Program
# ===== ===== =====
def mainObj(fileName):
    global counter  # Simple feature to count the number of times a die is rolled for the entire operation
    #global r

    """The following section is commented out.
    These are values and funtions to pull random numbers
    from http://random.org instead of the regular Python
    engine.  Those who dislike the pseudorandomness of
    Python may be inclined to outsource their random numbers
    from another place.

    For now, this will not be implemented.  A later version
    will include something to allow swapping between different
    random number generation engines."""
    #file = open("RandomOrgToken.txt", "r")
    #token = str(file.read())
    #r = RandomOrgClient(token)
    counter = 0
    tempReload(fileName)
    with open(fileName, "w") as F:
        bufCM(F)
    with open(fileName, "r") as F:
        res = F.read()
    print("Number of rolls made:", counter)
    #usage = r.get_requests_left()
    #print("Random.Org uses left:", usage)
    return res

# ===== ===== =====
# END OF MODULES
# ===== ===== =====


# Program is disabled from running by itself
# Modules are accessed via DiscordBones
