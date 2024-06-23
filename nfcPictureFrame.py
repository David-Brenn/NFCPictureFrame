import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
import os
from random import randrange
import time
#from tkVideoPlayer import TkinterVideo
from vlcVideoPlayer import VlcVideoPlayer
import sys
from configparser import ConfigParser
import configWrapper as config
from tkinter import messagebox
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import threading
from commands import Command

_isMacOS   = sys.platform.startswith('darwin')
_isLinux   = sys.platform.startswith('linux')
_isWindows = sys.platform.startswith('win')

class NFCPictureFrame:
    """ 
    A class to handle the picture frame logic. It contains picking the right image and showing in on a tkinter window
    """

    #Tkinter root window
    root = None

    #TKinter active after id
    pickImageAfterIds = []
    playVideoAfterIds = []

    #TKinter image labe. Set this var to show a image
    sliderFrame = None
    image_label = None



    #Screen size
    screen_height = 0
    screen_width = 0

    #Queue of images to be shown
    imageQueue = []
    #Queue of images that have allready be shown
    allReadyShownImages = []
    
    #place holder of the nfcID
    nfcID = ""
    
    #nfcIDDictinary = {"584184257487":"images","584184388557":"images2"}
    nfcReaderThread = None

    vlcMediaPlayer = None
    vlcCanvas = None

    pipeConn = None
    #Tkinter video player
    #TkVideoPlayer = None
    

    #Bool to interrupt the image slider
    interruptImageSlider = True

    #Bool to interrupt the NFC reader
    interruptNFCReader = True


    configParser = ConfigParser()

    def __init__(self,imageTimer,rootFolderPath,pipeConn):
        """
        A method to init the NFCPictureFrame class. It calls all the setup methods and starts the image slider and the NFC reader.
        """

        self.vlcMediaPlayer = VlcVideoPlayer()

        #Setup tkinter 
        self.setupTKWindow()

        self.setupTKFrame()
        #self.setupTKVideoPlayer()
        self.setupVLCMediaPlayer() 

        self.pipe_conn = pipeConn
        self.startPipeHandler()
        #Start the NFC loop
        self.startNFCLoop()
        #self.testVLCPlayer()
        #Start the image slider
        self.startImageSlider()
        self.root.mainloop()
        
    def startPipeHandler(self):
        """
        A method to start the pipe handler. This method is called from the main method and is used to handle the pipe connection.
        """
        self.pipeHandlerThread = threading.Thread(target=self.pipeHandler,args=(),daemon=True)
        self.pipeHandlerThread.start()

    def pipeHandler(self):
        """
        A method to handle the pipe connection.
        """
        while True:
            if(self.pipe_conn.poll()):
                message = self.pipe_conn.recv()
                print("Message from pipe: " + message.value)
                if(message == Command.STATUS):
                    statusMessage = ""
                    if(self.interruptImageSlider):
                        statusMessage += "NFC Frame: Stopped"
                    else:
                        statusMessage += "\nNFC Frame: Running"
                    self.pipe_conn.send(statusMessage)
                if(message == Command.START):
                    statusMessage = ""
                    if(self.interruptImageSlider):
                        self.startImageSlider()
                        statusMessage += "NFC Frame: Started"
                    else:
                        statusMessage += "NFC Frame: Already Started"
                    self.pipe_conn.send(statusMessage)
                if(message == Command.STOP):
                    statusMessage = ""
                    if not (self.interruptImageSlider):
                        self.stopImageSlider()
                        statusMessage += "NFC Frame: Stopped"
                    else:
                        statusMessage += "NFC Frame: Already Stopped"
                    self.pipe_conn.send(statusMessage)

            time.sleep(1)

    
        
    def setupTKWindow(self):  
        """
        A method to setup the tkinter window
        """
        self.root = tk.Tk()
        self.root.title("NFC Picture Frame")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.configure(highlightthickness=0,highlightcolor="black",borderwidth=0,background="black")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

    def setupTKFrame(self):
        """
        A method to setup the tkinter frame
        """
        self.sliderFrame = tk.Frame(self.root,height=self.screen_height,width=self.screen_width,background="black")
        self.sliderFrame.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.sliderFrame.pack(expand=True)

    def setupTKLable(self):
        """
        A method to setup the tkinter image lable
        """
        self.image_label = tk.Label(self.sliderFrame,height=self.screen_height,width=self.screen_width,background="black")
        self.image_label.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        #self.image_label.pack(expand=True)


   # def setupTKVideoPlayer(self):
        """
        A method to setup the tkinter video player
        """
        #self.TkVideoPlayer = TkinterVideo(master=self.root, scaled=False)
        #self.TkVideoPlayer.configure(background="black")
  
    
    def setupVLCMediaPlayer(self):
        self.vlcCanvas = tk.Canvas(self.sliderFrame,height=self.screen_height,width=self.screen_width,background="black")
        self.vlcMediaPlayer.setCanvas(self.vlcCanvas)

    def packVLCPlayer(self):
        self.vlcCanvas.pack(expand=True,fill="both")

    def unpackVLCPlayer(self):
        self.vlcCanvas.pack_forget()

    def checkRootFolder(self):
        """
        A method to check if the root folder is actually a folder
        """
        #TODO: Add folder picker if no root folder is set
        #Check if the active image folder is set
        if (config.rootFolderPath == ""):
            print("No root folder")
            self.pickRootFolder()
        else:
            if (os.path.isdir(config.rootFolderPath)):
                print("Root folder found")
                return True
            else:
                print("Root folder not found")
                self.pickRootFolder()

    def setInterruptImageSlider(self,boolean):
        """
        A method to set the interruptImageSlider variable
        """
        self.interruptImageSlider = boolean

    def setInterruptNFCReader(self,boolean):
        """
        A method to set the interruptNFCReader variable
        """
        self.interruptNFCReader = boolean

    def startImageSlider(self):
        """
        A method to start the image slider
        """
        self.setInterruptImageSlider(False)
        self.sliderFrame.configure(highlightbackground = "black",highlightthickness=0,borderwidth=0)
        self.setupTKLable()

        self.checkRootFolder()
        self.checkActiveImageFolder()
        self.scanFolderForImages()
        self.image_label.pack(expand=True)
        #TODO: Mabye remove the append step and simply call the method
        self.pickImageAfterIds.append(self.pickImage())

    def stopImageSlider(self):
        """
        A method to stop the image slider
        """
        self.setInterruptImageSlider(True)
        self.imageQueue = []
        self.allReadyShownImages = []
        self.image_label.pack_forget()
        self.vlcMediaPlayer.stopVideo()
        self.vlcCanvas.pack_forget()
        self.image_label.destroy()
        self.sliderFrame.configure(highlightbackground = "red", highlightthickness=2,borderwidth=2)

    def changeActiveImageFolder(self,activeImageFolderPath):
        """
        A method to change the active image folder
        """
        print("Changing active image folder")
        self.stopImageSlider()
        config.setActiveImageFolderPath(activeImageFolderPath)
        self.startImageSlider()
        self.root.after(3000,self.startNFCLoop)

    def checkActiveImageFolder(self):
        if (config.activeImageFolderPath == ""):
            #If not set the first folder as active image folder
            print("No active image folder. The first folder will be used")
            self.pickFirstActiveFolder()
        else :
            if (os.path.isdir(config.activeImageFolderPath)):
                print("Active image folder found")
                return True
            else:
                print("Active image folder not found")
                self.pickFirstActiveFolder()

    def pickFirstActiveFolder(self):    
        folders = os.listdir(config.rootFolderPath)
        for folder in folders:
            if(folder.startswith(".")):
                folders.remove(folder)
        if (folders.__len__() == 0):
            print("No folders found in root folder")
            self.closeWithError("No folders found in root folder")
        else :
            config.setActiveImageFolderPath(config.rootFolderPath+"/"+folders[0])


    def pickRootFolder(self):
        #TODO: Add a method to pick the root folder
        filename = filedialog.askdirectory()
        if filename == "":
            print("No folder selected")
            self.closeWithError("No folder selected")
        config.setRootFolderPath(filename)
    
    

    #Scan folder for images and add them to the queue   
    def scanFolderForImages(self):
        """
        Scan the activeImageFolder for images add fill the queue
        """
        file_types = [".JPG","JPEG","PNG",".GIF",".MP4",".jpg",".jpeg",".png",".gif",".mp4",".MOV",".mov"]
        #TODO: Add if folder exist check. If not print error
        for file in os.listdir(config.activeImageFolderPath):
            if file.endswith(tuple(file_types)):
                print(file)
                self.imageQueue.append(file)
        if(self.imageQueue.__len__() == 0):
            print("No images found in folder:" + config.activeImageFolderPath)
            self.closeWithError("No images found in folder" + config.activeImageFolderPath)
            return

    def pickImage(self):
        """
        Picks a random image from the ImageQueue and set it to the image label
        If the image is a video it will be played
        """
        if(self.interruptImageSlider):
            return
        else:
            if(self.imageQueue.__len__()!= 0):
                #Pick random image from queue
                pickedSlot = randrange(0,self.imageQueue.__len__())
                pickedImage = self.imageQueue.pop(pickedSlot)
                print("Picked image: " + pickedImage)
                #Add image to allready shown images
                self.allReadyShownImages.append(pickedImage)
                if(pickedImage.endswith((".mp4",".MP4",".mov",".MOV"))):
                    #To show a video we need to stop the image slider and show the video
                    self.setInterruptImageSlider(True)
                    self.image_label.pack_forget() 
                    #self.root.after_cancel(self.playVideoAfterIds.pop)                  
                    self.playVideoAfterIds = self.playVideo(config.activeImageFolderPath+"/"+pickedImage)
                    return
                else:
                    self.showImage(config.activeImageFolderPath+"/"+pickedImage)

                #Call this method again after imageTimer
                #self.root.after_cancel(self.pickImageAfterIds.pop())
                self.pickImageAfterIds.append(self.image_label.after(config.imageTimer*1000,self.pickImage))
            else: 
                print("No more images to show. Restarting queue")
                self.imageQueue = self.allReadyShownImages
                self.allReadyShownImages = []
                #self.root.after_cancel(self.pickImageAfterIds.pop())
                self.pickImageAfterIds.append(self.image_label.after(1,self.pickImage))

    def exit_fullscreen(self,event):
        self.root.attributes("-fullscreen", False)

    def videoDurationFound(self,event):
        """
        A method that calls itself every second to check if the video duration is found. If the duration is found it will call the videoEnded method with the duration as parameter.
        """
        print("Video duration found")
        videoDuration = int(self.TkVideoPlayer.video_info()["duration"])
        print(videoDuration)
        self.image_label.after(videoDuration+1,self.videoEnded)
        
    
    #def tkVideoEnded(self):
        """
        A method to stop the video and show the image label again.
        """
        #self.TkVideoPlayer.stop()
        #self.TkVideoPlayer.pack_forget()
        #self.image_label.pack(expand=True)
        #self.setInterruptImageSlider(False)
        #self.root.after(1,self.pickImage)
        #return


    def showImage(self,image_path):
        """
        A method to show a image on the image label.
        """
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image)
        image.thumbnail((self.screen_width, self.screen_height))
        image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=image,highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.image = image


    def playVideo(self,video_path):
        """
        A method to play a video on the video player. On mac it uses the tkinter video player and on other systems it uses the vlc video player.
        """
        self.packVLCPlayer()
        self.vlcMediaPlayer.playVideo(video_path)
        self.image_label.after(1000,self.vlcGetDuration)

    def vlcGetDuration(self):  
        """
        A method that calls itself every second until the duration is found. If the duration is found it will call the vlcVideoEnded method with the duration as parameter.
        """
        videoDuration = int(self.vlcMediaPlayer.mediaPlayer.get_length())
        print("VLC VideoDuration: " + str(videoDuration))
        if(videoDuration == 0 or videoDuration == -1):
            self.image_label.after(1000,self.vlcGetDuration)
        else:
            self.image_label.after(videoDuration,self.vlcVideoEnded)


    def vlcVideoEnded(self):
        """
        A method to stop the video and show the image label again.
        """
        self.vlcMediaPlayer.stopVideo()
        self.unpackVLCPlayer()
        self.image_label.pack(expand=True)
        self.setInterruptImageSlider(False)
        self.image_label.after(1,self.pickImage)
        

    def NFCLoop(self):
        """
        A method to loop the NFC reader and check for new nfc tags. This method is called every second and only stops if a new nfc tag is read and then loads images from the new folder.
        """
        while not (self.interruptNFCReader):
            nfcId,nfcText = self.readNFCID()
            if(nfcId != "" ):
                newFolder = self.translateIDToFolderName(str(nfcId))
                activeImageFolderPath = config.rootFolderPath+"/"+newFolder
                if(activeImageFolderPath == config.activeImageFolderPath):
                    print("Same folder")
                    print("Starting NFC loop again")
                    time.sleep(5)
                elif(os.path.isdir(activeImageFolderPath)):
                    self.changeActiveImageFolder(activeImageFolderPath)
                    self.stopNFCLoop()
                else:
                    print("No folder found for ID: " + str(nfcId))
                    print("Folder path: " + activeImageFolderPath)
                    print("Starting NFC loop again")
                    time.sleep(5)

            else:
                print("No ID found")
                print("Starting NFC loop again")
                time.sleep(5)
                

    def translateIDToFolderName(self,nfcID):
        """
        A method to translate the nfcID to a folder name
        """
        if(nfcID in config.nfcIDDictinary):
            return config.nfcIDDictinary[nfcID]
        else:
            print("No folder name found for ID: " + nfcID)
            return nfcID


    def readNFCID(self):
        """
        A method to read the NFC ID and text
        """
        try:
            reader = SimpleMFRC522()
            nfcId, nfcText = reader.read()
            print(nfcId, nfcText)
        finally:
            GPIO.cleanup()

        return nfcId, nfcText
    
    def startNFCLoop(self):
        """
        A method to start the NFC loop
        """
        self.interruptNFCReader = False
        self.nfcReaderThread = threading.Thread(target=self.NFCLoop,args=(),daemon=True)
        self.nfcReaderThread.start()

    def stopNFCLoop(self):
        """
        A method to stop the NFC loop 
        """
        self.interruptNFCReader = True

    def testVLCPlayer(self):
        """
        A method to test the vlc video player
        """
        self.packVLCPlayer()
        self.vlcMediaPlayer.playVideo(config.rootFolderPath+"/images/video.mp4")
        

    def closeWithError(self,errorMessage):
        """ 
        A method to close the program and show a message
        """
        messagebox.showerror("NFC Picture Frame",errorMessage)
        self.root.destroy()


    def testChangeActiveImageFolder(self,ms,activeImageFolderPath):
        """
        A method to test the changeActiveImageFolder method
        """
        print("Test change active image folder")
        self.image_label.after(ms,self.changeActiveImageFolder,activeImageFolderPath)
