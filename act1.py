
import cv2
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from PIL import image
imagen = Image.open("act1.jpg")
datos = np.array(imagen)

img_bgr = cv2.cvtColor(datos, cv2.COLOR_RGB2BGR)
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([35, 255, 255])

lower_purple = np.array([130, 50, 50])
upper_purple = np.array([160, 255, 255])

mask_yellow_hsv = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
mask_purple_hsv = cv2.inRange(img_hsv, lower_purple, upper_purple)

mask_total_hsv = cv2.bitwise_or(mask_yellow_hsv, mask_purple_hsv)

result_hsv = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_total_hsv)

lower_yellow_lab = np.array([150, 110, 120])
upper_yellow_lab = np.array([255, 145, 160])

lower_purple_lab = np.array([20, 140, 130])
upper_purple_lab = np.array([160, 180, 180])

mask_yellow_lab = cv2.inRange(img_lab, lower_yellow_lab, upper_yellow_lab)
mask_purple_lab = cv2.inRange(img_lab, lower_purple_lab, upper_purple_lab)

mask_total_lab = cv2.bitwise_or(mask_yellow_lab, mask_purple_lab)

result_lab = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_total_lab)

plt.figure()

plt.subplot(3,4,1)
plt.axis("off")
plt.title("Original")
plt.imshow(datos)

plt.subplot(3,4,2)
plt.axis("off")
plt.title("Filtro BGR")
plt.imshow(img_bgr)

plt.subplot(3,4,3)
plt.axis("off")
plt.title("Filtro HSV")
plt.imshow(img_hsv)

plt.subplot(3,4,4)
plt.axis("off")
plt.title("Filtro LAB")
plt.imshow(img_lab)

plt.subplot(3,4,5)
plt.axis("off")
plt.title("Filtro HSV")
plt.imshow(img_hsv)

plt.subplot(3,4,6)
plt.axis("off")
plt.title("Solo amarillo")
plt.imshow(mask_yellow_hsv)

plt.subplot(3,4,7)
plt.axis("off")
plt.title("Solo morado")
plt.imshow(mask_purple_hsv)

plt.subplot(3,4,8)
plt.axis("off")
plt.title("Combinación")
plt.imshow(result_hsv)

plt.subplot(3,4,9)
plt.axis("off")
plt.title("Filtro LAB")
plt.imshow(img_lab)

plt.subplot(3,4,10)
plt.axis("off")
plt.title("Solo amarillo")
plt.imshow(mask_yellow_lab)

plt.subplot(3,4,11)
plt.axis("off")
plt.title("Solo morado")
plt.imshow(mask_purple_lab)

plt.subplot(3,4,12)
plt.axis("off")
plt.title("Combinación")
plt.imshow(result_lab)
