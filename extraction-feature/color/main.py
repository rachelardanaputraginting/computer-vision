# === Fitur Ekstraksi Warna ===
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew
from skimage.measure import label
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime

# ----------------- PILIH GAMBAR DARI FILE EXPLORER -----------------
def pilih_gambar():
    Tk().withdraw()
    path = askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    return path

# ----------------- HISTOGRAM WARNA -----------------
def histogram_warna(img, color_space='RGB', bins=32):
    if color_space == 'HSV':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif color_space == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    channels = ('R', 'G', 'B') if color_space == 'RGB' else ('H', 'S', 'V')
    colors = ('red', 'green', 'blue')
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.title('Gambar')

    plt.subplot(1, 2, 2)
    for i, col in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [bins], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, bins])
    plt.title(f'Histogram Warna ({color_space})')
    plt.tight_layout()
    plt.show()

# ----------------- MOMEN WARNA -----------------
def momen_warna(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    stats = []
    nama_channel = ['Red', 'Green', 'Blue']
    for i in range(3):
        channel = img_rgb[:, :, i].flatten()
        mean = np.mean(channel)
        var = np.var(channel)
        skewness = skew(channel)
        kurt = kurtosis(channel)
        stats.append((mean, var, skewness, kurt))

    # Create a figure with 2 subplots
    plt.figure(figsize=(15, 6))
    
    # First subplot: Original image
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title('Gambar Asli')
    plt.axis('off')

    # Second subplot: Color moments visualization
    plt.subplot(1, 2, 2)
    x = np.arange(len(nama_channel))
    width = 0.2

    # Plot each moment type
    bars1 = plt.bar(x - width*1.5, [s[0] for s in stats], width, label='Mean', color='red')
    bars2 = plt.bar(x - width*0.5, [s[1] for s in stats], width, label='Variance', color='green')
    bars3 = plt.bar(x + width*0.5, [s[2] for s in stats], width, label='Skewness', color='blue')
    bars4 = plt.bar(x + width*1.5, [s[3] for s in stats], width, label='Kurtosis', color='purple')

    # Add value labels on top of each bar
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

    plt.xlabel('Channel')
    plt.ylabel('Value')
    plt.title('Color Moments')
    plt.xticks(x, nama_channel)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

    print("\nMomen Warna (R, G, B):")
    for i, name in enumerate(nama_channel):
        print(f"{name} - Mean: {stats[i][0]:.2f}, Var: {stats[i][1]:.2f}, Skewness: {stats[i][2]:.2f}, Kurtosis: {stats[i][3]:.2f}")

# ----------------- CCV -----------------
def hitung_ccv(img, tau=100):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    bins = [8, 3, 3]
    bin_total = np.prod(bins)
    quantized = np.zeros((h, w), dtype=int)

    for i in range(h):
        for j in range(w):
            h_val = int(hsv[i, j, 0] * bins[0] / 180)
            s_val = int(hsv[i, j, 1] * bins[1] / 256)
            v_val = int(hsv[i, j, 2] * bins[2] / 256)
            quantized[i, j] = h_val * bins[1] * bins[2] + s_val * bins[2] + v_val

    alpha = np.zeros(bin_total)
    beta = np.zeros(bin_total)
    output = np.zeros_like(img)

    for bin_idx in range(bin_total):
        mask = (quantized == bin_idx).astype(np.uint8)
        labeled = label(mask, connectivity=1)
        for region_id in range(1, np.max(labeled)+1):
            region_mask = (labeled == region_id)
            size = np.sum(region_mask)
            if size >= tau:
                alpha[bin_idx] += size
                output[region_mask] = (0, 255, 0)  # Koheren - Hijau
            else:
                beta[bin_idx] += size
                output[region_mask] = (0, 0, 255)  # Tidak Koheren - Merah

    # Create figure with 3 subplots
    plt.figure(figsize=(20, 10))
    
    # Original image
    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Gambar Asli")
    plt.axis('off')

    # CCV result
    plt.subplot(2, 2, 2)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title("Hasil CCV (Hijau=Koheren, Merah=Tidak)")
    plt.axis('off')

    # CCV values plot - Koheren
    plt.subplot(2, 2, 3)
    x = np.arange(bin_total)
    width = 0.8
    
    bars1 = plt.bar(x, alpha, width, label='Koheren', color='green')
    
    # Add value labels on top of each bar
    for bar in bars1:
        height = bar.get_height()
        if height > 0:  # Only show non-zero values
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', rotation=90)

    plt.xlabel('Bin')
    plt.ylabel('Jumlah Pixel')
    plt.title('Nilai CCV Koheren')
    plt.xticks(x)
    plt.grid(True, linestyle='--', alpha=0.7)

    # CCV values plot - Tidak Koheren
    plt.subplot(2, 2, 4)
    bars2 = plt.bar(x, beta, width, label='Tidak Koheren', color='red')
    
    # Add value labels on top of each bar
    for bar in bars2:
        height = bar.get_height()
        if height > 0:  # Only show non-zero values
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', rotation=90)

    plt.xlabel('Bin')
    plt.ylabel('Jumlah Pixel')
    plt.title('Nilai CCV Tidak Koheren')
    plt.xticks(x)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

    # Print numerical values in console
    print("\nNilai CCV untuk setiap bin:")
    print("Bin\tKoheren\tTidak Koheren")
    print("-" * 30)
    for i in range(bin_total):
        print(f"{i}\t{int(alpha[i])}\t{int(beta[i])}")

    return alpha, beta

def simpan_fitur(nama, fitur):
    filename = f"output/fitur_{nama}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(", ".join(map(str, fitur)))
    print(f"\nFitur disimpan di: {filename}")

# ----------------- MENU UTAMA -----------------
def main():
    print("=== Program Analisis Gambar: Histogram | Momen | CCV ===")
    path = pilih_gambar()
    if not path:
        print("Tidak ada file dipilih.")
        return

    img = cv2.imread(path)
    if img is None:
        print("Gagal memuat gambar.")
        return

    while True:
        print("\n--- MENU ---")
        print("1. Histogram Warna")
        print("2. Momen Warna")
        print("3. Color Coherence Vector (CCV)")
        print("4. Keluar")

        pilihan = input("Pilih (1/2/3/4): ")

        if pilihan == '1':
            space = input("Gunakan color space RGB atau HSV? (default RGB): ").upper()
            if space not in ['RGB', 'HSV']:
                space = 'RGB'
            histogram_warna(img, color_space=space)

        elif pilihan == '2':
            momen_warna(img)

        elif pilihan == '3':
            tau_input = input("Masukkan nilai ambang tau (default 100): ")
            tau = int(tau_input) if tau_input.strip().isdigit() else 100
            alpha, beta = hitung_ccv(img, tau)
            print("\nContoh nilai CCV:")
            for i in range(10):
                print(f"Bin {i}: Koheren = {int(alpha[i])}, Tidak = {int(beta[i])}")

        elif pilihan == '4':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Ulangi.")

# ----------------- JALANKAN PROGRAM -----------------
if __name__ == '__main__':
    main()
