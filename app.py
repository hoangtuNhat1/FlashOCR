import tkinter as tk
from customtkinter import CTk, CTkLabel, CTkFrame
import pynput
import mss
from utils import predict   
from PIL import Image   
import cv2  
import numpy as np 
import clipboard
import threading
import time
class App(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("OCR")
        self.mainFrame = CTkFrame(self)
        self.label = CTkLabel(self.mainFrame, text="Press '.' to start selecting points...")
        self.overlayFrame = CTkFrame(self)
        self.label.pack(pady=20)
        self.point_a = None 
        self.point_b = None  
        self.click_count = 0
        self.mainFrame.pack()
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        
    def on_press(self, key):
          if key == pynput.keyboard.KeyCode(char='.'):
               self.mainFrame.pack_forget()
               self.attributes('-fullscreen', True)
               self.wm_attributes('-alpha',0.5)
               self.overlayFrame.pack(fill="both", expand=True)
               return False
    def on_click(self, x, y, button, pressed):
          if pressed and button == pynput.mouse.Button.left:
               if self.click_count == 0:
                    self.point_a = (x, y)
                    self.click_count += 1
               elif self.click_count == 1:
                    self.point_b = (x, y)
                    self.click_count = 0
                    self.overlayFrame.pack_forget()
                    self.attributes('-fullscreen', False)
                    self.wm_attributes('-alpha',1)
                    self.mainFrame.pack(fill="both", expand=True)
                    return False
    def start_listening(self):
          with pynput.keyboard.Listener(on_press=self.on_press) as listener:
               listener.join()
          with pynput.mouse.Listener(on_click=self.on_click) as listener:
               listener.join()
    def run(self) : 
         while True: 
               self.start_listening()
               x1, y1 = self.point_a
               x2, y2 = self.point_b
               smaller_x = min(x1, x2)
               smaller_y = min(y1, y2)
               bigger_x = max(x1, x2)
               bigger_y = max(y1, y2)
               with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    sct_img = sct.grab(monitor)
               img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
               img_array = np.array(img)
               img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
               cropped_image = img_array[smaller_y:bigger_y, smaller_x:bigger_x]
               result = predict(cropped_image)
               self.label.configure(text=result+"\n"+"Press '.' to start selecting points...")
               clipboard.copy(result)
if __name__ == "__main__":
    app = App()
    app.mainloop()
