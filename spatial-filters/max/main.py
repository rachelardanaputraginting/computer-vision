import numpy as np
import scipy.ndimage
import os
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Buat jendela Tkinter tersembunyi untuk memilih file
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

if not file_path:
    print("No file selected. Exiting...")
    exit()

# Buka gambar dalam mode grayscale ('L')
img = Image.open(file_path).convert('L')

# Konversi gambar ke array numpy
img_array = np.array(img)

# Kernel rata-rata 5x5
K = np.ones((5, 5)) / 25

# Konvolusi dengan kernel
B = scipy.ndimage.convolve(img_array, K)

# Konversi kembali ke gambar
B = Image.fromarray(B)

# Simpan hasil gambar yang difilter
B.save('mean2.png')

# Buka gambar lagi untuk filter Median
img1 = Image.open(file_path).convert('L')
img2 = img1.filter(ImageFilter.MedianFilter(size=3))

# Konversi gambar ke array NumPy sebelum ditampilkan
img1_array = np.array(img1)
img2_array = np.array(img2)

# Buat folder output jika belum ada
os.makedirs("output", exist_ok=True)

# Simpan hasil filter
img2.save("output/median_output.png")

# Tampilkan hasil dengan matplotlib
fig = plt.figure()
plt.gray()
ax1 = fig.add_subplot(121)  # Subplot pertama
ax2 = fig.add_subplot(122)  # Subplot kedua

ax1.imshow(img1)  # Pastikan gambar original ditampilkan dengan benar
ax1.set_title("Original")

ax2.imshow(img2_array, cmap='gray')  # Pastikan gambar yang difilter juga ditampilkan dengan benar
ax2.set_title("Filtered")

plt.show()
