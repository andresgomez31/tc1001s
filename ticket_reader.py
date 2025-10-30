import pytesseract
from PIL import Image
import re

def extract_text_from_image(image_path):
    """Lee el texto de una imagen usando OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_items_and_resume(text):
    """Extrae los productos con precios y el resumen del ticket usando regex."""
    pattern_items = r"([A-Za-z\s]+)\s+\d+\s(\$\d+\.\d{2})"
    pattern_resume = r"([A-Za-z\s]+)\s(\$\d+\.\d{2})"

    items = re.findall(pattern_items, text)
    resume = re.findall(pattern_resume, text)

    return items, resume

def print_extracted_data(items, resume):
    """Imprime los resultados del OCR y la extracción."""
    print("Artículos encontrados:")
    for item, price in items:
        print(f"{item.strip()} → {price}")

    print("\nResumen:")
    for detail, total in resume: 
        print(f"{detail.strip()} → {total}")

def main():
    image_path = "receipt.jpg"
    text = extract_text_from_image(image_path)
    items, resume = extract_items_and_resume(text)
    print_extracted_data(items, resume)

if __name__ == "__main__":
    main()
