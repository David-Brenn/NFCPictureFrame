from flask import Flask
from nfcPictureFrame import NFCPictureFrame

app = Flask(__name__)
nfcPictureFrame = NFCPictureFrame(5,"")
app.run(host='0.0.0.0')

@app.route('/')
def applicationStatus():
    string = ""
    if(nfcPictureFrame.interruptImageSlider):
        string = string + "The image slider is currently not running."
    else:
        string = string + "The image slider is currently running."
    if(nfcPictureFrame.interruptNFCReader):
        string = string + "The NFC reader is currently not running."
    else:
        string = string + "The NFC reader is currently running."
    return string


@app.route('/startNFCFrame')
def startNFCFrame():
    if (nfcPictureFrame.interruptImageSlider):
        nfcPictureFrame.startImageSlider()
        return 'NFC Frame Started'
    else:
        return 'NFC Frame Already Started'
    

@app.route('/stopNFCFrame')
def stopNFCFrame():
    if (nfcPictureFrame.interruptImageSlider):
        return 'NFC Frame Already Stopped'
    else:
        nfcPictureFrame.stopImageSlider()
        return 'NFC Frame Stopped'

@app.route('/addNFCTag/<nfcID>/<folderName>')
def addNFCTag(nfcID, folderName):
    if(nfcID == ""):
        return "NFC ID cannot be empty"
    else:
        if(folderName == ""):
            return "Folder name cannot be empty"
        else:
            return nfcPictureFrame.addNfcID(nfcID, folderName) 

@app.route('/removeNFCTag/<nfcID>')
def removeNFCTag(nfcID):
    if(nfcID == ""):
        return "NFC ID cannot be empty"
    else:
        return nfcPictureFrame.removeNfcID(nfcID)

@app.route("/renameNFCTag/<nfcID>/<newFolderName>")
def renameNFCTag(nfcID, newFolderName):
    if(nfcID == ""):
        return "NFC ID cannot be empty"
    else:
        if(newFolderName == ""):
            return "Folder name cannot be empty"
        else:
            return nfcPictureFrame.renameNfcID(nfcID, newFolderName)

@app.route("/getNFCTags")
def getNFCTags():
    nfcJson = nfcPictureFrame.getNFCTags().to_json()
    return nfcJson

