from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
import math

# Membuat direktori output jika belum ada
os.makedirs("output", exist_ok=True)

def tampilkan_menu():
    """Menampilkan menu transformasi"""
    print("\n=== MENU TRANSFORMASI PIXEL ===")
    print("1. Power Law Transformation")
    print("2. Log Transformation")
    print("3. Contrast Stretching")
    print("4. Histogram Equalization")
    print("0. Keluar")

def pilih_gambar():
    """Fungsi untuk memilih file gambar menggunakan dialog"""
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar",
        filetypes=[("File Gambar", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    
    return file_path

def tampilkan_gambar_dan_histogram(img_array, transformed_array, title_original, title_transformed):
    """Menampilkan gambar asli dan hasil transformasi beserta histogram dan CDF"""
    plt.figure(figsize=(12, 6))
    
    # Gambar asli
    plt.subplot(2, 2, 1)
    plt.imshow(img_array, cmap='gray')
    plt.title(title_original)
    plt.axis('off')
    
    # Histogram dan CDF asli
    plt.subplot(2, 2, 2)
    hist_orig, bins_orig = np.histogram(img_array.ravel(), bins=256, range=[0, 256])
    cdf_orig = hist_orig.cumsum()
    ax1 = plt.gca()
    ax1.bar(bins_orig[:-1], hist_orig, width=1, color='gray', alpha=0.5, label='Histogram')
    ax2 = ax1.twinx()
    ax2.plot(cdf_orig, color='red', label='CDF')
    plt.title(f"Histogram dan CDF {title_original}")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Gambar hasil transformasi
    plt.subplot(2, 2, 3)
    plt.imshow(transformed_array, cmap='gray')
    plt.title(title_transformed)
    plt.axis('off')
    
    # Histogram dan CDF hasil transformasi
    plt.subplot(2, 2, 4)
    hist_trans, bins_trans = np.histogram(transformed_array.ravel(), bins=256, range=[0, 256])
    cdf_trans = hist_trans.cumsum()
    ax1 = plt.gca()
    ax1.bar(bins_trans[:-1], hist_trans, width=1, color='black', alpha=0.5, label='Histogram')
    ax2 = ax1.twinx()
    ax2.plot(cdf_trans, color='red', label='CDF')
    plt.title(f"Histogram dan CDF {title_transformed}")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.show()

def power_law_transform(img_array, gamma=1.0):
    """Menerapkan power law transformation"""
    # Normalize the image to [0,1]
    normalized = img_array / 255.0
    # Apply power law transformation
    transformed = np.power(normalized, gamma)
    # Scale back to [0,255]
    transformed = (transformed * 255).astype(np.uint8)
    return transformed

def log_transform(img_array):
    """Menerapkan log transformation"""
    # Convert to float and add 1 to avoid log(0)
    img_float = img_array.astype(float) + 1
    # Get maximum value
    max_val = np.max(img_float)
    # Apply log transformation
    c = 255 / np.log(1 + max_val)
    transformed = c * np.log(1 + img_float)
    # Convert back to uint8
    transformed = transformed.astype(np.uint8)
    return transformed

def contrast_stretching(img_array):
    """Menerapkan contrast stretching sesuai rumus t(i,j) = 255 * (I(i,j) - a) / (b - a)"""
    # Meminta input nilai minimum dan maksimum dari user
    a = int(input("Masukkan nilai piksel minimum (a): "))
    b = int(input("Masukkan nilai piksel maksimum (b): "))
    
    # Validasi input
    if a >= b:
        raise ValueError("Nilai minimum harus lebih kecil dari nilai maksimum")
    if a < 0 or b > 255:
        raise ValueError("Nilai harus berada dalam rentang 0-255")
    
    print(f"Nilai piksel minimum (a): {a}")
    print(f"Nilai piksel maksimum (b): {b}")
    
    # Debug: print beberapa nilai sebelum stretching
    print("\nBeberapa nilai sebelum stretching:")
    print(f"Sample values before stretching: {img_array[0:5, 0:5]}")
    
    # Konversi ke float untuk perhitungan
    img_float = img_array.astype(float)
    
    # Contrast stretching transformation: t(i,j) = 255 * (I(i,j) - a) / (b - a)
    stretched = 255 * (img_float - a) / (b - a)
    
    # Konversi kembali ke uint8
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)
    
    # Debug: print beberapa nilai setelah stretching
    print("\nBeberapa nilai setelah stretching:")
    print(f"Sample values after stretching: {stretched[0:5, 0:5]}")
    
    # Debug: print statistik
    print("\nStatistik gambar:")
    print(f"Original - Min: {np.min(img_array)}, Max: {np.max(img_array)}, Mean: {np.mean(img_array):.2f}")
    print(f"Stretched - Min: {np.min(stretched)}, Max: {np.max(stretched)}, Mean: {np.mean(stretched):.2f}")
    
    return stretched

def histogram_equalization(img_array):
    """Menerapkan histogram equalization"""
    # Flatten ke 1D
    flat = img_array.flatten()
    
    # Hitung histogram dan bins
    hist, bins = np.histogram(flat, bins=256, range=[0, 256])
    
    # Hitung CDF
    cdf = hist.cumsum()
    
    # Normalisasi CDF
    cdf_normalized = cdf * 255 / cdf[-1]
    
    # Mapping ke CDF baru
    equalized_flat = cdf_normalized[flat]
    equalized_img = equalized_flat.reshape(img_array.shape)
    
    # Konversi ke uint8
    equalized_img = equalized_img.astype(np.uint8)
    
    # Debug prints
    print("\nStatistik gambar:")
    print(f"Original - Min: {np.min(img_array)}, Max: {np.max(img_array)}, Mean: {np.mean(img_array):.2f}")
    print(f"Equalized - Min: {np.min(equalized_img)}, Max: {np.max(equalized_img)}, Mean: {np.mean(equalized_img):.2f}")
    
    return equalized_img

def terapkan_transformasi(image_path, transform_type):
    """Menerapkan transformasi piksel ke gambar"""
    try:
        # Membuka dan mengubah gambar ke grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Mengambil tanggal dan waktu saat ini untuk nama file
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Menerapkan transformasi sesuai jenis
        if transform_type == 1:  # Power Law
            gamma = float(input("Masukkan nilai gamma (0.1-3.0): "))
            transformed_array = power_law_transform(img_array, gamma)
            title_original = "Gambar Asli"
            title_transformed = f'Power Law Transformation (gamma={gamma})'
            output_name = f"power_law_{current_date}.png"
            tampilkan_gambar_dan_histogram(img_array, transformed_array, title_original, title_transformed)
            
        elif transform_type == 2:  # Log Transformation
            transformed_array = log_transform(img_array)
            title_original = "Gambar Asli"
            title_transformed = 'Log Transformation'
            output_name = f"log_transform_{current_date}.png"
            tampilkan_gambar_dan_histogram(img_array, transformed_array, title_original, title_transformed)
            
        elif transform_type == 3:  # Contrast Stretching
            transformed_array = contrast_stretching(img_array)
            title_original = "Gambar Asli"
            title_transformed = 'Contrast Stretching'
            output_name = f"contrast_stretching_{current_date}.png"
            tampilkan_gambar_dan_histogram(img_array, transformed_array, title_original, title_transformed)
            
        else:  # Histogram Equalization
            transformed_array = histogram_equalization(img_array)
            title_original = "Gambar Asli"
            title_transformed = 'Histogram Equalization'
            output_name = f"histogram_equalization_{current_date}.png"
            tampilkan_gambar_dan_histogram(img_array, transformed_array, title_original, title_transformed)
        
        transformed_img = Image.fromarray(transformed_array)
        
        # Menyimpan gambar hasil transformasi
        output_path = f"output/{output_name}"
        transformed_img.save(output_path)
        
        print(f"\nTransformasi berhasil dilakukan!")
        print(f"Gambar hasil disimpan di: {output_path}")
        
        return True
            
    except Exception as e:
        print(f"\nTerjadi kesalahan: {str(e)}")
        return False

def main():
    print("Selamat datang di Alat Transformasi Piksel")
    
    # Meminta pengguna untuk memilih gambar terlebih dahulu
    print("\nSilakan pilih gambar yang ingin ditransformasi:")
    image_path = pilih_gambar()
    
    if not image_path:
        print("Tidak ada gambar yang dipilih. Program dihentikan.")
        return
    
    print(f"Gambar yang dipilih: {image_path}")
    
    while True:
        tampilkan_menu()
        
        choice = input("Pilih opsi (1-4, atau 0): ")
        
        if choice == '0':
            print("\nTerima kasih telah menggunakan Alat Transformasi Piksel!")
            break
        
        elif choice in ['1', '2', '3', '4']:
            success = terapkan_transformasi(image_path, int(choice))
            
            if success:
                change = input("\nApakah Anda ingin memilih gambar baru? (y/n): ")
                if change.lower() == 'y':
                    image_path = pilih_gambar()
                    if not image_path:
                        print("Tidak ada gambar yang dipilih.")
                        break
                    print(f"Gambar yang dipilih: {image_path}")
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()

"""
PERBEDAAN TEKNIK PENGOLAHAN CITRA:

1. Power Law Transformation (Gamma Correction)
   - Menggunakan rumus s = c * r^γ
   - Cocok untuk memperbaiki citra yang terlalu terang/gelap
   - γ < 1: meningkatkan intensitas gelap
   - γ > 1: meningkatkan intensitas terang

2. Log Transformation
   - Menggunakan rumus s = c * log(1 + r)
   - Efektif untuk memperluas nilai piksel gelap
   - Menekan nilai piksel terang
   - Cocok untuk citra dengan rentang dinamis tinggi

3. Contrast Stretching
   - Memperluas rentang intensitas ke seluruh skala grayscale (0-255)
   - Meningkatkan kontras dengan memetakan nilai minimum ke 0 dan maksimum ke 255
   - Tidak mengubah distribusi histogram, hanya skala
   - Cocok untuk citra dengan kontras rendah

4. Histogram Equalization
   - Menyeragamkan distribusi intensitas citra
   - Mengubah histogram menjadi lebih merata
   - Meningkatkan kontras global
   - Cocok untuk citra dengan histogram yang tidak merata
"""