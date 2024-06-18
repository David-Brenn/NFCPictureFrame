from flask import Flask
from nfcPictureFrame import NFCPictureFrame
from multiprocessing import Process, Manager





def run_flask_app(shared_state):
    app = Flask(__name__)
    print("Starting Flask App")

    @app.route('/')
    def applicationStatus():
        string = ""
        if(shared_state['interruptImageSlider']):
            string = string + "The image slider is currently not running."
        else:
            string = string + "The image slider is currently running."
        return string
    app.run(host='0.0.0.0')
    

def run_image_slider(shared_state):
    shared_state['interruptImageSlider'] = True
    nfcPictureFrame = NFCPictureFrame(5,"")
    

if __name__ == '__main__':
    with Manager() as manager:
        shared_state = manager.dict()

        image_slider_process = Process(target=run_image_slider, args=(shared_state,))

        flask_process = Process(target=run_flask_app, args=(shared_state,))

        image_slider_process.start()
        flask_process.start()

        image_slider_process.join()
        flask_process.join()
        


"""
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

"""
