# Import library yang dibutuhkan
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import os
from datetime import datetime

class ImageFilterApp:
    def __init__(self, root):
        # Inisialisasi aplikasi dengan window utama
        self.root = root
        self.root.title("Aplikasi Filter Gambar")
        self.root.geometry("1000x800")  # Ukuran default window
        
        # Buat folder output jika belum ada
        # exist_ok=True artinya tidak error kalau folder sudah ada
        os.makedirs("output", exist_ok=True)
        
        # Inisialisasi variabel-variabel penting
        self.image_path = None  # Lokasi file gambar
        self.original_image = None  # Gambar asli
        self.filtered_image = None  # Gambar hasil filter
        
        # Panggil fungsi untuk membuat elemen-elemen GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Buat frame-frame utama untuk organisasi layout
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)
        
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10)
        
        # Tombol untuk memilih gambar
        tk.Button(self.top_frame, text="Pilih Gambar", command=self.choose_image).pack(side=tk.LEFT, padx=10)
        
        # Variabel untuk menyimpan pilihan filter yang dipilih
        self.filter_var = tk.StringVar()
        self.filter_var.set("canny")  # Filter default yang terpilih
        
        # Daftar filter yang tersedia (nama tampilan, nilai variabel)
        filters = [
            ("Deteksi Tepi Canny", "canny"),
            ("Filter Maksimum", "max"),
            ("Filter Minimum", "min"),
            ("Filter Median", "median"),
            ("Deteksi Tepi Sobel", "sobel"),
            ("Prewitt Horizontal", "prewitt_h"),
            ("Prewitt Vertikal", "prewitt_v"),
            ("Prewitt Kombinasi", "prewitt_combined")
        ]
        
        # Buat radio button untuk setiap filter
        for text, value in filters:
            tk.Radiobutton(self.top_frame, text=text, variable=self.filter_var,
                          value=value, command=self.apply_filter).pack(side=tk.LEFT, padx=10)
        
        # Area tampilan gambar
        self.original_label = tk.Label(self.middle_frame, text="Gambar Asli")
        self.original_label.pack(side=tk.LEFT, padx=20)
        
        self.filtered_label = tk.Label(self.middle_frame, text="Gambar Hasil Filter")
        self.filtered_label.pack(side=tk.LEFT, padx=20)
        
        # Tombol untuk menerapkan filter
        tk.Button(self.bottom_frame, text="Terapkan Filter", command=self.apply_filter).pack(pady=10)
        
    def choose_image(self):
        # Membuka dialog untuk memilih file gambar
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("File Gambar", "*.png *.jpg *.jpeg *.bmp *.gif")]  # Format gambar yang didukung
        )
        if file_path:  # Jika pengguna memilih file
            self.image_path = file_path
            self.load_image(file_path)
            
    def load_image(self, path):
        try:
            # Coba membuka file gambar
            self.original_image = Image.open(path)
            # Ubah ukuran gambar agar pas di window (thumbnail = mempertahankan rasio aspek)
            self.original_image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(self.original_image)
            # Tampilkan gambar asli
            self.original_label.configure(image=photo)
            self.original_label.image = photo  # Simpan referensi agar tidak dihapus oleh garbage collector
            self.apply_filter()  # Terapkan filter default
        except Exception as e:
            # Tampilkan pesan error jika gagal membuka gambar
            messagebox.showerror("Error", f"Gagal memuat gambar: {str(e)}")
            
    def apply_filter(self):
        # Pastikan gambar sudah dipilih sebelum menerapkan filter
        if not self.original_image:
            return
            
        try:
            # Konversi ke grayscale (mode L = 8-bit pixel, hitam dan putih)
            img = self.original_image.convert('L')
            
            # Dapatkan tanggal dan waktu sekarang untuk nama file
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Terapkan filter sesuai pilihan
            filter_type = self.filter_var.get()
            
            if filter_type == 'canny':
                # Deteksi tepi Canny menggunakan Sobel dan thresholding
                sobel = img.filter(ImageFilter.FIND_EDGES)  # Sobel edge detection
                threshold = 100  # Nilai batas
                # Ubah pixel: jika > threshold maka putih (255), jika tidak maka hitam (0)
                filtered = sobel.point(lambda x: 255 if x > threshold else 0)
                output_path = f"output/canny_{current_date}.png"
                
            elif filter_type == 'max':
                # Filter Max: mengganti pixel dengan nilai maximum di sekitarnya
                filtered = img.filter(ImageFilter.MaxFilter(size=3))  # size 3x3 pixel
                output_path = f"output/max_{current_date}.png"
                
            elif filter_type == 'min':
                # Filter Min: mengganti pixel dengan nilai minimum di sekitarnya
                filtered = img.filter(ImageFilter.MinFilter(size=3))  # size 3x3 pixel
                output_path = f"output/min_{current_date}.png"
                
            elif filter_type == 'median':
                # Filter Median: mengganti pixel dengan nilai median di sekitarnya (mengurangi noise)
                filtered = img.filter(ImageFilter.MedianFilter(size=3))  # size 3x3 pixel
                output_path = f"output/median_{current_date}.png"
                
            elif filter_type == 'sobel':
                # Filter Sobel: deteksi tepi dengan operator Sobel
                filtered = img.filter(ImageFilter.FIND_EDGES)
                output_path = f"output/sobel_{current_date}.png"
                
            elif filter_type == 'prewitt_h':
                # Filter Prewitt horizontal: deteksi tepi horizontal
                # Matriks kernel Prewitt horizontal: [-1, 0, 1, -1, 0, 1, -1, 0, 1]
                prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
                filtered = img.filter(prewitt_h)
                output_path = f"output/prewitt_h_{current_date}.png"
                
            elif filter_type == 'prewitt_v':
                # Filter Prewitt vertikal: deteksi tepi vertikal
                # Matriks kernel Prewitt vertikal: [-1, -1, -1, 0, 0, 0, 1, 1, 1]
                prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
                filtered = img.filter(prewitt_v)
                output_path = f"output/prewitt_v_{current_date}.png"
                
            elif filter_type == 'prewitt_combined':
                # Kombinasi Prewitt horizontal dan vertikal
                prewitt_h = ImageFilter.Kernel((3, 3), [-1, 0, 1, -1, 0, 1, -1, 0, 1], 1)
                prewitt_v = ImageFilter.Kernel((3, 3), [-1, -1, -1, 0, 0, 0, 1, 1, 1], 1)
                h_filtered = img.filter(prewitt_h)  # Hasil filter horizontal
                v_filtered = img.filter(prewitt_v)  # Hasil filter vertikal
                # Gabungkan kedua hasil dengan blend (proporsi 50:50)
                filtered = Image.blend(h_filtered, v_filtered, 0.5)
                output_path = f"output/prewitt_combined_{current_date}.png"
            
            # Simpan gambar hasil filter
            filtered.save(output_path)
            
            # Tampilkan gambar hasil filter
            filtered.thumbnail((400, 400))  # Ubah ukuran agar pas di window
            photo = ImageTk.PhotoImage(filtered)
            self.filtered_label.configure(image=photo)
            self.filtered_label.image = photo  # Simpan referensi agar tidak dihapus garbage collector
            
            # Tampilkan pesan sukses
            messagebox.showinfo("Sukses", f"Filter berhasil diterapkan dan disimpan di: {output_path}")
            
        except Exception as e:
            # Tampilkan pesan error jika gagal menerapkan filter
            messagebox.showerror("Error", f"Gagal menerapkan filter: {str(e)}")

# Program utama
if __name__ == "__main__":
    root = tk.Tk()  # Buat window tkinter
    app = ImageFilterApp(root)  # Inisialisasi aplikasi
    root.mainloop()  # Jalankan aplikasi (looping event)