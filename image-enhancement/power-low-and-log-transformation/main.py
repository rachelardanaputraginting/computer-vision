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
            title = f'Power Law Transformation (gamma={gamma})'
            output_name = f"power_law_{current_date}.png"
        else:  # Log Transformation
            transformed_array = log_transform(img_array)
            title = 'Log Transformation'
            output_name = f"log_transform_{current_date}.png"
        
        transformed_img = Image.fromarray(transformed_array)
        
        # Menyimpan gambar hasil transformasi
        output_path = f"output/{output_name}"
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
        
        choice = input("Pilih opsi (1, 2, atau 0): ")
        
        if choice == '0':
            print("\nTerima kasih telah menggunakan Alat Transformasi Piksel!")
            break
        
        elif choice in ['1', '2']:
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


{
    
}