import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
import re

image = Image.open("receipt.jpg")
text = pytesseract.image_to_string(image)

pattern_items = r"([A-Za-z\s]+)\s+\d+\s(\$\d+\.\d{2})"
pattern_resume = r"([A-Za-z\s]+)\s(\$\d+\.\d{2})"

items = re.findall(pattern_items, text)
resume = re.findall(pattern_resume, text)

for item, price in items:
    print(f"{item.strip()} → {price}")

for detail, total in resume: 
    print(f"{detail.strip()} → {total}")

