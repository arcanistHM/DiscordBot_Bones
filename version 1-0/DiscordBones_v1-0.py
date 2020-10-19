"""Discord Bones

Welcome to the Discond bot: Bones.
Basic           BBBBB     OO    N   N  EEEEE   SSS
Open            B    B   O  O   NN  N  E      S
Nominal         BBBBB   O    O  N N N  EEE     SS
Essentials      B    B   O  O   N  NN  E         S
System          BBBBB     OO    N   N  EEEEE  SSS

The purpose of this program is not solely for being a Discord-interfaced RolePlaying aid.
This program is meant to also function as a guide to utilizing Discord API in Python.
Everything that is done in this program is carefully noted in as concise and descriptive
as I can.  So long as one has a basic understanding of Python language, you should be able
to learn what each function does and implement it in your own designs.

Additionally, this is a good learning tool for myself.  If I can properly explain what
everything does, then it reinforces my OWN learning of the systems.

I do advocate that if you create your Discord bot, please do NOT outright copy/paste this
code into yours.  At the very least, type it all out for yourself.  I believe putting in
that sort of effort goes a long way towards getting a full grasp over any topic.

==== ==== ====

The Bones programs are derived from systems created by 13 Swords.
All programming to create the Bones programs are by Hailed Manic.

Version: 1-0
Date: 10/18/2020
"""

import asyncio, discord, os, shutil
"""Importing these modules:
    - asyncio : Asynchronous I/O; used in framework for network
    - discord : Discord API
    - os : Basic file operation; i.e. opening/reading/writing files
    - shutil : High-level file operation; i.e. creating/removing folders

Vestigial
    - sys : 'System-specifical parameters and functions'
    - time : Time-related functions; i.e. Sleep, check machine time
"""

from discord.ext import commands
from discord.ext.commands import Bot
from ObjBones_D import *
from Dice_D import *
"""Additional imports:
    - These two are nessecary to run the bot program and handle commands
        + discord.ext : commands
        + discord.ext.commands : Bot
    - These pull modules from other Bones projects to use in the bot; the program will look in the same
        folder as itself for these
        + ObjBones_D : *
        + Dice_D : *

Vestigial
    - Sends orders to the command line
        + os : system
"""

# ===== ===== =====
# BEGIN MODULES
# ===== ===== =====
"""During the execution of the code, there are print() lines added in to
provide feedback to the operator and report what is happening while the
bot is in use."""

# Check for valid token on file.
# If there is no token on file or the token is not a valid length
# then the operator will be given a chance to create/amend the token.
# Failure to provide a valid token will result in this module returning
# a fail value of '0'.
def checkToken():
    x = 0
    while x == 0:
        print("Loading token...")
        if os.path.exists("key.txt"):                   #A token is needed run any Discord bot.  These are free to acquire from http://discord.com/devleopers/applicaions
            print("\'key.txt\' located \nExtracting...")
            with open("key.txt", "r") as file:          #Temporarily open the key.txt file (in the same directory as this program) and grab the token
                t = file.read()
            l = len(t)
            print("Checking key length")
            if l == 59:                                 #As of 10/18/2020, I believe all bot tokens are 59 characters in length.  Further reasearch is needed to confirm this
                print("Key of correct length found \nApplying...")
                x = 1                                   #Mark the loop for closure
            else:
                print("Key length not correct.\nPlease fix key.txt")
                y = fixToken()                          #Offer chance to fix token in-program
                if y != "Y":                            #If the operator declines to fix the toekn...
                    x = 1                                   #...the loop is marked for closure
                    t = 0                                   #...a failure value is marked
        else:
            print("No token file found.")
            y = fixToken()                              #Offer chance to create a token
            if y != "Y":                                #As above, if the operator declines to create a token...
                x = 1                                       #...the loop is marked for closure
                t = 0                                       #...a failure value is marked
    return t

# In-Program fix for bot token.
# The operator simply needs to input a clear 'Y' or 'N' for this module.
# (Capitalization does not matter)
# 'Y' will direct the operator to provide a token.
# 'N' carries on without creating/changing the 'key.txt' file.
def fixToken():
    x = 0
    print("Do you with to paste a new key? (y/n)")
    while x == 0:
        ans = str(input())
        ans.upper()                                 #Make any answer a uniform capital for easy reading
        if ans == "Y":
            key = str(input("Paste key now: "))     #Grab the new key from the operator
            with open("key.txt", "w") as file:      #Open/Create a file for the token and paste the key into it
                file.write(key)
            x = 1                                   #Valid answer received; marking loop for closure
        elif ans == "N":
            x = 1                                   #Valid answer received; marking loop for closure
    return ans

# Flush and create caching folder.
"""For memory purposes, this bot makes use of a cache to contain temporary files.
The purpose is to create one(1) temp file per User per Request Type.  This means that
every user can have one file of each type of recordable request sent to the bot.
    For example:
        > User A requests Objective
            >> UserATmpObj is made
        > User B request Objective and Diceroll
            >> UserBTmpObj is made
            >> UserBTmpDce is made
        > User A can request the file for their Objective
        > User B can request the file for their Objective and their Diceroll
        > Files persist in memory until overwritten by...
            >> ...a new request of the same type
            >> ...bot is shut down and rebooted
Utilizing a caching system makes it easier to manage the requests from multiple users.
"""
# This module creates a folder within the same directory as the program
# is running in to cache temporary files.  If a cache folder already
# exists, then it will be deleted, along with all the contents, BEFORE a
# new cache is created.
# Deleting the cache is meant to act as a space-saver and clean up old,
# unneeded files.
def cacheReload():
    if os.path.exists("caching"):       #Check for the cache folder
        shutil.rmtree("caching")        #Delete the cache along with ALL contents
        print("Purging Cache: \\caching\\")
    else:
        print("No leftover cache found")
    print("Creating cache folder...")
    os.mkdir("caching")                 #Create a new folder for the cache


# ----- ----- ----- ----- ----- -----
# Listing all possible commands and abilities give to the bot.
"""The next section contains the list of commands and responses the bot will be able to utilize.
Pay close attention to the exact commands used.  This is where things can get complicated very quickly.
'async' is very important here, as you don't want this to be read linearly.  The bot needs to be able
to receive any command at any time."""
# ----- ----- ----- ----- ----- -----
def botCommands(c):
    @c.event
    async def on_ready():
        print("Discord Bones is ready.")
        return

    """
    When creating a Command for the bot, there are a few features that can be packed into the command data.
    Do NOT try to create a 'help' command.  Discord API automatically integrates that command.  You can affect the
    information given in the 'help' response, though.
    Every command created will be listed in the 'help' response.  You can alter the meta data of the commands
    to give more helpful context.
        - name          : The title of the command; can be called with this name
                            + If none, it will default to the name given after 'async def'
        - description   : A longer (and hopefully better detailed) description of the command
                            + Accessed when someone calls 'help' and the command name
        - brief         : A short description that appears in the immediate help response
        - aliases       : A list of keywords that call the same command
                            + If there is a list given, it will ingore the name given after 'async def'
                            + The value for 'name' is part of this list and should NOT be repeated here
        - pass_context  : Allows for additional conditions before processing the command
                            + Normally, this should be set to True to allow the command
                            + Alternatively, this can be ignored when writing the meta data to keep it True and not
                                risk affecting it
    
    To make a command, there are two basic parts...
        @<prefix command>.command()
        async def <module name>(<context variable>):

    After the 'async def' line, indent as appropriate and write in the code for how the program should respond to
    the received command.
    """
    # Basic 'hello' test command
    @c.command(name = "Hello",
               description = "Sends a 'hello' back as a basic, low-level system test",
               brief = "Receive a hello test back",
               aliases = ["hello", "Hi", "hi"],
               pass_context = True)
    async def hello(ctx):
        # Grabs both the name of the caller and the name of the server
        # to print out who sent the request.
        caller = str(ctx.message.author) + " from " + str(ctx.message.guild)
        print("Hello requested: " + str(caller))
        await ctx.send("Hello, this is a testing command.")

    # This command calls upon the ObjBones_D program to generate an objective.  The User ID of the
    # person calling on this command is used to create a file name in the cache system, making it
    # identifiable for other uses.
    # The result of the file are put into a string variable and printed out, as well as pinging the
    # person who called the command.  The formating rules for Discord messages apply here, as well.
    # In this instance the tidle(`) signs are used to offset the objective in 'code format'.
    @c.command(name = "Objective Generator",
               description = "Uses a derivitive of the Objective Bones program to create a bare bones outline for an objective/mission/quest",
               brief = "Create a barebones objective",
               aliases = ["obj", "Obj", "OBJ", "Objective", "objective"])
    async def objective(ctx):
        caller = ctx.message.author.id
        name = str(ctx.message.author.mention)      #Similar to '.author.id'; however, this adds an '@'...
        print("Objective requested: " + str(caller))    #...to the beginning, allowing the author to be pinged
        fileName = str(caller) + "_tmpObj.txt"
        async with ctx.typing():                    #Turns on typing indicator while the following processes
            obj = mainObj(fileName)                 #Calls on and runs the ObjectiveBones_D program...
                                                    #...and returns a string with the entire objective result
        await ctx.send(name + "\n" + "`" + obj + "`")
    
    # This command produces the temp file related to the caller.
    # The User ID is grabbed, along with the first word after the command sign.  The first word
    # is used to determine the type of file being requested.  The command also checks if the
    # request file even exists, first of all.
    # Currently, the file types available are:
    #   - Objective
    @c.command(name = "Save",
                    description = "Order a .txt file for the results recived. (Add 'obj' or 'dice' to your message)",
                    brief = "Save results as .txt",
                    aliases = ["file", "File", "FILE", "s", "S", "save", "SAVE"])
    async def save(ctx, fInp):                  #Grab metadata and first word after callsign
        caller = ctx.message.author.id          #Grab User ID
        name = ctx.message.author.mention       #Grab Mention to ping caller
        print("File requested: " + str(caller))

        # Checks request against possible words to indicate type of file desired
        #   - Obj : Objective Bones file
        #   - Dce : Diceroll
        if fInp in ["OBJ", "Obj", "obj", "O", "o", "OBOJECTIVE", "Objective", "objective"]:
            fType = "Obj"
            print("Type: Objective")
        elif fInp in ["DICE", "Dice", "dice", "D", "d", "ROLL", "Roll", "roll", "R", "r"]:
            fType = "Dce"
            print("Type: Diceroll")
        else:
            fType = ""
            print("Type: NULL")

        #String the User ID and the file type into a file path
        filePath = "caching\\" + str(caller) + "_tmp" + fType + ".txt"

        if os.path.exists(filePath):                        #Checks if the file patch exists
            await ctx.send(name, file=discord.File(filePath))
            print("File found. Sent.")
        elif not os.path.exists(filePath) and fType != "":  #If the path does not exist and a valid file type was selected, the bot will report no file available
            await ctx.send("Sorry, " + name + ", I can't find that file.")
            print("No file found.")
        return

    # This command draws from Dice_D to perform a diceroll for the caller.
    # The User ID is grabbed to create the name of the temp file.
    @c.command(name = "Diceroll",
            description = "Reads sets of dice and rolls them; append flat value to the end only.",
            brief = "Rolls dice as requested",
            aliases = ["dice", "Dice", "roll", "Roll", "r", "R"])
    async def dice(context, *, msg):
        caller = context.message.author.id
        name = context.message.author.mention
        print("Diceroll Requested: " + str(caller))
        fileName = "caching\\" + str(caller) + "_tmpDce.txt"
        result = mainRoller(fileName, msg)
        await context.channel.send(name + "\n" + result)

"""
asyc def <module name>(<context variable>)
<context variable> = C ...
    > C.message : produces all the diffent bits of meta data available from a message
    > C.message.author : produces the name of the caller
        > C.message.author.id : produces the User ID number
    > C.message.channel : produces the channel the call was made from
    > C.message.guild : produces the server the call was sent from

Reading a message:
    async def <module name>(<context variable>, <variable 2>)
        <variable 2> will contain the first word after the command callsign
    async def <module name>(<context variable>, *<variable 2>)
        <variable 2> will be a list of ALL WORDS stated after the command callsign
    sync def <module name>(<context variable>, *, <variable 2>)
        <variable 2> will contain the full message as a string
"""

# ----- ----- -----
# Main program
# ----- ----- -----
def main():
    cacheReload()
    toke = checkToken()
    client = commands.Bot(command_prefix = ".b ")
    botCommands(client)
    client.run(toke)
    return

# ===== ===== =====
# END OF MODULES
# ===== ===== =====
main()
                
