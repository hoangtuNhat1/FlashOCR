# FlashOCR Project

Welcome to FlashOCR! This application is designed to accelerate your Japanese learning experience using Optical Character Recognition (OCR) technology. It's fast, user-friendly, and easy to install. Should you encounter any issues, feel free to direct message (DM) me for support.

## Demo

![OCR Demo](asset/demo.gif)

## Installation

### Prerequisites

Ensure that Python (version 3.6 or later) is installed on your machine. You can download Python from [python.org](https://www.python.org/downloads/).

### Setup

Follow these steps to set up the FlashOCR project on your local machine:

1. **Clone the repository**
   ```bash
   git clone https://github.com/PhamQuangNhut/FlashOCR
   cd FlashOCR
2. **Install required packages**
   ```bash
   pip install -r requirements.txt
3. **Download OCR model weights**
   Download the [model weights](https://drive.google.com/file/d/1ql_28Un1OhI_lUUtkie0o5SggplvNRC5/view?usp=sharing) required for the OCR. After downloading, update the model path in `utils.py` to point to the downloaded weights.
## Usage
  ### Notes
  - This project utilizes the [Manga OCR](https://github.com/kha-white/manga-ocr/tree/master) for the OCR model. You can replace it with another model if desired.
  - It's recommended to use a virtual environment to avoid conflicts with other packages.
  - If you encounter any issues during installation, ensure your pip is up-to-date (pip install --upgrade pip).
  - For best results, use high-quality images with clear, legible text.
  ### Run 
  To run the application, use the following command:
  
   ```bash
   python app.py
  
   

