import numpy as np
from PIL import Image  # Menggunakan Pillow untuk membaca dan menyimpan gambar
import scipy.ndimage

# Membuka gambar dan mengonversinya ke grayscale
image_path = './images/water-fall.jpg'
a = Image.open(image_path).convert('L')  # Konversi ke grayscale

# Mengonversi gambar PIL ke array NumPy
a = np.array(a)

# Inisialisasi filter berukuran 5x5
# Filter dibagi oleh 25 untuk normalisasi
k = np.ones((5, 5)) / 25

# Melakukan konvolusi
b = scipy.ndimage.convolve(a, k)

# Memastikan nilai piksel tetap dalam rentang 0-255
b = np.clip(b, 0, 255)

# Mengonversi hasil ndarray kembali ke gambar PIL
b_image = Image.fromarray(b.astype(np.uint8))

# Menyimpan hasil gambar
output_path = './images/output/water-fall.jpg'
b_image.save(output_path)

print(f"Hasil disimpan di: {output_path}")