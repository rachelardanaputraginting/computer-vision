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
    """
    Menampilkan histogram warna dari gambar dalam format RGB atau HSV.
    
    Parameter:
    - img: Gambar input
    - color_space: Ruang warna yang digunakan ('RGB' atau 'HSV')
    - bins: Jumlah bin untuk histogram (default: 32)
    
    Output:
    - Menampilkan gambar asli dan histogram warna untuk setiap channel
    - Histogram menunjukkan distribusi intensitas warna
    """
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
    plt.title('Gambar Asli')

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
    """
    Menghitung dan menampilkan momen warna (mean, variance, skewness, kurtosis) untuk setiap channel RGB.
    
    Parameter:
    - img: Gambar input
    
    Output:
    - Menampilkan gambar asli dan tabel momen warna
    - Tabel berisi nilai statistik untuk setiap channel warna
    - Momen warna membantu menganalisis distribusi warna dalam gambar
    """
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

    # Buat figure dengan 2 subplot
    plt.figure(figsize=(15, 6))
    
    # Subplot pertama: Gambar asli
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title('Gambar Asli')
    plt.axis('off')

    # Subplot kedua: Tampilan numerik
    plt.subplot(1, 2, 2)
    plt.axis('off')  # Matikan axis
    
    # Buat data tabel
    table_data = [
        ['Channel', 'Mean', 'Variance', 'Skewness', 'Kurtosis'],
        ['Red', f'{stats[0][0]:.2f}', f'{stats[0][1]:.2f}', f'{stats[0][2]:.2f}', f'{stats[0][3]:.2f}'],
        ['Green', f'{stats[1][0]:.2f}', f'{stats[1][1]:.2f}', f'{stats[1][2]:.2f}', f'{stats[1][3]:.2f}'],
        ['Blue', f'{stats[2][0]:.2f}', f'{stats[2][1]:.2f}', f'{stats[2][2]:.2f}', f'{stats[2][3]:.2f}']
    ]
    
    # Buat tabel
    table = plt.table(cellText=table_data,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.2, 0.2, 0.2, 0.2, 0.2])
    
    # Styling tabel
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)
    
    # Styling header
    for i in range(5):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(color='white')
    
    # Styling sel data
    for i in range(1, 4):
        for j in range(5):
            table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    plt.title('Analisis Momen Warna', pad=20)
    plt.tight_layout()
    plt.show()

# ----------------- CCV -----------------
def hitung_ccv(img, tau=100):
    """
    Menghitung dan menampilkan Color Coherence Vector (CCV) dari gambar.
    
    Parameter:
    - img: Gambar input
    - tau: Threshold untuk menentukan koherensi (default: 100)
    
    Output:
    - Menampilkan gambar asli dan hasil CCV
    - Menampilkan tabel nilai CCV untuk setiap bin
    - CCV membantu menganalisis distribusi warna dan tekstur dalam gambar
    """
    # Resize gambar jika terlalu besar
    max_dimension = 400  # Dimensi maksimum untuk pemrosesan
    h, w = img.shape[:2]
    if max(h, w) > max_dimension:
        scale = max_dimension / max(h, w)
        new_h, new_w = int(h * scale), int(w * scale)
        img = cv2.resize(img, (new_w, new_h))
        print(f"Gambar di-resize ke {new_w}x{new_h} untuk komputasi lebih cepat")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    # Kurangi jumlah bin untuk komputasi lebih cepat
    bins = [4, 2, 2]  # Dikurangi dari [8, 3, 3]
    bin_total = np.prod(bins)
    
    # Kuantisasi vektor
    h_quantized = np.floor(hsv[:,:,0] * bins[0] / 180.0).astype(int)
    s_quantized = np.floor(hsv[:,:,1] * bins[1] / 256.0).astype(int)
    v_quantized = np.floor(hsv[:,:,2] * bins[2] / 256.0).astype(int)
    
    # Hitung indeks bin untuk setiap pixel
    quantized = h_quantized * bins[1] * bins[2] + s_quantized * bins[2] + v_quantized

    alpha = np.zeros(bin_total)
    beta = np.zeros(bin_total)
    output = np.zeros_like(img)

    # Proses setiap bin
    for bin_idx in range(bin_total):
        # Dapatkan mask untuk bin saat ini
        mask = (quantized == bin_idx)
        if not np.any(mask):  # Lewati jika tidak ada pixel dalam bin ini
            continue
            
        # Label komponen terhubung
        labeled = label(mask.astype(np.uint8), connectivity=1)
        
        # Dapatkan label unik (kecuali background 0)
        unique_labels = np.unique(labeled)[1:]
        
        # Proses setiap region
        for region_id in unique_labels:
            region_mask = (labeled == region_id)
            size = np.sum(region_mask)
            
            if size >= tau:
                alpha[bin_idx] += size
                output[region_mask] = (0, 255, 0)  # Koheren - Hijau
            else:
                beta[bin_idx] += size
                output[region_mask] = (0, 0, 255)  # Tidak Koheren - Merah

    # Buat figure dengan 2 subplot
    plt.figure(figsize=(15, 6))
    
    # Gambar asli
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Gambar Asli")
    plt.axis('off')

    # Hasil CCV
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title("Hasil CCV (Hijau=Koheren, Merah=Tidak)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Buat figure untuk tampilan numerik
    plt.figure(figsize=(15, 8))
    plt.axis('off')
    
    # Buat data tabel
    table_data = [['Bin', 'Koheren', 'Tidak Koheren']]
    for i in range(bin_total):
        if alpha[i] > 0 or beta[i] > 0:  # Hanya tampilkan nilai non-zero
            table_data.append([str(i), str(int(alpha[i])), str(int(beta[i]))])
    
    # Buat tabel
    table = plt.table(cellText=table_data,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.2, 0.4, 0.4])
    
    # Styling tabel
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)
    
    # Styling header
    for i in range(3):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(color='white')
    
    # Styling sel data
    for i in range(1, len(table_data)):
        for j in range(3):
            table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    plt.title('Analisis Color Coherence Vector (CCV)', pad=20)
    plt.tight_layout()
    plt.show()

    return alpha, beta

def simpan_fitur(nama, fitur):
    filename = f"output/fitur_{nama}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(", ".join(map(str, fitur)))
    print(f"\nFitur disimpan di: {filename}")

# ----------------- MENU UTAMA -----------------
def main():
    print("=== Program Analisis Gambar: Histogram | Momen | CCV ===")
    print("\nPilihan Analisis:")
    print("1. Histogram Warna - Menampilkan distribusi intensitas warna dalam format RGB/HSV")
    print("2. Momen Warna - Menampilkan statistik warna (mean, variance, skewness, kurtosis)")
    print("3. Color Coherence Vector (CCV) - Menganalisis distribusi warna dan tekstur")
    print("4. Keluar")
    
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

        elif pilihan == '4':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Ulangi.")

# ----------------- JALANKAN PROGRAM -----------------
if __name__ == '__main__':
    main()
