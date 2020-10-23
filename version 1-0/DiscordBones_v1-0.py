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

Version: 1-1
Date: 10/23/2020
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

# Check for valid token on file.
def checkToken():
    x = 0
    while x == 0:
        print("Loading token...")
        if os.path.exists("key.txt"):
            print("\'key.txt\' located \nExtracting...")
            with open("key.txt", "r") as file:
                t = file.read()
            l = len(t)
            print("Checking key length")
            if l == 59:
                print("Key of correct length found \nApplying...")
                x = 1
            else:
                print("Key length not correct.\nPlease fix key.txt")
                y = fixToken()
                if y != "Y":
                    x = 1
                    t = 0
        else:
            print("No token file found.")
            y = fixToken()
            if y != "Y":
                x = 1
                t = 0
    return t

# In-Program fix for bot token.
def fixToken():
    x = 0
    print("Do you with to paste a new key? (y/n)")
    while x == 0:
        ans = str(input())
        ans = ans.upper()
        if ans == "Y":
            key = str(input("Paste key now: "))
            with open("key.txt", "w") as file:
                file.write(key)
            x = 1
        elif ans == "N":
            x = 1
    return ans

# Flush and create caching folder.
def cacheReload():
    if os.path.exists("caching"):
        shutil.rmtree("caching")
        print("Purging Cache: \\caching\\")
    else:
        print("No leftover cache found")
    print("Creating cache folder...")
    os.mkdir("caching")


# ----- ----- ----- ----- ----- -----
# Listing all possible commands and abilities give to the bot.
# ----- ----- ----- ----- ----- -----
def botCommands(c):
    @c.event
    async def on_ready():
        print("Discord Bones is ready.")
        return
    
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

    # Calls upon the ObjBones_D program to generate an objective.
    @c.command(name = "Objective Generator",
               description = "Uses a derivitive of the Objective Bones program to create a bare bones outline for an objective/mission/quest",
               brief = "Create a barebones objective",
               aliases = ["obj", "Obj", "OBJ", "Objective", "objective"])
    async def objective(ctx):
        caller = ctx.message.author.id
        name = str(ctx.message.author.mention)
        print("Objective requested: " + str(caller))
        fileName = str(caller) + "_tmpObj.txt"
        async with ctx.typing():
            obj = mainObj(fileName)
        await ctx.send(name + "\n" + "`" + obj + "`")

    # Currently, the file types available are:
    #   - Objective
    @c.command(name = "Save",
                    description = "Order a .txt file for the results recived. (Add 'obj' or 'dice' to your message)",
                    brief = "Save results as .txt",
                    aliases = ["file", "File", "FILE", "s", "S", "save", "SAVE"])
    async def save(ctx, fInp):
        caller = ctx.message.author.id
        name = ctx.message.author.mention
        print("File requested: " + str(caller))

        #   - Obj : Objective Bones file
        if fInp in ["OBJ", "Obj", "obj", "O", "o", "OBOJECTIVE", "Objective", "objective"]:
            fType = "Obj"
            print("Type: Objective")
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
        result = mainRoller(msg)
        print(result)
        await context.channel.send(name + "\n" + str(result))

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
    client = commands.Bot(command_prefix = "/b ")
    botCommands(client)
    client.run(toke)
    return

# ===== ===== =====
# END OF MODULES
# ===== ===== =====
main()
                
