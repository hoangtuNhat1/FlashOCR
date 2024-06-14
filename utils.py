from customtkinter import *   
import pynput
import cv2
import numpy as np
from PIL import Image
import mss
import re 
import jaconv
from transformers import AutoFeatureExtractor, AutoTokenizer, VisionEncoderDecoderModel, TrOCRProcessor
import clipboard
model_path = ''
feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = VisionEncoderDecoderModel.from_pretrained(model_path).to('cuda')
def post_process(text):
    text = ''.join(text.split())
    text = text.replace('…', '...')
    text = re.sub('[・.]{2,}', lambda x: (x.end() - x.start()) * '.', text)
    text = jaconv.h2z(text, ascii=True, digit=True)
    return text
def predict(image):
#     image = image.convert('L').convert('RGB')
    pixel_values = feature_extractor(image, return_tensors="pt").pixel_values.to('cuda')
    ouput = model.generate(pixel_values)[0]
    text = tokenizer.decode(ouput, skip_special_tokens=True)
    text = post_process(text)
    return text