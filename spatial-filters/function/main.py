# Import library yang dibutuhkan
from PIL import Image, ImageFilter
import os
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# Buat folder output jika belum ada
os.makedirs("output", exist_ok=True)

def tampilkan_menu():
    """Menampilkan menu pilihan filter"""
    print("\n=== APLIKASI FILTER GAMBAR ===")
    print("1. Deteksi Tepi Canny")
    print("2. Filter Maksimum")
    print("3. Filter Minimum")
    print("4. Filter Median")
    print("5. Filter Mean (Rata-rata)")
    print("6. Deteksi Tepi Sobel")
    print("7. Prewitt Horizontal")
    print("8. Prewitt Vertikal")
    print("9. Prewitt Kombinasi")
    print("0. Keluar")

def pilih_gambar():
    """Fungsi untuk memilih file gambar menggunakan dialog"""
    # Buat window Tkinter minimal (tidak akan ditampilkan)
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window Tkinter
    
    # Tampilkan dialog pemilihan file
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar",
        filetypes=[("File Gambar", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    
    return file_path

def filter_canny(gray_img):
    """Menerapkan filter Canny (deteksi tepi)"""
    sobel = gray_img.filter(ImageFilter.FIND_EDGES)
    threshold = 100
    return sobel.point(lambda x: 255 if x > threshold else 0)

def filter_maximum(gray_img):
    """Menerapkan filter Maximum"""
    return gray_img.filter(ImageFilter.MaxFilter(size=3))

def filter_minimum(gray_img):
    """Menerapkan filter Minimum"""
    return gray_img.filter(ImageFilter.MinFilter(size=3))

def filter_median(gray_img):
    """Menerapkan filter Median"""
    return gray_img.filter(ImageFilter.MedianFilter(size=3))

def filter_mean(gray_img):
    """Menerapkan filter Mean (rata-rata)"""
    return gray_img.filter(ImageFilter.BoxBlur(radius=1))

def filter_sobel(gray_img):
    """Menerapkan filter Sobel (deteksi tepi)"""
    return gray_img.filter(ImageFilter.FIND_EDGES)

def filter_prewitt_horizontal(gray_img):
    """Menerapkan filter Prewitt horizontal"""
    prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
    return gray_img.filter(prewitt_h)

def filter_prewitt_vertical(gray_img):
    """Menerapkan filter Prewitt vertikal"""
    prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
    return gray_img.filter(prewitt_v)

def filter_prewitt_combined(gray_img):
    """Menerapkan kombinasi filter Prewitt horizontal dan vertikal"""
    prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
    prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
    h_filtered = gray_img.filter(prewitt_h)
    v_filtered = gray_img.filter(prewitt_v)
    return Image.blend(h_filtered, v_filtered, 0.5)

def buka_gambar(path):
    """Membuka gambar hasil filter dengan aplikasi default sistem"""
    try:
        if os.name == 'nt':  # Windows
            os.system(f'start "{path}"')
        elif os.name == 'posix':  # macOS dan Linux
            os.system(f'open "{path}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{path}"')
        print("Gambar dibuka di aplikasi default.")
    except:
        print("Tidak dapat membuka gambar secara otomatis.")

def terapkan_filter(image_path, filter_type):
    """Fungsi untuk menerapkan filter pada gambar"""
    try:
        # Buka gambar
        img = Image.open(image_path)
        
        # Konversi ke grayscale
        gray_img = img.convert('L')
        
        # Dapatkan tanggal dan waktu sekarang untuk nama file
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Dictionary mapping filter type ke fungsi dan nama file
        filter_options = {
            '1': {'func': filter_canny, 'name': 'canny'},
            '2': {'func': filter_maximum, 'name': 'max'},
            '3': {'func': filter_minimum, 'name': 'min'},
            '4': {'func': filter_median, 'name': 'median'},
            '5': {'func': filter_mean, 'name': 'mean'},
            '6': {'func': filter_sobel, 'name': 'sobel'},
            '7': {'func': filter_prewitt_horizontal, 'name': 'prewitt_h'},
            '8': {'func': filter_prewitt_vertical, 'name': 'prewitt_v'},
            '9': {'func': filter_prewitt_combined, 'name': 'prewitt_combined'}
        }
        
        # Mendapatkan filter yang dipilih
        selected_filter = filter_options.get(filter_type)
        
        if selected_filter:
            # Terapkan filter
            filtered = selected_filter['func'](gray_img)
            
            # Buat nama file output
            output_path = f"output/{selected_filter['name']}_{current_date}.png"
            
            # Simpan gambar hasil filter
            filtered.save(output_path)
            
            # Tampilkan hasil
            print(f"\nFilter berhasil diterapkan!")
            print(f"Gambar hasil disimpan di: {output_path}")
            
            # Tanya apakah ingin membuka file
            buka = input("\nBuka gambar hasil? (y/n): ")
            if buka.lower() == 'y':
                buka_gambar(output_path)
                
            return True
        else:
            print("Pilihan filter tidak valid.")
            return False
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

# Program utama
def main():
    print("Selamat datang di Aplikasi Filter Gambar CLI")
    
    # Meminta user untuk memilih gambar terlebih dahulu
    print("\nPilih gambar yang akan diedit:")
    image_path = pilih_gambar()
    
    if not image_path:
        print("Tidak ada gambar yang dipilih. Program berhenti.")
        return
    
    print(f"Gambar terpilih: {image_path}")
    
    while True:  # Looping agar program berjalan terus sampai user memilih keluar
        tampilkan_menu()  # Menampilkan menu pilihan operasi
        
        # Meminta input pilihan operasi dari user
        pilihan = input("Pilih operasi (1-9, 0 untuk keluar): ")
        
        if pilihan == '0':
            print("\nTerima kasih telah menggunakan Aplikasi Filter Gambar!")
            break
        
        elif pilihan in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            sukses = terapkan_filter(image_path, pilihan)
            
            # Jika filter berhasil, tanya apakah ingin pilih gambar baru
            if sukses:
                ganti = input("\nApakah ingin memilih gambar baru? (y/n): ")
                if ganti.lower() == 'y':
                    image_path = pilih_gambar()
                    if not image_path:
                        print("Tidak ada gambar yang dipilih.")
                        break
                    print(f"Gambar terpilih: {image_path}")
        else:
            print("\nPilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()