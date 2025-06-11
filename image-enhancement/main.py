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

def tampilkan_menu_utama():
    """Menampilkan menu utama"""
    print("\n=== MENU UTAMA TRANSFORMASI GAMBAR ===")
    print("1. Transformasi Piksel (T(x) = x + 50)")
    print("2. Transformasi Image Inverse")
    print("3. Power Law Transformation")
    print("4. Log Transformation")
    print("0. Keluar")

def pilih_gambar():
    """Fungsi untuk memilih file gambar menggunakan dialog"""
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar",
        filetypes=[("File Gambar", "*.png *.jpg *.jpeg")]
    )
    
    return file_path

def transformasi_pixel(img_array, offset=50):
    """Menerapkan transformasi piksel T(x) = x + offset menggunakan perulangan"""
    # Membuat array baru dengan ukuran yang sama
    transformed = np.zeros_like(img_array)
    
    # Melakukan transformasi piksel per piksel
    for i in range(img_array.shape[0]):  # baris
        for j in range(img_array.shape[1]):  # kolom
            # Menerapkan transformasi dan memastikan nilai tetap dalam range 0-255
            new_value = img_array[i, j] + offset
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            transformed[i, j] = new_value
    
    return transformed

def image_inverse(img_array):
    """Menerapkan transformasi inverse pada gambar menggunakan perulangan"""
    # Membuat array baru dengan ukuran yang sama
    transformed = np.zeros_like(img_array)
    
    # Melakukan transformasi piksel per piksel
    for i in range(img_array.shape[0]):  # baris
        for j in range(img_array.shape[1]):  # kolom
            # Menerapkan transformasi inverse
            transformed[i, j] = 255 - img_array[i, j]
    
    return transformed

def power_law_transform(img_array, gamma=1.0, c=1.0):
    """Menerapkan transformasi power law"""
    # Convert to float
    b1 = img_array.astype(float)
    # Get maximum value
    b3 = np.max(b1)
    # Normalize
    b2 = b1/b3
    # Apply gamma correction
    b3 = np.log(b2)*gamma
    # Perform gamma correction
    c = np.exp(b3)*255.0
    # Convert to int
    transformed = c.astype(int)
    return transformed

def log_transform(img_array, c):
    """Menerapkan transformasi logaritmik"""
    # Convert to float
    b1 = img_array.astype(float)
    # Get maximum value
    b2 = np.max(b1)
    # Perform log transformation
    transformed = (255.0*np.log(1+b1))/np.log(1+b2)
    # Convert to int
    transformed = transformed.astype(int)
    return transformed

def tampilkan_gambar(original, transformed, title):
    """Menampilkan gambar asli dan gambar hasil transformasi"""
    fig = plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Gambar Asli')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(transformed, cmap='gray')
    plt.title(title)
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def terapkan_transformasi(image_path, transform_type):
    """Menerapkan transformasi ke gambar"""
    try:
        # Membuka dan mengubah gambar ke grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Mengambil tanggal dan waktu saat ini untuk nama file
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Menerapkan transformasi sesuai jenis
        if transform_type == 1:
            transformed_array = transformasi_pixel(img_array)
            output_path = f"output/pixel_transform_{current_date}.png"
            title = 'Gambar Hasil Transformasi (T(x) = x + 50)'
        elif transform_type == 2:
            transformed_array = image_inverse(img_array)
            output_path = f"output/inverse_transform_{current_date}.png"
            title = 'Gambar Hasil Transformasi Inverse'
        elif transform_type == 3:
            gamma = float(input("Masukkan nilai gamma (0.1-3.0): "))
            c = float(input("Masukkan nilai konstanta c (0.1-10.0): "))
            transformed_array = power_law_transform(img_array, gamma, c)
            output_path = f"output/power_law_{current_date}.png"
            title = f'Power Law Transformation (gamma={gamma}, c={c})'
        else:  # transform_type == 4
            c = float(input("Masukkan nilai konstanta c (1-100): "))
            transformed_array = log_transform(img_array, c)
            output_path = f"output/log_transform_{current_date}.png"
            title = f'Log Transformation (c={c})'
        
        transformed_img = Image.fromarray(transformed_array.astype(np.uint8))
        
        # Menyimpan gambar hasil transformasi
        transformed_img.save(output_path)
        
        # Menampilkan hasil transformasi
        tampilkan_gambar(img_array, transformed_array, title)
        
        print(f"\nTransformasi berhasil dilakukan!")
        print(f"Gambar hasil disimpan di: {output_path}")
        
        return True
            
    except Exception as e:
        print(f"\nTerjadi kesalahan: {str(e)}")
        return False

def main():
    print("Selamat datang di Alat Transformasi Gambar")
    
    # Meminta pengguna untuk memilih gambar terlebih dahulu
    print("\nSilakan pilih gambar yang ingin ditransformasi:")
    image_path = pilih_gambar()
    
    if not image_path:
        print("Tidak ada gambar yang dipilih. Program dihentikan.")
        return
    
    print(f"Gambar yang dipilih: {image_path}")
    
    while True:
        tampilkan_menu_utama()
        
        choice = input("Pilih opsi (0-4): ")
        
        if choice == '0':
            print("\nTerima kasih telah menggunakan Alat Transformasi Gambar!")
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
