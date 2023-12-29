# NFCPictureFrame

To do
- Buy old Tv
- Explain code more
- Add video functionality

This project aims to make a nfc digital picture frame. The idear is that souviniers from vacations should funciton as a NFC Tag for the digital picture frame. This is done by adding a tiny nfc sticker to the souvenier and reading the data with the help of a ncf reader connectet to a raspberry. The raspberry then shows a diashow with the according pictures and videos. All of this is fit inside of a old TV so its compacted at doesnt look to modern like many digital picture frames do. 

The Pictures are shown with the help of the python library TKinter while the videos are presented with vlc or omxplayer. The information form the NFC reader is used to get the right image folder. The images of the folder are randomly queued.

If the basic functions works the project can be extendet by a image cloud storage on the Raspberry and a App to controll the Frame. The app should have the function to add a NFC tag to a certain image folder maybe with a image of the souvenier. This information should be stored in a dictornary on the raspberry to compate the tag information with the could folder name.
