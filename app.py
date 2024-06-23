from flask import Flask, request
from nfcPictureFrame import NFCPictureFrame
from multiprocessing import Process, Pipe
from commands import Command
import configWrapper as config
import json



def run_flask_app(pipeConn):
    app = Flask(__name__)
    print(pipeConn.recv())

    @app.route('/')
    def applicationStatus():
        pipeConn.send(Command.STATUS)
        if pipeConn.poll(3):
            status = pipeConn.recv()
            return status
        else: 
            return "No response from Image Slider"
        return status
    
    @app.route('/start')
    def startImageSlider():
        pipeConn.send(Command.START)
        if pipeConn.poll(3):
            status = pipeConn.recv()
            return status
        else: 
            return "No response from Image Slider"
        return status
    
    @app.route('/stop')
    def stopImageSlider():
        pipeConn.send(Command.STOP)
        if pipeConn.poll(3):
            status = pipeConn.recv()
            return status
        else: 
            return "No response from Image Slider"
        return status
    
    @app.route('/reload-config')
    def reloadConfig():
        pipeConn.send(Command.RELOAD_CONFIG)
        if pipeConn.poll(3):
            status = pipeConn.recv()
            return status
        else: 
            return "No response from Image Slider"
        return status
    
    @app.route('/nfc')
    def listNFCIDs():
        return json.dumps(config.nfcIDDictinary)
    
    #Add POST method to add NFC ID
    @app.route('/nfc/add', methods=['POST'])
    def addNFCID():
        data = request.json  # Get JSON data from the request
        nfcID = data.get('nfcID')
        folderName = data.get('folderName')
        
        if not nfcID:
            return "NFC ID cannot be empty", 400  # Return a 400 Bad Request response
        if not folderName:
            return "Folder name cannot be empty", 400  # Return a 400 Bad Request response
        
        # Assuming config.addNfcID(nfcID, folderName) adds the NFC ID and folder name to your configuration
        # and returns True if successful, False otherwise.
        if config.addNfcID(nfcID, folderName):
            reloadConfig()
            return f"NFC ID {nfcID} with folder name {folderName} added successfully", 200
        else:
            return "Failed to add NFC ID and folder name", 500  # Return a 500 Internal Server Error response
        
    #Add DELETE method to remove NFC ID
    @app.route('/nfc/remove', methods=['DELETE'])
    def removeNFCID():
        data = request.json  # Get JSON data from the request
        nfcID = data.get('nfcID')
        
        if not nfcID:
            return "NFC ID cannot be empty", 400  # Return a 400 Bad Request response
        
        # Assuming config.removeNfcID(nfcID) removes the NFC ID from your configuration
        # and returns True if successful, False otherwise.
        if config.removeNfcID(nfcID):
            reloadConfig()
            return f"NFC ID {nfcID} removed successfully", 200
        else:
            return "Failed to remove NFC ID", 500  # Return a 500 Internal Server Error response
        
    #Add PUT method to rename NFC ID
    @app.route('/nfc/rename', methods=['PUT'])
    def renameNFCID():
        data = request.json  # Get JSON data from the request
        nfcID = data.get('nfcID')
        newFolderName = data.get('newFolderName')
        
        if not nfcID:
            return "NFC ID cannot be empty", 400  # Return a 400 Bad Request response
        if not newFolderName:
            return "New folder name cannot be empty", 400  # Return a 400 Bad Request response
        
        # Assuming config.renameNfcID(nfcID, newFolderName) renames the folder name associated with the NFC ID
        # and returns True if successful, False otherwise.
        if config.renameNfcID(nfcID, newFolderName):
            reloadConfig()
            return f"Folder name for NFC ID {nfcID} renamed to {newFolderName} successfully", 200
        else:
            return "Failed to rename folder name for NFC ID", 500  # Return a 500 Internal Server Error response

    #Add POST/GET  method to set/get image timer
    @app.route('/image-timer', methods=['POST', 'GET'])
    def imageTimer():
        if request.method == 'GET':
            return str(config.imageTimer)
        if request.method == 'POST':
            data = request.json  # Get JSON data from the request
            timer = data.get('timer')
            
            if not timer:
                return "Timer cannot be empty", 400  # Return a 400 Bad Request response
            
            # Assuming config.setImageTimer(timer) sets the image timer in your configuration
            # and returns True if successful, False otherwise.
            if config.setImageTimer(timer):
                reloadConfig()
                return f"Image timer set to {timer} successfully", 200
            else:
                return "Failed to set image timer", 500  # Return a 500 Internal Server Error response

    @app.route('/root-image-folder', methods=['POST', 'GET'])
    def rootImageFolder():
        if request.method == 'GET':
            return config.rootFolderPath
        if request.method == 'POST':
            data = request.json  # Get JSON data from the request
            rootImageFolder = data.get('rootImageFolder')
            
            if not rootImageFolder:
                return "Root image folder cannot be empty", 400  # Return a 400 Bad Request response
            
            # Assuming config.setRootImageFolder(rootImageFolder) sets the root image folder in your configuration
            # and returns True if successful, False otherwise.
            if config.setRootFolderPath(rootImageFolder):
                reloadConfig()
                return f"Root image folder set to {rootImageFolder} successfully", 200
            else:
                return "Failed to set root image folder", 500  # Return a 500 Internal Server Error response



    app.run(host='0.0.0.0')


    """
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



    

def run_image_slider(pipeConn):
    pipeConn.send("Starting Image Slider")
    nfcPictureFrame = NFCPictureFrame(5,"",pipeConn)
    

if __name__ == '__main__':
        
        parentConn, childConn = Pipe()
        image_slider_process = Process(target=run_image_slider, args=(childConn,))

        flask_process = Process(target=run_flask_app, args=(parentConn,))

        image_slider_process.start()
        flask_process.start()

        image_slider_process.join()
        flask_process.join()
        