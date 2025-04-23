import numpy as np
import cv2 as cv  # Seharusnya cv2, bukan cv4
from matplotlib import pyplot as plt

img = cv.imread("ronaldo.jpg", cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists"  # os.path.exists, bukan op.part.exists
edges = cv.Canny(img, 100, 200)

plt.subplot(121), plt.imshow(img, cmap="gray")  # Syntax yang benar untuk subplot dan imshow
plt.title("Original Image"), plt.xticks([]), plt.yticks([])  # "Image" bukan "Imahe"
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title("Edge Image"), plt.xticks([]), plt.yticks([])

plt.show()