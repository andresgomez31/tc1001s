import pytesseract
from PIL import Image
import re
import cv2
import numpy as np

def preprocess_image(image_path):
    """Preprocesa la imagen para mejorar la lectura OCR."""
    # Cargar imagen con OpenCV
    img = cv2.imread(image_path)

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo para mejorar contraste
    gray = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Eliminar ruido con desenfoque
    gray = cv2.medianBlur(gray, 3)

    # Convertir de nuevo a objeto PIL
    processed_image = Image.fromarray(gray)
    return processed_image


def extract_text_from_image(image_path):
    """Lee el texto de una imagen usando OCR."""
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang="eng")  # Cambia a "spa" si el ticket está en español
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
    print("📋 Artículos encontrados:")
    for item, price in items:
        print(f"{item.strip()} → {price}")

    print("\n💰 Resumen:")
    for detail, total in resume: 
        print(f"{detail.strip()} → {total}")


def main():
    image_path = "receipt.jpg"
    text = extract_text_from_image(image_path)
    items, resume = extract_items_and_resume(text)
    print_extracted_data(items, resume)


if __name__ == "__main__":
    main()