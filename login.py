import tkinter as tk
from PIL import Image, ImageTk
import cv2

class VideoThumbnail:
    def __init__(self, filename, master):
        self.filename = filename
        self.master = master
        self.thumbnail = self.generate_thumbnail()

    def generate_thumbnail(self):
        cap = cv2.VideoCapture(self.filename)
        _, frame = cap.read()
        cap.release()
        if frame is None:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(img)
        return thumbnail

class ImageThumbnail:
    def __init__(self, filename, master):
        self.filename = filename
        self.master = master
        self.thumbnail = self.generate_thumbnail()

    def generate_thumbnail(self):
        img = Image.open(self.filename)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(img)
        return thumbnail

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Media Thumbnails")

        # Create list of filenames
        self.filenames = ["car.png"]

        # Create list of thumbnail objects
        self.thumbnails = []
        for filename in self.filenames:
            if filename.endswith(".jpg") or filename.endswith(".png"):
                thumbnail = ImageThumbnail(filename, master)
            elif filename.endswith(".mp4") or filename.endswith(".avi"):
                thumbnail = VideoThumbnail(filename, master)
            self.thumbnails.append(thumbnail)

        # Create a grid of thumbnail images
        self.thumbnail_frame = tk.Frame(master)
        self.thumbnail_frame.pack()
        for i, thumbnail in enumerate(self.thumbnails):
            if thumbnail.thumbnail is None:
                continue
            thumbnail_label = tk.Label(self.thumbnail_frame, image=thumbnail.thumbnail)
            thumbnail_label.grid(row=i//3, column=i%3, padx=5, pady=5)
            thumbnail_label.bind("<Button-1>", lambda event, index=i: self.view_media(index))

    def view_media(self, index):
        filename = self.filenames[index]
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(filename)
            img.show()
        elif filename.endswith(".mp4") or filename.endswith(".avi"):
            cap = cv2.VideoCapture(filename)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

root = tk.Tk()
app = App(root)
root.mainloop()
