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
    print("5. Filter Mean (Rata-rata)")  # Filter baru
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

def terapkan_filter(image_path, filter_type):
    """Fungsi untuk menerapkan filter pada gambar"""
    try:
        # Buka gambar
        img = Image.open(image_path)
        
        # Konversi ke grayscale
        gray_img = img.convert('L')
        
        # Dapatkan tanggal dan waktu sekarang untuk nama file
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Terapkan filter sesuai pilihan
        if filter_type == '1':  # Canny
            sobel = gray_img.filter(ImageFilter.FIND_EDGES)
            threshold = 100
            filtered = sobel.point(lambda x: 255 if x > threshold else 0)
            output_path = f"output/canny_{current_date}.png"
            
        elif filter_type == '2':  # Max
            filtered = gray_img.filter(ImageFilter.MaxFilter(size=3))
            output_path = f"output/max_{current_date}.png"
            
        elif filter_type == '3':  # Min
            filtered = gray_img.filter(ImageFilter.MinFilter(size=3))
            output_path = f"output/min_{current_date}.png"
            
        elif filter_type == '4':  # Median
            filtered = gray_img.filter(ImageFilter.MedianFilter(size=3))
            output_path = f"output/median_{current_date}.png"
            
        elif filter_type == '5':  # Mean (filter baru)
            filtered = gray_img.filter(ImageFilter.BoxBlur(radius=1))  # BoxBlur adalah filter mean/rata-rata
            output_path = f"output/mean_{current_date}.png"
            
        elif filter_type == '6':  # Sobel
            filtered = gray_img.filter(ImageFilter.FIND_EDGES)
            output_path = f"output/sobel_{current_date}.png"
            
        elif filter_type == '7':  # Prewitt Horizontal
            prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
            filtered = gray_img.filter(prewitt_h)
            output_path = f"output/prewitt_h_{current_date}.png"
            
        elif filter_type == '8':  # Prewitt Vertikal
            prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
            filtered = gray_img.filter(prewitt_v)
            output_path = f"output/prewitt_v_{current_date}.png"
            
        elif filter_type == '9':  # Prewitt Kombinasi
            prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
            prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
            h_filtered = gray_img.filter(prewitt_h)
            v_filtered = gray_img.filter(prewitt_v)
            filtered = Image.blend(h_filtered, v_filtered, 0.5)
            output_path = f"output/prewitt_combined_{current_date}.png"
        
        # Simpan gambar hasil filter
        filtered.save(output_path)
        
        # Tampilkan hasil
        print(f"\nFilter berhasil diterapkan!")
        print(f"Gambar hasil disimpan di: {output_path}")
        
        # Tanya apakah ingin membuka file
        buka = input("\nBuka gambar hasil? (y/n): ")
        if buka.lower() == 'y':
            try:
                # Buka gambar dengan aplikasi default
                import os
                if os.name == 'nt':  # Windows
                    os.system(f'start {output_path}')
                elif os.name == 'posix':  # macOS dan Linux
                    os.system(f'open {output_path}' if os.uname().sysname == 'Darwin' else f'xdg-open {output_path}')
                print("Gambar dibuka di aplikasi default.")
            except:
                print("Tidak dapat membuka gambar secara otomatis.")
                
        return True
        
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