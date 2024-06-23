from configparser import ConfigParser
import os


#Add global variables here
imageTimer = 5
rootFolderPath = ""
activeImageFolderPath = ""
nfcIDDictinary = {}

configFilePath = "config.ini"
configParser = ConfigParser()

def readConfigFile():
    """
    A method to read the config file. If no file is found it will create a new one.
    """
    if (not os.path.isfile(configFilePath)):
        print("No config file found")
        initConfigFile()

    configParser.read(configFilePath)
    global imageTimer
    imageTimer = configParser.getint("Settings","imageTimer")

    global rootFolderPath
    rootFolderPath = configParser.get("Settings","rootFolderPath")

    global activeImageFolderPath
    activeImageFolderPath = configParser.get("Settings","activeImageFolderPath")

    global nfcIDDictinary
    nfcIDDictinary = {}
    if (configParser.has_section("nfcIDDictionary")):
        nfcIDDictinary = {key: value for key, value in configParser.items("nfcIDDictionary")}
    return "Config file read"    


def initConfigFile():
    """
    A method to init the config file
    """
    if not (configParser.has_section("Settings")):
        configParser.add_section("Settings")
    configParser.set("Settings","imageTimer",str(imageTimer))
    configParser.set("Settings","rootFolderPath",rootFolderPath)
    configParser.set("Settings","activeImageFolderPath",activeImageFolderPath)
    with open('config.ini', 'w') as configfile:
        configParser.write(configfile)
    return "Config file created"

def setRootFolderPath(path):
    """
    A method to set the root folder path
    """
    global rootFolderPath
    rootFolderPath = path
    if not (configParser.has_section("Settings")):
        configParser.add_section("Settings")
    configParser.set("Settings","rootFolderPath",path)
    with open('config.ini', 'w') as configfile:
        configParser.write(configfile)
    return "Root Folder Path set"


def setActiveImageFolderPath(path):
    """
    A method to set the active image folder path
    """
    global activeImageFolderPath
    activeImageFolderPath = path
    if not (configParser.has_section("Settings")):
        configParser.add_section("Settings")
    configParser.set("Settings","activeImageFolderPath",path)
    with open('config.ini', 'w') as configfile:
        configParser.write(configfile)
    return "Active Image Folder Path set"


def setImageTimer(timer):
    """
    A method to set the image timer
    """
    global imageTimer
    imageTimer = timer
    if not (configParser.has_section("Settings")):
        configParser.add_section("Settings")
    configParser.set("Settings","imageTimer",str(timer))
    with open('config.ini', 'w') as configfile:
        configParser.write(configfile)
    return "Image Timer set"


def writeNfcIDDictionary():
    """
    A method to write the nfc id dictionary
    """
    if not (configParser.has_section("nfcIDDictionary")):
        configParser.add_section("nfcIDDictionary")
    for key in nfcIDDictinary:
        configParser.set("nfcIDDictionary",key,nfcIDDictinary[key])
    with open('config.ini', 'w') as configfile:
        configParser.write(configfile)
    return "NFC ID Dictionary written"


def addNfcID(id,folderName):
    """
    A method to add a nfc id to the nfc id dictionary
    """
    if (nfcIDDictinary.__contains__(id)):
        return "NFC ID already exists"
    nfcIDDictinary[id] = folderName
    writeNfcIDDictionary()
    return "NFC Tag Added"


def removeNfcID(id):
    """
    A method to remove a nfc id from the nfc id dictionary
    """
    if(id in nfcIDDictinary):
        nfcIDDictinary.pop(id)
        writeNfcIDDictionary()
    else:
        return "NFC ID not found"
    return "NFC Tag Removed"


def renameNfcID(id,newFolderName):
    """
    A method to rename a nfc id from the nfc id dictionary
    """
    if(id in nfcIDDictinary):
        nfcIDDictinary[id] = newFolderName
        writeNfcIDDictionary()
    else:
        print("ID not found")
        return "NFC ID not found"
    return "NFC Tag Renamed"


# Initialize the config file
readConfigFile()