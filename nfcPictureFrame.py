import cv2
import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title("NFC Picture Frame")

root.attributes("-fullscreen", True)

def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

root.configure(background="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")



def update_image():
    image_path = "testbild.jpg"
    image = Image.open(image_path)
    image.thumbnail((screen_width, screen_height))
    image = ImageTk.PhotoImage(image)

    image_label = tk.Label(root, highlightthickness=0, highlightbackground="black", image=image)
    image_label.pack()

#video_label = tk.Label(root, highlightthickness=0, highlightbackground="black")
#video_label.pack()

video_path = "video.mp4"
#cap = cv2.VideoCapture(video_path)

def update_video():
    
    ret,frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        video_label.configure(image=photo)
        video_label.image = photo

        root.after(10, update_video)
    else:
        cap.release()

#update_video()
update_image()


root.mainloop()