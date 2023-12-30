import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os
from random import randrange

class NFCPictureFrame:
    #Time a image is shown in seconds
    imageTimer = 0
    #Path to the folder where the images are stored
    rootFolderPath = ""

    activeImageFolderPath = ""

    #Tkinter root window
    root = None
    image_label = None

    #Screen size
    screen_height = 0
    screen_width = 0

    #Queue of images to be shown
    imageQueue = []
    allReadyShownImages = []
    #nfcID
    nfcID = "images"
    def __init__(self,imageTimer,rootFolderPath):
        self.root = tk.Tk()
        self.root.title("NFC Picture Frame")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.configure(background="black")
        self.root.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        
        self.image_label = tk.Label(self.root)
        self.image_label.configure(highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.pack(expand=True)

        self.imageTimer = imageTimer

        if(rootFolderPath == ""):
            rootFolderPath = os.path.dirname(os.path.realpath(__file__))
        self.rootFolderPath = rootFolderPath

        self.scanForNFCFolder()
        self.scanFolderForImages()
        self.pickImage()
        

        self.root.mainloop()
    
    #Scan for a folder with the nfcID as name
    def scanForNFCFolder(self):
        if (os.path.isdir(self.rootFolderPath+"/" +self.nfcID)):
            self.activeImageFolderPath = self.rootFolderPath+"/" +self.nfcID
            
        print(self.activeImageFolderPath)


    #Scan folder for images and add them to the queue   
    def scanFolderForImages(self):
        file_types = [".jpg",".jpeg",".png"]
        for file in os.listdir(self.activeImageFolderPath):
            if file.endswith(tuple(file_types)):
                print(file)
                self.imageQueue.append(file)
        if(self.imageQueue.__len__ == 0):
            print("No images found in folder")
            return

    def pickImage(self):
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
        self.image_label.configure(image=image,highlightthickness=0,highlightcolor="black",borderwidth=0)
        self.image_label.image = image



x = NFCPictureFrame(5,"")

