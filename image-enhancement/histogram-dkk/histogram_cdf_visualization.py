import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image

def histogram_cdf_equalization():
    # Sembunyikan jendela utama Tkinter
    Tk().withdraw()

    # Dialog pemilihan file
    file_path = askopenfilename(title="Pilih Gambar Grayscale", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    if not file_path:
        print("Tidak ada file yang dipilih.")
        return

    # Membaca gambar dan konversi ke grayscale
    img = Image.open(file_path).convert('L')
    img_np = np.array(img)

    # Flatten ke 1D
    flat = img_np.flatten()

    # Hitung histogram dan bins untuk gambar asli
    hist_original, bins = np.histogram(flat, bins=256, range=[0, 256])
    
    # Hitung CDF untuk gambar asli
    cdf_original = hist_original.cumsum()
    cdf_original_normalized = cdf_original * float(hist_original.max()) / cdf_original.max()

    # Proses equalization
    cdf_masked = np.ma.masked_equal(cdf_original, 0)
    cdf_normalized = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
    cdf_final = np.ma.filled(cdf_normalized, 0).astype('uint8')

    # Mapping ke CDF baru
    equalized_flat = cdf_final[flat]
    equalized_img = equalized_flat.reshape(img_np.shape)

    # Hitung histogram dan CDF untuk gambar hasil equalization
    hist_equalized, _ = np.histogram(equalized_flat, bins=256, range=[0, 256])
    cdf_equalized = hist_equalized.cumsum()
    cdf_equalized_normalized = cdf_equalized * float(hist_equalized.max()) / cdf_equalized.max()

    # Visualisasi hasil
    plt.figure(figsize=(15, 10))

    # Histogram Asli
    plt.subplot(2, 2, 1)
    plt.bar(bins[:-1], hist_original, width=1, color='gray')
    plt.title("Histogram Asli")
    plt.xlim([0, 256])
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Frekuensi")

    # CDF Asli
    plt.subplot(2, 2, 2)
    plt.plot(bins[:-1], cdf_original_normalized, color='blue')
    plt.title("CDF Asli")
    plt.xlim([0, 256])
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("CDF")

    # Histogram Setelah Equalization
    plt.subplot(2, 2, 3)
    plt.bar(bins[:-1], hist_equalized, width=1, color='black')
    plt.title("Histogram Setelah Equalization")
    plt.xlim([0, 256])
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Frekuensi")

    # CDF Setelah Equalization
    plt.subplot(2, 2, 4)
    plt.plot(bins[:-1], cdf_equalized_normalized, color='red')
    plt.title("CDF Setelah Equalization")
    plt.xlim([0, 256])
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("CDF")

    plt.tight_layout()
    plt.show()

    # Simpan hasil jika perlu
    # Image.fromarray(equalized_img).save("equalized_output.png")

if __name__ == "__main__":
    histogram_cdf_equalization() 