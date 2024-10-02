from customtkinter import CTk, CTkLabel, CTkFrame, CTkCanvas
import mss
from utils import predict   
from PIL import Image   
import cv2  
import numpy as np 
import clipboard

class App(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("OCR")
        
        self.mainFrame = CTkFrame(self)
        self.mainFrame.pack()
        
        self.label = CTkLabel(self.mainFrame, text="Press 'Enter' to start selecting points...")
        self.label.pack(pady=20)
        
        self.overlayFrame = CTkFrame(self)
        
        self.canvas = CTkCanvas(self.overlayFrame)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)
        self.bind("<KeyPress>", self.handle_keypress)
        self.canvas.pack(fill="both", expand=True)  
        
        self.first_click_x = None
        self.first_click_y = None
        self.rectangle_id = None
        self.click_count = 0
        self.allow_drawing = False

    # Update rectangle position as the mouse moves
    def update_rectangle(self, event):
        if self.rectangle_id:
            self.canvas.coords(self.rectangle_id, self.first_click_x, self.first_click_y, event.x, event.y)

    # Handle the mouse click to start and stop drawing the rectangle
    def handle_click(self, event):
        if self.first_click_x is None and self.first_click_y is None:
            self.first_click_x = event.x
            self.first_click_y = event.y
            self.rectangle_id = self.canvas.create_rectangle(self.first_click_x, self.first_click_y, self.first_click_x, self.first_click_y, outline='red')
        else:
            self.update_rectangle(event)

    # Update the rectangle while dragging the mouse
    def handle_motion(self, event):
        if self.first_click_x is not None and self.first_click_y is not None and self.allow_drawing:
            self.update_rectangle(event)

    # Handle key press events
    def handle_keypress(self, event):
        if event.keysym == 'Return':  # 'Enter' key
            if not self.allow_drawing:
                # Start selecting points
                self.mainFrame.pack_forget()
                self.attributes('-fullscreen', True)
                self.wm_attributes('-alpha', 0.5)
                self.overlayFrame.pack(fill="both", expand=True)
                self.allow_drawing = True
            else:
                # Finalize the selection and run OCR
                self.overlayFrame.pack_forget()
                self.attributes('-fullscreen', False)
                self.wm_attributes('-alpha', 1)
                self.mainFrame.pack(fill="both", expand=True)
                self.run(self.first_click_x, self.first_click_y, self.canvas.winfo_pointerx(), self.canvas.winfo_pointery())
                self.first_click_x = None
                self.first_click_y = None
                self.rectangle_id = None
                self.canvas.delete("all")
                self.allow_drawing = False
        elif event.keysym == 'Escape':  # Escape key to cancel selection
            self.overlayFrame.pack_forget()
            self.attributes('-fullscreen', False)
            self.wm_attributes('-alpha', 1)
            self.mainFrame.pack(fill="both", expand=True)
            self.first_click_x = None
            self.first_click_y = None
            self.rectangle_id = None
            self.canvas.delete("all")
            self.allow_drawing = False

    # Run the OCR process after the rectangle is selected
    def run(self, x1, y1, x2, y2):
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
        cropped_image = img_array[smaller_y:bigger_y, smaller_x:smaller_x]
        result = predict(cropped_image)
        self.label.configure(text=result + "\n" + "Press 'Enter' to start selecting points...")
        clipboard.copy(result)

if __name__ == "__main__":
    app = App()
    app.mainloop()
