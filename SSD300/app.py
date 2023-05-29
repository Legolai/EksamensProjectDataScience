import cv2
from detect import detect
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import time
import imutils


class VideoFeed:
    def __init__(self, video_source=0) -> None:
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self) -> None:
        if self.video.isOpened():
            self.video.release()


class App:
    min_score: float
    max_overlap: float
    top_k: int

    def __init__(self, window: tk.Tk, window_title: str, video_source=0, height=400, width=800) -> None:
        self.min_score = 0.4
        self.max_overlap = 0.4
        self.top_k = 200
        
        self.window = window
        self.window.configure(background="white", borderwidth=0)
        self.window.geometry(f"{width}x{height}")
        self.window.title(window_title)
        self.video_source = video_source
        self.video = VideoFeed(video_source)

        self.frame1 = tk.Frame(window, bg="black", bd=0)
        self.frame2 = tk.Frame(window, width=350, bg="white")

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.frame1, bg="black", bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.min_score_slider = tk.Scale(self.frame2, bg="white",  from_=0.01, to=1.0, resolution=0.01,
                                         orient=tk.HORIZONTAL, label="Min Score", showvalue=True, command=self.assign_min_score, length=300, tickinterval=0.2, variable=self.min_score)
        self.min_score_slider.set(self.min_score)
        self.min_score_slider.pack()
        self.max_overlap_slider = tk.Scale(self.frame2, bg="white", from_=0.01, to=1.0, resolution=0.01,
                                           orient=tk.HORIZONTAL, label="Max Overlap", showvalue=True, command=self.assign_max_overlap, length=300, tickinterval=0.2, variable=self.max_overlap)
        self.max_overlap_slider.set(self.max_overlap)
        self.max_overlap_slider.pack()
        self.top_k_slider = tk.Scale(self.frame2, bg="white", from_=1, to=1000, resolution=100,
                                     orient=tk.HORIZONTAL, label="Top K", showvalue=True, command=self.assign_top_k, length=300, tickinterval=200, variable=self.top_k)
        self.top_k_slider.set(self.top_k)
        self.top_k_slider.pack()
        
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.frame2.pack(side=tk.RIGHT, fill=tk.BOTH)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def assign_min_score(self, value: str):
        self.min_score = float(value)

    def assign_max_overlap(self, value: str):
        self.max_overlap = float(value)
    
    def assign_top_k(self, value: str):
        self.top_k = float(value)

    def update(self):
        ret, frame = self.video.get_frame()
        if ret:
            
            frame = cv2.flip(frame, 1)
            to_width = self.frame1.winfo_width()
            width = 600 if to_width <= 1 else to_width
            frame = imutils.resize(frame, width=width )
            img_pil =   Image.fromarray(frame)
            detected_img = detect(img_pil, min_score=self.min_score,
                                max_overlap=self.max_overlap, top_k=self.top_k)
            self.photo = ImageTk.PhotoImage(image=detected_img)
            self.canvas.create_image(
                0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

if __name__ == '__main__':
    App(tk.Tk(), "Pigeon detector")
