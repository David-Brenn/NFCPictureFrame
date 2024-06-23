# NFCPictureFrame
This project aims to make a nfc digital picture frame. The idear is that souviniers from vacations should funciton as a NFC Tag for the digital picture frame. This is done by adding a tiny nfc sticker to the souvenier and reading the data with the help of a ncf reader connectet to a raspberry. The raspberry then shows a diashow with the according pictures and videos. All of this is fit inside of a old TV so its compacted at doesnt look to modern like many digital picture frames do. 

The Pictures are shown with the help of the python library TKinter while the videos are presented with vlc or omxplayer. The information form the NFC reader is used to get the right image folder. The images of the folder are randomly queued.

The picture frame can be controlled by unsing a Flask REST API. It has for example the possiblity to stop the slide show or to add a new NFC tag. Currently i'm working on creating a Iphone App that uses the API and provides a better user interface. 

To store files on the raspberry i use samba. This makes it possible create a shared folder that is public to the network. The folder can be editied via every filesystem by adding a server. For better compabillity with iphone add [this](https://forum.rockstor.com/t/configure-samba-to-work-better-with-apple-devices/8956) configuration to the samba config. 
