from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# Membuat direktori output jika belum ada
os.makedirs("output", exist_ok=True)

def tampilkan_menu():
    """Menampilkan menu transformasi"""
    print("\n=== MENU TRANSFORMASI PIXEL ===")
    print("1. Transformasi Piksel (T(x) = x + 50)")
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

def tampilkan_gambar(original, transformed):
    """Menampilkan gambar asli dan gambar hasil transformasi"""
    fig = plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Gambar Asli')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(transformed, cmap='gray')
    plt.title('Gambar Hasil Transformasi (T(x) = x + 50)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def terapkan_transformasi(image_path):
    """Menerapkan transformasi piksel ke gambar"""
    try:
        # Membuka dan mengubah gambar ke grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Mengambil tanggal dan waktu saat ini untuk nama file
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Menerapkan transformasi
        transformed_array = transformasi_pixel(img_array)
        transformed_img = Image.fromarray(transformed_array.astype(np.uint8))
        
        # Menyimpan gambar hasil transformasi
        output_path = f"output/pixel_transform_{current_date}.png"
        transformed_img.save(output_path)
        
        # Menampilkan hasil transformasi
        tampilkan_gambar(img_array, transformed_array)
        
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
        
        choice = input("Pilih opsi (1 atau 0): ")
        
        if choice == '0':
            print("\nTerima kasih telah menggunakan Alat Transformasi Piksel!")
            break
        
        elif choice == '1':
            success = terapkan_transformasi(image_path)
            
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
