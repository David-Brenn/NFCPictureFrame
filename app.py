from flask import Flask
from nfcPictureFrame import NFCPictureFrame
from multiprocessing import Process, Pipe





def run_flask_app(pipe_conn):
    app = Flask(__name__)
    print(pipe_conn.recv())

    @app.route('/')
    def applicationStatus():
        string = ""
        string = string + "The image slider is currently not running."
        return string
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



    

def run_image_slider(pipe_conn):
    pipe_conn.send("Starting Image Slider")
    nfcPictureFrame = NFCPictureFrame(5,"")
    

if __name__ == '__main__':
        
        parent_conn, child_conn = Pipe()
        image_slider_process = Process(target=run_image_slider, args=(child_conn,))

        flask_process = Process(target=run_flask_app, args=(parent_conn,))

        image_slider_process.start()
        flask_process.start()

        image_slider_process.join()
        flask_process.join()
        