import pynput
import cv2
import numpy as np
from PIL import Image
import mss
import re 
import jaconv
from transformers import AutoFeatureExtractor, AutoTokenizer, VisionEncoderDecoderModel, TrOCRProcessor
import clipboard
model_path = './FinalModel/'
feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = VisionEncoderDecoderModel.from_pretrained(model_path).to('cuda')
point_a = None
point_b = None
click_count = 0
def on_click(x, y, button, pressed):
    global point_a, point_b, click_count

    if pressed and button == pynput.mouse.Button.left:
        if click_count == 0:
            point_a = (x, y)
            click_count += 1
            print("Click on the second point to get the end coordinate.")
        elif click_count == 1:
            point_b = (x, y)
            click_count = 0
            return False

def on_press(key):
    global point_a, point_b, click_count
    if key == pynput.keyboard.KeyCode(char='.'):
         return False
def start_listening():
     print("Press '.' to start selecting points...")
     with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()
     print("Click on the first point to get the start coordinate.")
     with pynput.mouse.Listener(on_click=on_click) as listener:
          listener.join()
def post_process(text):
    text = ''.join(text.split())
    text = text.replace('…', '...')
    text = re.sub('[・.]{2,}', lambda x: (x.end() - x.start()) * '.', text)
    text = jaconv.h2z(text, ascii=True, digit=True)
    return text
def infer(image):
#     image = image.convert('L').convert('RGB')
    pixel_values = feature_extractor(image, return_tensors="pt").pixel_values.to('cuda')
    ouput = model.generate(pixel_values)[0]
    text = tokenizer.decode(ouput, skip_special_tokens=True)
    text = post_process(text)
    return text
# Main function
def main():
     while True:
          start_listening()
          x1, y1 = point_a
          x2, y2 = point_b
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
          result = infer(cropped_image)
          clipboard.copy(result)
# Run the main function
if __name__ == "__main__":
    main()


