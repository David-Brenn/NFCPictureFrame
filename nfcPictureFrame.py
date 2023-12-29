import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os
from random import randrange

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
    def __init__(self,imageTimer,rootFolderPath):
        #Setup the TK window
        self.root = tk.Tk()
        self.root.title("NFC Picture Frame")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.configure(background="black")
        self.root.configure(highlightthickness=0,highlightcolor="black")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        #Setup the image lable
        self.image_label = tk.Label(self.root)
        self.image_label.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.pack(expand=True)
        
        self.imageTimer = imageTimer

        if(rootFolderPath == ""):
            rootFolderPath = os.path.dirname(os.path.realpath(__file__))
        self.rootFolderPath = rootFolderPath

        #Fill the queue 
        self.scanForNFCFolder()
        self.scanFolderForImages()
        self.pickImage()
        

        self.root.mainloop()

    
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
        file_types = [".jpg",".jpeg",".png"]
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
        Picks a random image from the ImageQueue and 
        """
        if(self.imageQueue.__len__()!= 0):
            #Pick random image
            
            pickedSlot = randrange(0,self.imageQueue.__len__()) 
            pickedImage = self.imageQueue.pop(pickedSlot)

            self.showImage(self.activeImageFolderPath+"/"+pickedImage)
            self.allReadyShownImages.append(pickedImage)
            self.root.after(self.imageTimer*1000,self.pickImage)

    def exit_fullscreen(self,event):
        self.root.attributes("-fullscreen", False)


    def showImage(self,image_path):
        image = Image.open(image_path)
        image.thumbnail((self.screen_width, self.screen_height))
        image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=image)
        self.image_label.image = image



x = NFCPictureFrame(5,"")

