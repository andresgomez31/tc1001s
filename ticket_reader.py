"""
Script para procesar recibos usando OCR.

Este módulo carga una imagen de un recibo, la preprocesa usando OpenCV
para mejorar la legibilidad, extrae texto con Tesseract, y luego
analiza el texto con regex para encontrar artículos y totales.
"""

# 1. Importaciones de la biblioteca estándar (ordenadas)
import re

# 2. Importaciones de terceros (ordenadas)
import cv2
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image_path: str) -> Image.Image:
    """
    Carga y preprocesa una imagen para mejorar los resultados de OCR.

    El preprocesamiento incluye conversión a escala de grises,
    umbral adaptativo y eliminación de ruido.

    Args:
        image_path (str): La ruta al archivo de imagen.

    Returns:
        Image.Image: Una imagen de objeto PIL preprocesada.
    """
    # Cargar la imagen usando OpenCV
    img = cv2.imread(image_path)

    # Convertir a escala de grises, ya que OCR funciona mejor sin color
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo para manejar diferentes condiciones de iluminación.
    # Esto crea una imagen binaria (blanco y negro) que es más fácil de leer.
    # 31: El tamaño del bloque de píxeles para calcular el umbral.
    # 2: Constante C restada de la media (ajuste fino).
    gray = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Aplicar un desenfoque de mediana para eliminar el ruido de "sal y pimienta"
    # Un kernel de 3x3 es ligero y efectivo para ruido pequeño.
    gray = cv2.medianBlur(gray, 3)

    # Convertir el array de NumPy (OpenCV) a un objeto PIL (requerido por Tesseract)
    processed_image = Image.fromarray(gray)
    return processed_image


def extract_text_from_image(image_path: str) -> str:
    """
    Extrae texto de una imagen usando Tesseract OCR.

    Args:
        image_path (str): La ruta al archivo de imagen.

    Returns:
        str: El texto crudo extraído de la imagen.
    """
    image = preprocess_image(image_path)
    
    # Usar Tesseract para convertir la imagen preprocesada en texto
    # lang="eng" es para inglés. Cambiar a "spa" si el recibo está en español.
    text = pytesseract.image_to_string(image, lang="eng")
    return text


def extract_items_and_resume(text: str) -> tuple:
    """
    Analiza el texto crudo del OCR para extraer artículos y un resumen.

    Usa expresiones regulares (regex) para encontrar patrones que coincidan
    con los artículos (texto + precio) y el resumen (total, impuestos, etc.).

    Args:
        text (str): El texto crudo de Tesseract.

    Returns:
        tuple: Una tupla conteniendo (lista_de_items, lista_de_resumen).
    """
    # Patrón para artículos: (Texto) (dígitos) ($precio)
    # Ej: "PRODUCTO X 1 $10.00"
    pattern_items = r"([A-Za-z\s]+)\s+\d+\s(\$\d+\.\d{2})"
    
    # Patrón para resumen: (Texto) ($precio)
    # Ej: "SUBTOTAL $20.00"
    pattern_resume = r"([A-Za-z\s]+)\s(\$\d+\.\d{2})"

    items = re.findall(pattern_items, text)
    resume = re.findall(pattern_resume, text)

    return items, resume


def print_extracted_data(items: list, resume: list):
    """
    Imprime los datos extraídos de forma legible en la consola.

    Args:
        items (list): Lista de tuplas (item, precio).
        resume (list): Lista de tuplas (detalle, total).
    """
    print("📋 Artículos encontrados:")
    if not items:
        print("...ninguno.")
        
    for item, price in items:
        # .strip() limpia espacios en blanco al inicio o final
        print(f"{item.strip()} → {price}")

    print("\n💰 Resumen:")
    if not resume:
        print("...ninguno.")
        
    for detail, total in resume:
        print(f"{detail.strip()} → {total}")


def main():
    """
    Función principal para ejecutar el flujo completo del script.
    """
    try:
        image_path = "receipt.jpg"
        text = extract_text_from_image(image_path)
        items, resume = extract_items_and_resume(text)
        print_extracted_data(items, resume)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{image_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()