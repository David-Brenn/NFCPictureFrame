import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os
from random import randrange
import vlc
import time
from tkVideoPlayer import TkinterVideo

class NFCPictureFrame:
    """ 
    A class to handle the picture frame logic. It contains picking the right image and showing in on a tkinter window
    """
    #Time a image is shown in seconds
    imageTimer = 0
    
    #Path to the folder where the images are stored
    rootFolderPath = ""

    activeImageFolderPath = ""

    #Tkinter root window
    root = None

    #TKinter image labe. Set this var to show a image
    image_label = None

    #Screen size
    screen_height = 0
    screen_width = 0

    #Queue of images to be shown
    imageQueue = []
    #Queue of images that have allready be shown
    allReadyShownImages = []
    
    #place holder of the nfcID
    nfcID = "images"

    #VLC instance
    vlcInstance = None

    #Tkinter video player
    TkVideoPlayer = None

    #Bool to interrupt the image slider
    interruptImageSlider = False

    #Bool to interrupt the NFC reader
    interruptNFCReader = False

    def __init__(self,imageTimer,rootFolderPath):
        #Setup tkinter 
        self.setupTKWindow()
        self.setupTKLable()
     
        self.imageTimer = imageTimer

        self.setupTKVideoPlayer()

        self.setRootFolderPath(rootFolderPath)  


        #Fill the queue 
        self.scanForNFCFolder()
        self.scanFolderForImages()

        #Start the NFC loop
        self.startNFCLoop()

        #Start the image slider
        self.pickImage()

        self.root.mainloop()

        
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


    def setupTKLable(self):
        """
        A method to setup the tkinter image lable
        """
        self.image_label = tk.Label(self.root,height=self.screen_height,width=self.screen_width,background="black")
        self.image_label.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.pack(expand=True)

    
    def setupTKVideoPlayer(self):
        """
        A method to setup the tkinter video player
        """
        self.TkVideoPlayer = TkinterVideo(master=self.root, scaled=False)
        self.TkVideoPlayer.configure(background="black")

    def setRootFolderPath(self,rootFolderPath):
        """
        A method to set the root folder path.
        """
        if(rootFolderPath == ""):
            rootFolderPath = os.path.dirname(os.path.realpath(__file__))
        self.rootFolderPath = rootFolderPath
    
    def scanForNFCFolder(self):
        """
        A method to find a folder with nfcID as name
        """
        if (os.path.isdir(self.rootFolderPath+"/" +self.nfcID)):
            self.activeImageFolderPath = self.rootFolderPath+"/" +self.nfcID
            
        print(self.activeImageFolderPath)
        #TODO: Else case if no folder is found. Show error message onscreen

    #Scan folder for images and add them to the queue   
    def scanFolderForImages(self):
        """
        Scan the activeImageFolder for images add fill the queue
        """
        file_types = [".jpg",".jpeg",".png",".gif",".mp4"]
        #TODO: Add if folder exist check. If not print error
        for file in os.listdir(self.activeImageFolderPath):
            if file.endswith(tuple(file_types)):
                print(file)
                self.imageQueue.append(file)
        if(self.imageQueue.__len__ == 0):
            print("No images found in folder")
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
                #Pick random image
                
                pickedSlot = randrange(0,self.imageQueue.__len__())
                pickedImage = self.imageQueue.pop(pickedSlot)
                print("Picked image: " + pickedImage)
                self.allReadyShownImages.append(pickedImage)
                if(pickedImage.endswith(".mp4")):
                    self.interuptImageSlider = True
                    self.image_label.pack_forget()
                    #self.TkVideoPlayer.bind("<<Duration>>",self.videoDurationFound)
                    self.playVideo(self.activeImageFolderPath+"/"+pickedImage)
                    print("Current duration: " + str(self.TkVideoPlayer.current_duration()))
                    self.root.after(20000,self.videoEnded)
                    return
                else:
                    self.showImage(self.activeImageFolderPath+"/"+pickedImage)

                self.root.after(self.imageTimer*1000,self.pickImage)
            else: 
                print("No more images to show. Restarting queue")
                self.imageQueue = self.allReadyShownImages
                self.allReadyShownImages = []
                self.root.after(1,self.pickImage())

    def exit_fullscreen(self,event):
        self.root.attributes("-fullscreen", False)

    def videoDurationFound(self,event):
        print("Video duration found")
        videoDuration = int(self.TkVideoPlayer.video_info()["duration"])
        print(videoDuration)
        self.root.after(videoDuration+1,self.videoEnded)
        
    
    def videoEnded(self):
        self.TkVideoPlayer.stop()
        self.TkVideoPlayer.pack_forget()
        self.image_label.pack(expand=True)
        self.interruptImageSlider = False
        self.root.after(1,self.pickImage)
        return


    def showImage(self,image_path):
        image = Image.open(image_path)
        image.thumbnail((self.screen_width, self.screen_height))
        image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=image,highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.image = image


    def playVideo(self,video_path):
        #Setup the VLC instance
        #self.image_label.image = ""
        self.TkVideoPlayer.load(video_path)
        self.TkVideoPlayer.pack(expand=True, fill="both")
        self.TkVideoPlayer.play() # play the video
        #videoplayer.pack_forget()
        #self.image_label.pack(expand=True)


    def NFCLoop(self):
        """
        A method to loop the NFC reader and check for new nfc tags. This method is called every second and only stops if a new nfc tag is read and then loads images from the new folder.
        """
        if(self.interruptNFCReader):
            return
        else:
        #TODO: Add if ID was read and if it is a new ID)
            print("NFC loop")
        #TODO: Add else case if no new ID was read
        self.root.after(1000,self.NFCLoop)

    def startNFCLoop(self):
        """
        A method to start the NFC loop
        """
        self.interruptNFCReader = False
        self.NFCLoop()

    def stopNFCLoop(self):
        """
        A method to stop the NFC loop 
        """
        self.interruptNFCReader = True

x = NFCPictureFrame(5,"")

